<script setup>
import { useRegistryStore } from '@/store/registry.store'

const registryStore = useRegistryStore()

await registryStore.getRegistries()

const registries = ref({
    url: undefined,
    username: undefined,
    password: undefined
})

const sendRegistry = async () => {
    await registryStore.sendRegistry(registries.value).then(() => {
        registries.value = {
            registry: undefined,
            user: undefined,
            password: undefined
        }
    })
}
</script>

<template>
    <div class="h-2/3 bg-white border rounded-md">
        <div class="grid grid-cols-3 gap-5 p-3">
            <div v-for="registry in registryStore.registries" :key="registry.url"
                class="text-white px-5 rounded-lg py-5 overflow-hidden cursor-pointer bg-primary relative">
                <svg class="absolute opacity-20 -right-5 -bottom-5" width="116" height="116" viewBox="0 0 24 24"
                    fill="white">
                    <path
                        d="M18 10.031v-6.423l-6.036-3.608-5.964 3.569v6.499l-6 3.224v7.216l6.136 3.492 5.864-3.393 5.864 3.393 6.136-3.492v-7.177l-6-3.3zm-1.143.036l-4.321 2.384v-4.956l4.321-2.539v5.111zm-4.895-8.71l4.272 2.596-4.268 2.509-4.176-2.554 4.172-2.551zm-10.172 12.274l4.778-2.53 4.237 2.417-4.668 2.667-4.347-2.554zm4.917 3.587l4.722-2.697v5.056l-4.722 2.757v-5.116zm6.512-3.746l4.247-2.39 4.769 2.594-4.367 2.509-4.649-2.713zm9.638 6.323l-4.421 2.539v-5.116l4.421-2.538v5.115z" />
                </svg>
                <p class="truncate">{{ $t('registry.url') }} : {{ registry.registry }}</p>
                <p class="truncate">{{ $t('registry.username') }} : {{ registry.user }}</p>
                <p class="truncate">{{ $t('registry.password') }} : {{ registry.password }}</p>
            </div>
        </div>
    </div>
    <div class="mt-3">
        <form class="gap-3" @submit.prevent="sendRegistry">
            <label class="block">{{ $t('registry.url') }} :</label>
            <input v-model="registries.registry" type="text" class="border-b-1 border outline-none px-2 py-1 rounded">

            <label class="block">{{ $t('registry.username') }} :</label>
            <input v-model="registries.user" type="text" class="border-b-1 border outline-none px-2 py-1 rounded">

            <label class="block">{{ $t('registry.password') }} :</label>
            <input v-model="registries.password" type="password" class="border-b-1 border outline-none px-2 py-1 rounded block">

            <button type="submit" class="bg-primary w-fit px-3 py-1 mt-1 text-white rounded">{{ $t('registry.added') }} !</button>
        </form>



    </div>
</template>