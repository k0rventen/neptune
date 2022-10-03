<template>
  <button class="px-3 text-center py-1 rounded-md text-white bg-red-600" :type="type" :disabled="disabled">
    <slot />
  </button>
</template>

<script>
export default {
  name: "ButtonClassique",
  props: {
    type: {
      type: String,
      default: "button"
    },
    disabled: {
      type: Boolean,
    },
    color: {
      type: String,
      default: "primary"
    }
  }
}
</script>
