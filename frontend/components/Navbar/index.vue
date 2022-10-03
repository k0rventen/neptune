<template>
  <div class="w-full flex justify-between items-center shadow px-5 bg-[#A6D1E6] text-white">
    <p class="font-bold font-clash text-2xl">Neptune</p>
    <div class="flex items-center">
      <button v-for="element in elements" :key="element.name" class="font-bold py-5 px-3 hover:bg-[#88adbf]" @click="$router.push(element.route)">
        {{ element.name }}
      </button>
    </div>
  </div>
</template>

<script>
export default {
  name: "NavbarComponent",
  props: {
    elements: {
      type: Array,
      default: () => []
    }
  }
}
</script>
