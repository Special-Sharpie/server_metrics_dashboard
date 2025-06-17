// stores/useStatusStore.js
import { defineStore } from 'pinia'
import axios from 'axios'

export const useStatusStore = defineStore('status', {
  state: () => ({
    serverOnline: false,
    latency: null,
    version: "",
    motd: '',
    online: 0,
    max: 0,
    icon: '',
    players: [],
    loading: false,
    error: null,
  }),

  actions: {
    async fetchStatus() {
      this.loading = true
      this.error = null
      try {
        const response = await axios.get('http://192.168.0.189:8000/status')
        const data = response.data
        // console.log("in store", data.players)

        this.serverOnline = data.server_online
        this.latency = data.latency
        this.version = data.version.name
        this.motd = data.motd
        this.online = data.online
        this.max = data.max
        this.icon = data.icon
        this.players = data.players
      } catch (err) {
        this.error = err.message || 'Failed to fetch server status'
        console.error(err)
      } finally {
        this.loading = false
      }
    },
  },
})
