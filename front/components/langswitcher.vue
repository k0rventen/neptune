<script setup>
const { locales, locale, setLocale } = useI18n()

const language = computed({
    get: () => locale.value,
    set: (value) => {
        setLocale(value)
    }
})

</script>

<template>
    <select v-model="language">
        <option v-for="lang in locales">
            {{ lang }}
        </option>
    </select>
</template>