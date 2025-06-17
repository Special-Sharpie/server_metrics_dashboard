const interval = 1000

self.loop = async () => {
    await fetch("http://192.168.0.189:8000/logs")
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