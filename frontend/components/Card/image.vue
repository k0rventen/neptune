<template>
  <div class="w-full rounded-md overflow-hidden max-h-full">
    <div class="font-bold px-3 py-1 text-white uppercase" :class="`bg-${color}`">
      <p>{{ header }}</p>
    </div>
    <div class="bg-[#FEFBF6] h-full">

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
      default: '#A6D1E6'
    }
  }
}
</script>

<style scoped>

</style>
