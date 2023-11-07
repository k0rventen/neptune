import { defineStore } from "pinia";

export const useRegistryStore = defineStore('registry', () => {
    const registries: any = ref([])

    const getRegistries = async () => {
        await useBaseAPI('registries', {
            method: 'GET'
        }).then(({ data }) => {
            registries.value = data.value
        })
    }

    const sendRegistry = async (data: unknown) => {
        await useBaseAPI('registries', {
            method: 'POST',
            body: JSON.stringify(data)
        }).then(() => {
            registries.push(data)
        })
    }

    return { registries, getRegistries, sendRegistry }
})