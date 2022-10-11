<template>
  <div class="w-full rounded-md overflow-hidden max-h-full shadow-md">
    <div class="font-bold px-3 py-1 text-white uppercase" :class="color">
      <p>{{ header }}</p>
    </div>
    <div class="bg-[#FEFBF6] h-full px-3">
      <slot></slot>
    </div>
  </div>
</template>

<script>
import card from '@/mixins/card.js'


export default {
  name: "CardImage",
  mixins: [card],
  props : {
    color: {
      type: String,
      default: 'bg-[#A6D1E6]',
      require: true
    }
  }
}
</script>

<style scoped>

</style>
