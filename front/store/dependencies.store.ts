import { defineStore } from "pinia";

export const useDepStore = defineStore('dependence', () => {

    const dependencies = ref([])

    const getPackages = async ({page, perPage, filter}) => {
        await useBaseAPI(urlBuilder(page,perPage,filter), {
            method: 'GET'
        }).then(({ data }) => {
            dependencies.value = data.value
        })
    }

    const urlBuilder = (page: number, perPage: number, filter: object) => {
        let url = `packages?page=${page}&per_page=${perPage}`
        if (filter) {
            Object.entries(filter).forEach(([key, value]) => {
                if (value) {
                    url += `&${key}=${value}`
                }
            })
        }
        return url
    }

    return { getPackages, dependencies }
})