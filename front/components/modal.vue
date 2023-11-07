<script setup>
defineProps(['modelValue'])
const emit = defineEmits(['update:modelValue'])

const modal = ref()

const handleMouseout = (event) => {
    if (modal.value && !modal.value.contains(event.target)) {
        emit('update:modelValue', false)
    }
}

window.addEventListener('mousedown', handleMouseout)
</script>

<template>
    <Transition>
        <div v-if="modelValue"
            class="bg-black/25 backdrop-blur fixed top-0 left-0 w-full h-full z-20 flex justify-center items-center">
            <div ref="modal" class="bg-white p-3 min-h-[50vmin] min-w-[50vmax] rounded">
                <slot name="header"/>
                <hr class="mt-1">
                <slot />
            </div>
        </div>
    </Transition>
</template>

<style scoped>
.v-enter-active,
.v-leave-active {
    transition: opacity 0.5s ease;
}

.v-enter-from,
.v-leave-to {
    opacity: 0;
}
</style>