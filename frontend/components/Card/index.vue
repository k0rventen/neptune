<template>
  <div class="w-full rounded-md overflow-hidden max-h-full">
    <div class="bg-[#A6D1E6] font-bold px-3 py-1 text-white uppercase">
      <p>{{ header }}</p>
    </div>
    <div class="bg-[#FEFBF6] h-full">
      <slot />
    </div>
  </div>
</template>

<script>
import card from '@/mixins/card.js'

export default {
  name: "CardComponent",
  mixins: [card]
}
</script>
