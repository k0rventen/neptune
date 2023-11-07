<script setup>
const props = defineProps({
    modelValue: {
        type: Number,
        required: true
    },
    nbPages: {
        type: Number,
        required: true
    }
})
const emit = defineEmits('update:modelValue')

const nbDisplayedPages = () => {
    if (props.nbPages > 5) {
        return 5
    } else {
        return props.nbPages
    }
}

const setPage = (index) => {
    emit('update:modelValue', index + offset.value)
    if (props.nbPages > 5) {
        if (offset.value + index - 1 > props.nbPages - 5) {
            offset.value = props.nbPages - 5
        } else {
            offset.value = index + offset.value - 1
        }
    }
}

const downgradeOffset = () => {
    if (props.modelValue - 1 > 0) {
        if (offset.value - 1 >= 0) {
            if (props.modelValue - 5 <= props.nbPages - 5) {
                offset.value--
            }
        }
        emit('update:modelValue', props.modelValue - 1)
    }
}

const upgradeOffset = () => {
    if (props.modelValue + 1 <= props.nbPages) {
        if (offset.value + 5 < props.nbPages) {
            offset.value++
        }
        emit('update:modelValue', props.modelValue + 1)
    }
}

const offset = ref(0)
</script>


<template>
    <div class="flex items-center text-black">
        <svg @click="downgradeOffset()" width="25" clip-rule="evenodd" fill-rule="evenodd" stroke-linejoin="round"
            stroke-miterlimit="2" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
            <path
                d="m13.789 7.155c.141-.108.3-.157.456-.157.389 0 .755.306.755.749v8.501c0 .445-.367.75-.755.75-.157 0-.316-.05-.457-.159-1.554-1.203-4.199-3.252-5.498-4.258-.184-.142-.29-.36-.29-.592 0-.23.107-.449.291-.591 1.299-1.002 3.945-3.044 5.498-4.243z" />
        </svg>
        <button v-if="offset > 0" :key="index" class="px-3 py-1">
            ...
        </button>
        <button v-for="index in nbDisplayedPages()" :key="index" class="px-3 py-1"
            :class="{ 'bg-primary rounded-md text-white': index === props.modelValue - offset }" @click="setPage(index)">
            {{ index + offset }}
        </button>
        <button v-if="offset + 5 !== props.nbPage && props.nbPage >= 5" :key="index" class="px-3 py-1">
            ...
        </button>
        <svg @click="upgradeOffset()" width="25" class="rotate-180" clip-rule="evenodd" fill-rule="evenodd"
            stroke-linejoin="round" stroke-miterlimit="2" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
            <path
                d="m13.789 7.155c.141-.108.3-.157.456-.157.389 0 .755.306.755.749v8.501c0 .445-.367.75-.755.75-.157 0-.316-.05-.457-.159-1.554-1.203-4.199-3.252-5.498-4.258-.184-.142-.29-.36-.29-.592 0-.23.107-.449.291-.591 1.299-1.002 3.945-3.044 5.498-4.243z" />
        </svg>
    </div>
</template>