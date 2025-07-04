<script setup>
    import { onMounted, ref, watch } from 'vue'
    import ApexCharts from 'vue3-apexcharts'


    const resourceWorker = new Worker("/workers/resource-worker.js")
    
    const animatedSeries = ref([0])
    const animatedMemory = ref([0])

    const cpuChartOptions = {
    chart: {
        type: 'radialBar',
        offsetY: 0,
        height: 300,
        // wdith: 150,
        animations: {
            enabled: true,
            easing: 'easeinout',
            speed: 1000,
            animateGradually: {
                enabled: true,
                delay: 150
            },
            dynamicAnimation: {
                enabled: true,
                speed: 1000
            }
        }
    },
    grid: {
        show: true,
        padding: {
            top: 0,
            right: 0,
            bottom: 0,
            left: 0
        }
    },
    plotOptions: {
        radialBar: {
            startAngle: -130,
            endAngle: 130,
            track: {
                background: "#e7e7e7",
                strokeWidth: '97%',
                margin: 5,
            },
            dataLabels: {
                name: { show: false },
                value: {
                    fontSize: '24px',
                    formatter: val => `${val}%`
                }
            }
        }
    },
    fill: {
        colors: ['#A72E33']
        },
    labels: ['Usage']
    }
    const memChartOptions = {
    chart: {
        type: 'radialBar',
        offsetY: 0,
        // height: 100,
        animations: {
            enabled: true,
            easing: 'easeinout',
            speed: 1000,
            animateGradually: {
                enabled: true,
                delay: 150
            },
            dynamicAnimation: {
                enabled: true,
                speed: 1000
            }
        }
    },
    grid: {
        show: true,
        padding: {
            top: 0,
            right: 0,
            bottom: 0,
            left: 0
        }
    },
    plotOptions: {
        radialBar: {
            startAngle: -130,
            endAngle: 130,
            track: {
                background: "#e7e7e7",
                strokeWidth: '97%',
                margin: 5,
            },
            dataLabels: {
                name: { show: false },
                value: {
                    fontSize: '24px',
                    formatter: () => `${resource.value.memory_used}MB / ${resource.value.max_memory}MB`
                }
            }
        }
        },
        fill: {
            colors: ['#A72E33']
            },
        labels: ['Memory']
    }

    const resource = ref([])
    onMounted(() => {
      resourceWorker.onmessage = (event) => {
        resource.value = event.data;
        animatedSeries.value = [resource.value.cpu_usage]
        animatedMemory.value = [(resource.value.memory_used / resource.value.max_memory) * 100]
    };

    resourceWorker.postMessage({ action: 'start' });

    // setTimeout(() => {
    //         animatedSeries.value = [resource.value.cpu]
    //     }, 200) // Optional delay for smoother loading experience
    })
    watch(resource.value.cpu, (newValue) => {
        animatedSeries.value = [newValue]
    }, { immediate: true })


</script>

<template>

    <b-col md="6">
        <b-card class="mb-3 shadow-sm" style="height: 100%;">
            <h4 class="mb-2">CPU Usage</h4>
            <hr />
            <ApexCharts type="radialBar" :options="cpuChartOptions" :series="animatedSeries" />
        </b-card>
    </b-col>
    <b-col md="6">
        <b-card class="mb-3 shadow-sm" style="height: 100%;">
            <h4 class="mb-2">Memory Usage</h4>
            <hr />
            <ApexCharts type="radialBar" :options="memChartOptions" :series="animatedMemory" />
        </b-card>
    </b-col>
</template>

<style scoped>

</style>