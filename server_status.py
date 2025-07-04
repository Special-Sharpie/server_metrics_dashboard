from typing import Optional
from fastapi import FastAPI
from mcstatus import JavaServer
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import random

import mysql.connector
from mysql.connector import Error

app = FastAPI()

SERVER_ADDRESS = "192.168.1.70:25565"
LIVE = True
# RESTART_FILE = "/path/to/restart_timestamp.txt"  # Create this on startup

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # or ["*"] to allow all origins (not recommended in production)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def get_db_connection():
    try:
        connection = mysql.connector.connect(
            host="127.0.0.1",
            database="server_metrics",
            user="root",
            password="password"
        )
        if connection.is_connected():
            return connection
    except Error as e:
        print("----------------------------\n",
            "Error connecting to database:\n", 
            e,
            "----------------------------\n"
            )

def db_query(conn, query, params=[], dictionary=False):
    try: 
        if dictionary:
            cursor = conn.cursor(dictionary=True)
        else: 
            cursor = conn.cursor()
        cursor.execute(query, params)
        if(query[:6] in ("UPDATE", "DELETE", "INSERT")):
            result = conn.commit()
        else:
            result = cursor.fetchall()
        cursor.close()
        return result
    except Error as e:
            print("----------------------------\n",
            "Error querying database:\n", 
            e,
            "----------------------------\n"
            )

@app.get("/status")
async def status():
    # Get Minecraft server info
    try:
        server = JavaServer.lookup(SERVER_ADDRESS)
        status = server.status()
        server.ping()
        players = status.players.online
        player_details = status.players.sample
        max_players = status.players.max
        motd = status.description
        version = status.version
        latency = status.latency
        icon = status.icon
        server_online = True
        player_ls = [[player.name, player.id] for player in player_details] if player_details else []

        conn = get_db_connection()
        query = """SELECT timestamp FROM events WHERE event=1 AND username=%s ORDER BY id DESC LIMIT 1"""
        for p in player_ls:
            result = db_query(conn, query, [p[0],])
            p.append(result[0][0])

    except Exception:
        players = None
        max_players = None
        motd = None
        server_online = False

    return {
        "server_online": server_online,
        "latency": latency,
        "version": version,
        "motd":motd,
        "online":players,
        "max":max_players,
        "icon": icon,
        "players": player_ls
	}


class ConnectionEvent(BaseModel):
    username: str
    event: bool
    timestamp: int
    uuid: Optional[str] = None

@app.post("/event")
async def events(data: ConnectionEvent):
    conn = get_db_connection()
    query = """INSERT INTO events (username, event, timestamp) VALUES (%s, %s, %s)"""
    result = db_query(conn, query, [data.username, data.event, data.timestamp])
    if data.event == 1:
        query = """SELECT * FROM player_uuid WHERE uuid = %s AND username= %s"""
        result = db_query(conn, query, [data.uuid, data.username])
        if len(result) == 0:
            query = """INSERT INTO player_uuid (uuid, username) VALUES (%s, %s)"""
            result = db_query(conn, query, [data.uuid, data.username])
    # print(result)
    # Record to database


class Position(BaseModel):
    x: int
    y: int
    z: int
    username: str
    timestamp: int

@app.post("/position")
async def position(data: Position):
    conn = get_db_connection()
    query = """INSERT INTO positions (x, y, z, username, timestamp) VALUES (%s, %s, %s, %s, %s)"""
    params = list(data.dict().values())
    result = db_query(conn, query, params)
    print(result)
    # Record to database

class Log(BaseModel):
    message: str
    level: str
    timestamp: int

@app.post("/logs")
async def logs(data: Log):
    conn = get_db_connection()
    query = """INSERT INTO logs (message, level, timestamp) VALUES (%s, %s, %s)"""
    params = list(data.dict().values())
    result = db_query(conn, query, params)
    print(result)


class ResourceUsage(BaseModel):
    totalMemory: int
    maxMemory: int
    cpuUsage: float


@app.post("/resources")
async def post_resources(data: ResourceUsage):
    conn = get_db_connection()
    try:
        query = """INSERT INTO resource_usage (memory_used, max_memory, cpu_usage) values (%s, %s, %s)"""
        result = db_query(conn, query, params=list(data.dict().values()))
    except Exception as e:
        raise e


@app.get("/timeplayed/{username}")
async def timeplayed(username: str):
    conn = get_db_connection()
    query = """SELECT timestamp FROM events WHERE event=1 AND username=%s ORDER BY id DESC LIMIT 1"""
    result = db_query(conn, query, [username,])
    return result[0][0]


@app.get("/online")
async def online():
    return True


@app.get("/logs")
async def logs(lastId: int):
    conn = get_db_connection()
    if (lastId ==0):
        query = """SELECT *
        FROM (
            SELECT *
            FROM logs
            ORDER BY id DESC
            LIMIT 500
        ) sub
        ORDER BY id ASC;
        """
        result = db_query(conn, query, [], dictionary=True)
    else:
        query = """SELECT * FROM logs WHERE id > %s"""
        result = db_query(conn, query, [lastId,], dictionary=True)
    return result


@app.get("/resources")
async def resources():
    conn = get_db_connection()
    if LIVE:
        try:
            query = """SELECT * from resource_usage ORDER BY id DESC LIMIT 1"""
            result = db_query(conn, query, [], dictionary=True)
            print(result)
            return result[0]
        except Exception as e:
            raise e
    else:
        return {"cpu": random.randint(0,100), "memory_usage": 10560}
    

@app.get("/session")
async def session():
    conn = get_db_connection()
    try:
        query = """
SELECT e.username, e.event, u.uuid, e.timestamp
FROM events e
JOIN player_uuid u ON e.username = u.username
WHERE e.timestamp = (
  SELECT MAX(e2.timestamp)
  FROM events e2
  WHERE e2.username = e.username
)
ORDER BY e.event DESC, e.timestamp DESC;
"""
        result = db_query(conn, query, [], dictionary=True)
        return result
    except Exception as e:
        raise e


