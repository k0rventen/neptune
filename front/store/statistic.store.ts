import { defineStore } from "pinia";

export const useStatStore = defineStore('stats', () => {
    const stats = ref(undefined)
    const statsHisto = ref(undefined)
    const mostPopular = ref(undefined)

    const getStats = async () => {
        await useBaseAPI('statistics?current=true', {
            method: 'GET'
        }).then(({ data }) => {
            stats.value = data.value
        })
    }

    const getFiveImages = async () => {
        await useBaseAPI('tags/featured', {
            method: 'GET'
        }).then(({ data }) => {
            mostPopular.value = data.value
        })
    }

    const getHistoricalStat = async () => {
        await useBaseAPI('statistics?current=false', {
            method: 'GET'
        }).then(({ data }) => {
            statsHisto.value = data.value   
        })
    }

    return { stats, getStats, getFiveImages, mostPopular, getHistoricalStat, statsHisto }
})