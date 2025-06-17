<script setup>
    import { onMounted, ref, watch } from 'vue'
    import { useStatusStore } from '@/stores/useStatusStore'
    import Logs from "./Logs.vue"
    import axios from 'axios'

    // Format UNIX timestamp difference to HH:MM:SS
    function formatTimeSince(timestamp) {
        const now = Math.floor(Date.now() / 1000)
        let diff = now - timestamp
        if (diff < 0) diff = 0

        const hours = String(Math.floor(diff / 3600)).padStart(2, '0')
        const minutes = String(Math.floor((diff % 3600) / 60)).padStart(2, '0')
        const seconds = String(diff % 60).padStart(2, '0')

        return `${hours}:${minutes}:${seconds}`
    }

    const statusWorker = new Worker("/workers/server-status-worker.js")
    
    const statusStore = ref([])
    onMounted(() => {
      statusWorker.onmessage = (event) => {
        statusStore.value = event.data;
    };

    statusWorker.postMessage({ action: 'start' });
    })

</script>

<template>
    <div v-if="statusStore.loading">Loading...</div>
    <div v-else-if="statusStore.error">Error: {{ statusStore.error }}</div>
    <div v-else>
        <b-row class="justify-content-md-center">
            <b-col xl="5" class="dashboard-cell">
                <h4>Server Overview</h4>
                <b-avatar v-if="statusStore.icon" :src="statusStore.icon" square size="64px" style="border: 1px solid black;"></b-avatar>
                <span style="font-size: 20px; font-weight: 400;margin-left: 10px;">
                    {{ statusStore.motd }}
                </span>
                <div :style="{ width: (statusStore.max * 20 + (statusStore.max - 1) * 1) + 'px' }">
                    <span style="margin-top: 16px; margin-bottom: 0px;">Players Online:</span>
                    <span style="margin-bottom: 0px; float: right;">{{ statusStore.online }} / {{ statusStore.max }}</span>
                </div>
                <svg :width="statusStore.max* 20 + (statusStore.max - 1) * 1" :height="20" xmlns="http://www.w3.org/2000/svg">
                    <rect
                    v-for="n in statusStore.max"
                    :key="n"
                    :x="(n - 1) * (20 + 1)"
                    y="0"
                    :width="20"
                    :height="20"
                    :fill="n <= statusStore.online ? '#22c55e' : '#e5e7eb'"
                    stroke="#111827"
                    stroke-width="2"
                    rx="2"
                    />
                </svg>
            </b-col>
            <b-col xl="3" class="dashboard-cell">
                <h4>Server Status</h4>
                  <div class="status-header">
                    <span class="status-badge" :class="statusStore.serverOnline ? 'online' : 'offline'">
                    {{ statusStore.serverOnline ? '🟢 Online' : '🔴 Offline' }}
                    </span>
                </div>
                <p>Latency: {{ statusStore.latency }} ms</p>
                <p>
                    Version:
                    <span class="version-badge">{{ statusStore.version }}</span>
                </p>
            </b-col>
        </b-row>
        <b-row class="justify-content-md-center">
            <b-col xl="8" class="dashboard-cell">
                <b-row>
                    <b-col md="3" v-for="p in statusStore.players" :key="p[1]" style="padding-bottom: 5px;">
                        <b-avatar
                            :src="`https://crafatar.com/avatars/${p[1]}?size=64`"
                            size="32px"
                            square
                            class="player-avatar"
                        />
                        <span>{{ p[0] }}</span>
                        <span>{{ formatTimeSince(p[2]) }}</span>
                    </b-col>
                </b-row>
            </b-col>
        </b-row>
        <Logs />
    </div>
</template>

<style scoped>
.dashboard-cell {
  background-color: #ffffff;
  border-radius: 12px;
  padding: 20px;
  box-shadow: 0 1px 4px rgba(0, 0, 0, 0.06);
  margin: 10px 5px;
}

.version-badge {
  background-color: #3b82f6;
  color: white;
  padding: 2px 6px;
  font-size: 0.85rem;
  border-radius: 4px;
}

.status-header {
  display: flex;
  justify-content: space-between;
  margin-bottom: 12px;
}

.status-badge {
  padding: 4px 8px;
  font-size: 0.9rem;
  font-weight: 600;
  border-radius: 4px;
  color: white;
}

.status-badge.online {
  background-color: #22c55e;
}

.status-badge.offline {
  background-color: #ef4444;
}

.status-body {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.status-line {
  display: flex;
  justify-content: space-between;
  font-size: 0.95rem;
}

.version-badge {
  background-color: #3b82f6;
  color: white;
  padding: 2px 6px;
  font-size: 0.85rem;
  border-radius: 4px;
}

svg {
  margin-top: 5px;
}

.player-avatar {
  border: 2px solid #111827;
  margin-right: 8px;
}

h4 {
  font-weight: 600;
  color: #1f2937;
}
</style>