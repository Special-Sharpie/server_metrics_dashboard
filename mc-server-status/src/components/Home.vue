<script setup>
    import { onMounted, ref, watch } from 'vue'
    import { useStatusStore } from '@/stores/useStatusStore'
    import Logs from "./Logs.vue"
    import ResourceGraph from "./ResourceGraph.vue"
    import PlayerList from './PlayerList.vue'

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
        <b-container fluid class="p-3" style="border-left: 1px solid lightgray;border-right: 1px solid lightgray;height: 100%;"> 
          <b-card class="mb-3 shadow-sm">
            <h4 class="mb-2">Server Overview</h4>
              <b-avatar v-if="statusStore.icon" :src="statusStore.icon" square size="64px" style="border: 1px solid black;"></b-avatar>
              <span style="font-size: 20px; font-weight: 400;margin-left: 10px;">
                  {{ statusStore.motd }}
              </span>
            <b-row>
              <b-col md="4">
                <div :style="{ width: (statusStore.max * 20 + (statusStore.max - 1) * 1) + 'px' }">
                      <span style="margin-top: 16px; margin-bottom: 0px;"><strong>Players Online: </strong></span>
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
              <b-col md="3"><strong>Latency: </strong>{{  Math.round(statusStore.latency * 100) / 100 }} ms</b-col>
              <b-col md="3">
                <strong>Status: </strong>
                <b-badge :class="statusStore.serverOnline ? 'online' : 'offline'" style="font-size:medium; padding-right: 15px;">
                    {{ statusStore.serverOnline ? '🟢 Online' : '🔴 Offline ' }}
                </b-badge>
                <!-- 22c55e -->
              </b-col>
              <b-col md="2">
                <strong>Version: </strong>
                <b-badge style="background-color: #A72E33 !important; font-size:medium; padding-right: 10px;">{{ statusStore.version }}</b-badge>
              </b-col>
            </b-row>
          </b-card>

          <b-row>
            <!-- Left: Active Users -->
            <b-col md="3" class="mb-3">
              <b-card class="h-100 shadow-sm">
                  <PlayerList />
              </b-card>
            </b-col>

            <!-- Right: Charts -->
            <b-col md="9" class="mb-3" >
              <b-row class="mb-3">
                <ResourceGraph />
              </b-row>
              <b-row>
                <Logs />
              </b-row>
            </b-col>
          </b-row>
          
          </b-container>
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

.online {
  background-color: #22c55e !important;
}
.offline {
  background-color: #e5e7eb !important;
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