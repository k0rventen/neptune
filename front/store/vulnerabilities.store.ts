import { defineStore } from "pinia";

export const useVulnerabilitiesStore = defineStore('vulnerabilities', () => {

    const vulnerabilities = ref(undefined)

    const getVulnerabilities = async ({page, perPage, filter}) => {
        await useBaseAPI(urlBuilder(page, perPage, filter), {
            method: 'GET'
        }).then(({ data }) => {
            vulnerabilities.value = data.value 
        })
    }

    const urlBuilder = (page: number, perPage: number, filter: object) => {
        let url = `vulnerabilities?page=${page}&per_page=${perPage}`
        if (filter) {
            Object.entries(filter).forEach(([key, value]) => {
                if (value) {
                    url += `&${key}=${value}`
                }
            })
        }
        return url
    }

    const sendNotes = async (item, notes) => {
        console.log(notes)
        await useBaseAPI(`/vulnerabilities/${item.id}`, {
            method: 'PUT',
            body: JSON.stringify({ active: item.active, notes })
        })
    }

    const sendState = async (item, active) => {
        await useBaseAPI(`/vulnerabilities/${item.id}`, {
            method: 'PUT',
            body: JSON.stringify({ active, notes: item.notes })
        }).then(() => {
            vulnerabilities.value.items.find((el) => el.name === item.name).active = active
        })
    }

    return { getVulnerabilities, vulnerabilities, sendNotes, sendState }
})