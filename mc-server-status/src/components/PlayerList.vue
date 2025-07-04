<template>
    <h4 class="mb-3">Server Users</h4>
    <hr/>
    <PlayerListItem v-for="p in players" :key="p.uuid" :player="p" />
</template>

<script setup>
import { onMounted, ref } from 'vue'
import PlayerListItem from './PlayerListItem.vue';
import { Axios } from 'axios';

const playerListWorker = new Worker('/workers/play-time-worker.js')

const players = ref([])

onMounted(()=>{

    playerListWorker.onmessage = (event) => {
        players.value = [...event.data]
    }

    playerListWorker.postMessage({action: "start"})
})

</script>

<style scoped>

</style>