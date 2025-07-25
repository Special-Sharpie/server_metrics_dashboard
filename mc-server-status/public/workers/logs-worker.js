const interval = 1000
const DEV_IP = "192.168.1.70"
let lastId = 0


self.loop = async () => {
    await fetch(`http://${DEV_IP}:8000/logs?lastId=${lastId}`)
    .then(r => r.json())
    .then((data)=>{
        if (data.length > 0){
            lastId = data[data.length - 1].id
            self.postMessage(data)
        }
    })

    setTimeout(self.loop, interval);
}

self.onmessage = ({ data }) => {
    if (data.action === "start") {
        self.loop();
    }
};