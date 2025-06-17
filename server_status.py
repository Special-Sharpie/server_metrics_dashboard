from fastapi import FastAPI
from mcstatus import JavaServer
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

import mysql.connector
from mysql.connector import Error

app = FastAPI()

SERVER_ADDRESS = "mc.hockeystatsbot.ca"
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

@app.post("/event")
async def events(data: ConnectionEvent):
    conn = get_db_connection()
    query = """INSERT INTO events (username, event, timestamp) VALUES (%s, %s, %s)"""
    params = list(data.dict().values())
    result = db_query(conn, query, params)
    print(result)
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
async def logs():
    conn = get_db_connection()
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
    return result
    print(result)