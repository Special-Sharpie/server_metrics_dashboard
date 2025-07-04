const interval = 1000
const DEV_IP = "192.168.1.70"


self.loop = async () => {
    await fetch(`http://${DEV_IP}:8000/status`)
    .then(r => r.json())
    .then((data)=>{
        server = {
            serverOnline : data.server_online,
            latency : data.latency,
            version : data.version.name,
            motd : data.motd,
            online : data.online,
            max : data.max,
            icon : data.icon,
            players : data.players,
        }
        self.postMessage(server)
    })

    setTimeout(self.loop, interval);
}

self.onmessage = ({ data }) => {
    if (data.action === "start") {
        self.loop();
    }
};