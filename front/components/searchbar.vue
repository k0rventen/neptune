<script setup lang="ts">
const emit = defineEmits(["input"]);
</script>
<template>
  <div
    class="w-full flex bg-[#1b1c1e] px-3 py-2 gap-3 overflow-y-auto rounded border border-white/15 border"
  >
    <Icon
      name="ph:magnifying-glass-duotone"
      color="white"
      size="24"
      class="opacity-75 cursor-pointer"
    />
    <input
      class="bg-transparent w-full outline-none text-white"
      placeholder="Image name..."
      @input="(event) => emit('input', event?.target?.value)"
    />
  </div>
</template>
