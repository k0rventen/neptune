import { defineStore } from "pinia";

export const useImageStore = defineStore('image', () => {
    const images: any = ref([])
    const image: any = ref(undefined)

    const getImages = async ({page, perPage, filter}) => {
        await useBaseAPI(urlBuilder(page, perPage, filter), {
            method: 'GET'
        }).then(({ data }) => {
            images.value = data.value
        })
    }

    const scanImage = async (image) => {
        await useBaseAPI('scan', {
            method: 'POST',
            body: JSON.stringify(image)
        }).then(({ data }) => {
            images.value.push(data.value)
        })
    }

    const getImage = async (sha: string) => {
        await useBaseAPI(`/tags/${sha}`, {
            method: 'GET'
        }).then(({ data }) => {
            image.value = data.value
        })
    }

    const urlBuilder = (page: number, perPage: number, filter: object) => {
        let url = `tags?page=${page}&per_page=${perPage}`
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
        await useBaseAPI(`/vulnerabilities/${item.id}`, {
            method: 'PUT',
            body: JSON.stringify({ active: item.active, notes })
        }).then(() => {
            if(item.active) {
                image.value.active_vulnerabilities.find((el) => el.name === item.name).notes = notes
            } else {
                image.value.vulnerabilities.find((el) => el.name === item.name).notes = notes
            }
            console.log(image.value)
        })
    }

    const removeImg = async (sha) => {
        await useBaseAPI(`tags/${sha}`, {
            method: 'DELETE'
        })
    }

    const sendState = async (item, active) => {
        await useBaseAPI(`/vulnerabilities/${item.id}`, {
            method: 'PUT',
            body: JSON.stringify({ active, notes: item.notes })
        }).then(() => {
            if(!active) {
                const index = image.value.active_vulnerabilities.findIndex((el) => el.id === item.id)
                const editVuln = {...image.value.active_vulnerabilities[index]}
                editVuln.active = false
                image.value.vulnerabilities.push(editVuln)
                image.value.active_vulnerabilities = [...image.value.active_vulnerabilities.filter((el) => el.id !== item.id)]
            } else {
                const index = image.value.vulnerabilities.findIndex((el) => el.id === item.id)
                const editVuln = {...image.value.vulnerabilities[index]}
                editVuln.active = true
                image.value.active_vulnerabilities.push(editVuln)
                image.value.vulnerabilities = [...image.value.vulnerabilities.filter((el) => el.id !== item.id)]
            }
        })
    }

    return { images, image, getImage, getImages, scanImage, sendNotes, sendState, removeImg }
})