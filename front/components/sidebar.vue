<script setup>
const localPath = useLocalePath()

const isOpen = ref(false)
const openSidebar = (state) => {
    isOpen.value = state
}
</script>

<template>
    <div class="h-full w-16 px-2 py-2 bg-white shadow-md transition-all ease-in overflow-x-hidden flex flex-col justify-between"
        :class="{ 'w-72': isOpen }" @mouseenter="openSidebar(true)" @mouseleave="openSidebar(false)">
        <div>
            <div class="w-full flex justify-center">
                <img class="w-10" src="@/assets/img/logo.png" alt="neptune">
            </div>
            <hr class="mt-4">
            <div class="w-full mt-3 flex flex-col gap-3">
            </div>
            <nuxt-link class="flex flex-nowrap grow items-center gap-3 py-2" :to="localPath('/')">
                <img class="ml-3" src="@/assets/img/dashboard.svg" alt="">
                <p class="transition-all ease-in whitespace-nowrap" :class="isOpen ? 'opacity-100' : 'opacity-0'">{{
                    $t('sidebar.dashboard')
                }}</p>
            </nuxt-link>
            <nuxt-link class="flex flex-nowrap grow items-center gap-3 py-2" :to="localPath('/images')">
                <img class="ml-3" src="@/assets/img/box.svg" alt="">
                <p class="transition-all ease-in whitespace-nowrap" :class="isOpen ? 'opacity-100' : 'opacity-0'">{{
                    $t('sidebar.images') }}
                </p>
            </nuxt-link>
            <nuxt-link class="flex flex-nowrap grow items-center gap-3 py-2" :to="localPath('/vulnerabilities')">
                <img class="ml-3" src="@/assets/img/vulnerability.svg" alt="">
                <p class="transition-all ease-in whitespace-nowrap" :class="isOpen ? 'opacity-100' : 'opacity-0'">{{
                    $t('sidebar.vulnerabilities') }}</p>
            </nuxt-link>
            <nuxt-link class="flex flex-nowrap grow items-center gap-3 py-2" :to="localPath('/dependencies')">
                <img class="ml-3" src="@/assets/img/paperclip.svg" alt="">
                <p class="transition-all ease-in whitespace-nowrap" :class="isOpen ? 'opacity-100' : 'opacity-0'">{{
                    $t('sidebar.dependencies') }}</p>
            </nuxt-link>
            <nuxt-link class="flex flex-nowrap grow items-center gap-3 py-2" :to="localPath('/registry')">
                <img class="ml-3" src="@/assets/img/inbox.svg" alt="">
                <p class="transition-all ease-in whitespace-nowrap" :class="isOpen ? 'opacity-100' : 'opacity-0'">{{
                    $t('sidebar.registry') }}
                </p>
            </nuxt-link>
            <nuxt-link class="flex flex-nowrap grow items-center gap-3 py-2" :to="localPath('/new-vuln')">
                <img class="ml-3" src="@/assets/img/new.svg" alt="">
                <p class="transition-all ease-in whitespace-nowrap" :class="isOpen ? 'opacity-100' : 'opacity-0'">{{
                    $t('sidebar.new_vuln') }}</p>
            </nuxt-link>
        </div>
        <langswitcher />
    </div>
</template>