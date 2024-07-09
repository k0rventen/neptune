<script setup></script>

<template>
  <div class="min-h-screen bg-[#202124] flex relative">
    <div class="noise absolute opacity-25 w-full h-full z-0" />
    <Sidebar />
    <slot />
  </div>
</template>

<style scoped>
.noise {
  background-image: url("/public/noise-light.png");
}
</style>
