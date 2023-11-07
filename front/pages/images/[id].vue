<script setup>
import { useImageStore } from '~/store/images.store';

const imageStore = useImageStore()
const route = useRoute()
const router = useRouter()

await imageStore.getImage(route.params.id)

const copyNotes = ref({})
const { t } = useI18n()

const columns = [
    {
        name: t('img_detail.package'),
        key: 'package'
    },
    {
        name: t('img_detail.version'),
        key: 'version'
    },
    {
        name: t('img_detail.uptodate'),
        key: 'outdated',
        position: 'center'
    }
]

const vulnerabilitiesCol = [
    {
        name: t('img_detail.active'),
        key: 'ack'
    },
    {
        name: t('img_detail.cve'),
        key: 'name'
    },
    {
        name: t('img_detail.packages'),
        key: 'affected_package'
    },
    {
        name: t('img_detail.severity'),
        key: 'severity'
    },
    {
        name: t('img_detail.notes'),
        key: 'notes'
    }
]

const dataPackage = ref([
    ...imageStore.image.packages,
    ...imageStore.image.outdated_packages
])

const vulnData = ref([
    ...imageStore.image.vulnerabilities
])
vulnData.value.forEach((vuln) => {
    copyNotes.value[vuln.name] = vuln.notes
})

const vulnActive = ref([
    ...imageStore.image.active_vulnerabilities
])
vulnActive.value.forEach((vuln) => {
    copyNotes.value[vuln.name] = vuln.notes
})

const sendNewNotes = async (item) => {
    await imageStore.sendNotes(item, copyNotes.value[item.name])
}

const deleteImg = async () => {
    await imageStore.removeImg(route.params.id).then(() => {
        router.push('/images')
    })
}

const changeStatus = async (item) => {
    await imageStore.sendState(item, !item.active).then(() => {
        vulnActive.value = [...imageStore.image.active_vulnerabilities]
        vulnActive.value.forEach((vuln) => {
            copyNotes.value[vuln.name] = vuln.notes
        })
        vulnData.value = [
            ...imageStore.image.vulnerabilities
        ]
        vulnData.value.forEach((vuln) => {
            copyNotes.value[vuln.name] = vuln.notes
        })
    })
}
</script>

<template>
        <div class="bg-primary w-full p-5 text-white rounded relative">
            <svg @click="deleteImg" class="absolute w-4 right-5 top-5 fill-white cursor-pointer" clip-rule="evenodd" fill-rule="evenodd" stroke-linejoin="round" stroke-miterlimit="2" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><path d="m12 10.93 5.719-5.72c.146-.146.339-.219.531-.219.404 0 .75.324.75.749 0 .193-.073.385-.219.532l-5.72 5.719 5.719 5.719c.147.147.22.339.22.531 0 .427-.349.75-.75.75-.192 0-.385-.073-.531-.219l-5.719-5.719-5.719 5.719c-.146.146-.339.219-.531.219-.401 0-.75-.323-.75-.75 0-.192.073-.384.22-.531l5.719-5.719-5.72-5.719c-.146-.147-.219-.339-.219-.532 0-.425.346-.749.75-.749.192 0 .385.073.531.219z"/></svg>
            <div class="w-3/4 grid grid-cols-2 gap-x-5">
                <p>{{ t('img_detail.img_name') }}: {{ imageStore.image.image }}:{{ imageStore.image.tag }}</p>
                <p>{{ t('img_detail.packages') }}: {{ imageStore.image.packages.length }}</p>
                <p>{{ t('img_detail.img_size') }}: {{ useCalcConverter(imageStore.image.size) }}</p>
                <p>{{ t('img_detail.vulnerabilities') }}: {{ imageStore.image.vulnerabilities.length }}</p>
                <p>{{ t('img_detail.added_date') }}: {{ new Date(imageStore.image.date_added).toLocaleDateString('fr-FR') + ' à ' + new
                    Date(imageStore.image.date_added).toLocaleTimeString('fr-FR') }}</p>
                <p>{{ t('img_detail.active_vuln') }}: {{ imageStore.image.active_vulnerabilities.length }}</p>
                <p>{{ t('img_detail.distro') }}: {{ imageStore.image.distro }}</p>
                <p>{{ t('img_detail.outdated_package') }}: {{ imageStore.image.outdated_packages.length }}</p>
            </div>
        </div>
        <div class="grid w-full grid-cols-2 grid-rows-2 mt-5 gap-5">
            <div class="row-span-2 bg-white p-3">
                <custom-table :columns="columns" :data="dataPackage">
                    <template #outdated="{ item }">
                        <div class="w-full flex justify-center">
                            <svg v-if="item.outdated" class="fill-red-500" xmlns="http://www.w3.org/2000/svg" width="24"
                                height="24" viewBox="0 0 24 24">
                                <path
                                    d="M12 0c-6.627 0-12 5.373-12 12s5.373 12 12 12 12-5.373 12-12-5.373-12-12-12zm5.5 16.084l-1.403 1.416-4.09-4.096-4.102 4.096-1.405-1.405 4.093-4.092-4.093-4.098 1.405-1.405 4.088 4.089 4.091-4.089 1.416 1.403-4.092 4.087 4.092 4.094z" />
                            </svg>
                            <svg v-else class="fill-green-600" xmlns="http://www.w3.org/2000/svg" width="24" height="24"
                                viewBox="0 0 24 24">
                                <path
                                    d="M12 0c-6.627 0-12 5.373-12 12s5.373 12 12 12 12-5.373 12-12-5.373-12-12-12zm-1.25 16.518l-4.5-4.319 1.396-1.435 3.078 2.937 6.105-6.218 1.421 1.409-7.5 7.626z" />
                            </svg>
                        </div>
                    </template>
                </custom-table>
            </div>
            <div class="bg-white p-3">
                <custom-table :columns="vulnerabilitiesCol" :data="vulnActive">
                    <template #ack="{ item }">
                        <button @click="changeStatus(item)" class="px-2 py-1 rounded-md text-xs text-white uppercase font-bold"
                            :class="item.active ? 'bg-green-600' : 'bg-gray-400'">
                            {{
                                item.active
                                ? $t('vulnerabilities.active')
                                : $t('vulnerabilities.inactive')
                            }}
                        </button>
                    </template>
                    <template #severity="{ item }">
                        <div class="px-2 py-1 rounded-md text-white text-center w-36 uppercase font-bold"
                            :class="useColorSeverity(item)">
                            {{
                                $t(`vulnerabilities.state.${item.severity.toLowerCase()}`)
                            }}
                        </div>
                    </template>
                    <template #notes="{ item }">
                        <input v-model="copyNotes[item.name]" @focusout="sendNewNotes(item)" class="outline-none bg-transparent"
                            type="text">
                    </template>
                </custom-table>
            </div>
            <div class="bg-white p-3">
                <custom-table :columns="vulnerabilitiesCol" :data="vulnData">
                    <template #ack="{ item }">
                        <button @click="changeStatus(item)" class="px-2 py-1 rounded-md text-xs text-white uppercase font-bold"
                            :class="item.active ? 'bg-green-600' : 'bg-gray-400'">
                            {{
                                item.active
                                ? $t('vulnerabilities.active')
                                : $t('vulnerabilities.inactive')
                            }}
                        </button>
                    </template>
                    <template #severity="{ item }">
                        <div class="px-2 py-1 rounded-md text-white text-center w-36 uppercase font-bold"
                            :class="useColorSeverity(item)">
                            {{
                                $t(`vulnerabilities.state.${item.severity.toLowerCase()}`)
                            }}
                    </div>
                </template>
                        <template #notes="{ item }">
                                <input v-model="copyNotes[item.name]" @focusout="sendNewNotes(item)" class="outline-none bg-transparent"
                                    type="text">
                            </template>
        </custom-table>
    </div>
</div></template>