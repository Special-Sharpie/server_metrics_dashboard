<template>
  <div class="d-flex justify-content-between align-items-center">
    <div class="d-flex align-items-center">
      <b-avatar
        v-bind="player.event ? { badge: true } : {}"
        badge-variant="success"
        :src="`https://crafatar.com/avatars/${player.uuid}?size=64`"
        size="48px"
        square
        class="player-avatar"
        style="margin-right: 1rem;"
      />
      <strong>{{ player.username }}</strong>
    </div>
    <span class="text-muted small" :class="player.event ? 'online' : 'offline'">
        <strong>
            {{ formatTimeSince(player.timestamp, player.event) }}
        </strong>
    </span>
  </div>
</template>

<script setup>
    const props = defineProps({
        player: {
            type: Object,
            required: true
        }
    })

    // const props = defineProps({
    // username: {
    //     type: String,
    //     required: true
    // },
    // uuid: {
    //     type: String,
    //     required: true
    // },
    // timestamp:{
    //     type: Number,
    //     required: true
    // }
    // })
function formatTimeSince(timestamp, event) {
    const now = Math.floor(Date.now() / 1000)
    let diff = now - timestamp
    if (diff < 0) diff = 0

    const secondsInMonth = 2592000  // 30 * 24 * 60 * 60
    const secondsInWeek = 604800    // 7 * 24 * 60 * 60
    const secondsInDay = 86400      // 24 * 60 * 60

    if (diff >= secondsInMonth) {
        const months = Math.floor(diff / secondsInMonth)
        return `${months} month${months === 1 ? '' : 's'} ago`
    } else if (diff >= secondsInWeek) {
        const weeks = Math.floor(diff / secondsInWeek)
        return `${weeks} week${weeks === 1 ? '' : 's'} ago`
    } else if (diff >= secondsInDay) {
        const days = Math.floor(diff / secondsInDay)
        return `${days} day${days === 1 ? '' : 's'} ago`
    } else {
        if (event) {
            const hours = String(Math.floor(diff / 3600)).padStart(2, '0')
            const minutes = String(Math.floor((diff % 3600) / 60)).padStart(2, '0')
            const seconds = String(diff % 60).padStart(2, '0')
            return `${hours}:${minutes}:${seconds}`
        } else {
            if (diff >= 3600) {
                const hours = Math.floor(diff / 3600)
                return `${hours} hour${hours === 1 ? '' : 's'} ago`
            } else if (diff >= 60) {
                const minutes = Math.floor(diff / 60)
                return `${minutes} minute${minutes === 1 ? '' : 's'} ago`
            } else {
                return `${diff} second${diff === 1 ? '' : 's'} ago`
            }
        }
    }
}


</script>

<style scoped>
.player-avatar {
  border: 2px solid #111827;
  margin-bottom: 8px;
}

.custom-badge{
  background-color: #22c55e !important; /* custom green */
  border: 2px solid #fff; /* optional for better contrast */
}

.online {
  color: #22c55e !important;
}
.offline {
  color: none
}

</style>