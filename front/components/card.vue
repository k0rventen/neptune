<script setup>
const props = defineProps({
    image: {
        type: Object,
        required: true
    }
})

const selectColor = (vuln, outdated) => {
    if (vuln > 0) {
        return 'bg-red-400'
    }
    if (outdated > 0) {
        return 'bg-yellow-400'
    }
    return 'bg-[#10b981]'
}
</script>

<template>
    <nuxt-link class="w-full h-full rounded p-3 text-light-gray font-light relative overflow-hidden"
        :class="selectColor(props.image.vulnerabilities, props.image.outdated_packages)" :to="`/images/${props.image.sha}`">
        <svg class="absolute opacity-20 right-0 -bottom-8" width="128" height="128" viewBox="0 0 24 24"
            xmlns="http://www.w3.org/2000/svg" fill="white">
            <path
                d="M11.5 23l-8.5-4.535v-3.953l5.4 3.122 3.1-3.406v8.772zm1-.001v-8.806l3.162 3.343 5.338-2.958v3.887l-8.5 4.534zm-10.339-10.125l-2.161-1.244 3-3.302-3-2.823 8.718-4.505 3.215 2.385 3.325-2.385 8.742 4.561-2.995 2.771 2.995 3.443-2.242 1.241v-.001l-5.903 3.27-3.348-3.541 7.416-3.962-7.922-4.372-7.923 4.372 7.422 3.937v.024l-3.297 3.622-5.203-3.008-.16-.092-.679-.393v.002z" />
        </svg>
        <p>{{ $t('images.card.img_name') }}: {{ props.image.image + ':' + props.image.tag }}</p>
        <p>{{ $t('images.card.img_size') }}: {{ useCalcConverter(image.size) }}</p>
        <p>{{ $t('images.card.packages') }}: {{ props.image.packages }}</p>
        <p>{{ $t('images.card.vulnerabilities') }}: {{ props.image.vulnerabilities }}</p>
        <p>{{ $t('images.card.active_vuln') }}: {{ props.image.active_vulnerabilities }}</p>
        <p>{{ $t('images.card.outdated_package') }}: {{ props.image.outdated_packages }}</p>
        <p>{{ $t('images.card.img_add') }}: {{ new Date(props.image.date_added).toLocaleDateString('fr-FR') + ' à ' + new
            Date(props.image.date_added).toLocaleTimeString('fr-FR') }}</p>
    </nuxt-link>
</template>