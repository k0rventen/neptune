<script setup>
import { useImageStore } from '~/store/images.store';

const imageStore = useImageStore()

const pagination = reactive({
    page: 1,
    perPage: 20,
})

const filter = reactive({
    name_filter: undefined
})

const image = ref({
    image: undefined,
    return_error: false,
})
const openModal = ref(false)


const sendNewImg = async () => {
    await imageStore.scanImage(image.value)
}

const delay = ref(undefined)
const refresh = ref(0)

const delaySearch = (input) => {
    filter.name_filter = input.target.value
        clearTimeout(delay.value)
        delay.value = setTimeout(async () => {
            await imageStore.getImages({...pagination, filter})
            pagination.page = 1
            refresh.value++
        }, 750)
}

watch(pagination, async () => {
    await imageStore.getImages({...pagination, filter})
})

await imageStore.getImages({...pagination, filter})
</script>

<template>
        <!-- Modal add image -->
        <modal v-model="openModal">
                <template #header>
                    {{ $t('images.modal.title') }}
                </template>
                <form @submit.prevent="sendNewImg" class="flex flex-col justify-between w-full h-full min-h-[50vmin]">
                    <div class="mt-2">
                        <label>{{ $t('images.modal.img_name') }}:</label>
                        <input v-model="image.image" type="text" class="border-b-1 border ml-2 outline-none px-2 py-1 rounded">
                    </div>
                    <button type="submit" class="bg-primary w-full px-3 py-1 text-white rounded">
                        {{ $t('images.modal.add') }}
                    </button>
                </form>
        </modal>


        <input class="w-full px-2 py-2 shadow outline-none rounded" type="text" :placeholder="$t('images.img_name')" @input="delaySearch">
        <button class="px-3 py-1 mt-5 bg-primary text-white rounded" @click="openModal = true">{{ $t('images.add_img') }}</button>
        <div class="grid grid-cols-1 md:grid-cols-4 mt-5 gap-5">
            <card v-for="image in imageStore.images.items" :image="image"/>
        </div>
            <div class="w-full flex justify-center mt-3">
                <paginate v-model="pagination.page" :nbPages="Math.ceil(imageStore.images.total / imageStore.images.per_page)" :key="refresh"></paginate>
    </div>
</template>