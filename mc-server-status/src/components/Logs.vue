<template>
  <b-col md="12">
    <b-card bg-variant="dark" text-variant="light" class="log-viewer">
      <b-row class="mb-2">
        <b-col>
        </b-col>
        <b-col cols="auto">
          <b-form-checkbox v-model="autoScroll" switch size="sm">
            Auto-scroll
          </b-form-checkbox>
        </b-col>
      </b-row>

      <div ref="logContainer" class="log-container bg-black text-light p-2 rounded overflow-auto">
        <div
          v-for="(log, index) in logs"
          :key="index"
          class="log-entry d-flex flex-wrap align-items-start"
        >
          <span class="me-2">[{{ formatTimestampToTime(log.timestamp) }}]</span>
          <b-badge
          :variant="levelVariant(log.level)"
            class="me-2 text-uppercase"
            style="width: 60px;"
          >
            {{ log.level }}
          </b-badge>
          <span class="message">{{ log.message }}</span>
        </div>
      </div>
    </b-card>
  </b-col>
</template>

<script setup>
import { ref, watch, nextTick, onMounted } from 'vue'

const logs = ref([])

const autoScroll = ref(true)
const logContainer = ref(null)

const logsWorker = new Worker("/workers/logs-worker.js")

function levelVariant(level) {
  switch (level.toLowerCase()) {
    case 'info':
      return 'info'
    case 'warn':
      return 'warning'
    case 'error':
      return 'danger'
    case 'debug':
      return 'secondary'
    default:
      return 'light'
  }
}


watch(() => logs.value.length, () => {
  if (autoScroll.value) {
    nextTick(() => {
      const container = logContainer.value
      if (container) container.scrollTop = container.scrollHeight
    })
  }
})
onMounted(() => {
    logsWorker.onmessage = (event) => {
      if (logs.value.length === 0) {
        logs.value = event.data
      } else {
        logs.value.push(...event.data)
}
    };

    logsWorker.postMessage({ action: 'start' });
})
function formatTimestampToTime(timestamp) {
    const date = new Date(timestamp * 1000) // convert UNIX timestamp to milliseconds
    const hours = String(date.getHours()).padStart(2, '0')
    const minutes = String(date.getMinutes()).padStart(2, '0')
    const seconds = String(date.getSeconds()).padStart(2, '0')
    
    return `${hours}:${minutes}:${seconds}`
}

</script>

<style scoped>
.log-container {
  max-height: 300px;
}
.message {
  white-space: pre-wrap;
}
</style>
