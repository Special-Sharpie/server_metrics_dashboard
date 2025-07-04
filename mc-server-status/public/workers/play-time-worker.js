const interval = 1000
const DEV_IP = "192.168.1.70"

self.loop = async () => {
    await fetch(`http://${DEV_IP}:8000/session`)
    .then(r => r.json())
    .then((data)=>{
        self.postMessage(data)
    })

    setTimeout(self.loop, interval);
}

self.onmessage = ({ data }) => {
    if (data.action === "start") {
        self.loop();
    }
};