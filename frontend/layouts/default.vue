<template>
  <div class="bg-primary w-full h-screen overflow-hidden flex">
    <div class="w-1/5 bg-red-600 h-screen">
      <Sidebar :elements="[
      { name: $t('navbar.home'), route: '/' },
      { name: $t('navbar.images'), route: '/images' },
      { name: $t('navbar.vulnerabilities'), route: '/vulnerabilities' },
      { name: $t('navbar.dependencies'), route: '/dependencies' }
      ]" />
    </div>
    <div class="w-full">
      <Nuxt />
    </div>
  </div>

</template>

<script>
export default {
  name: "DefaultLayout"
}
</script>
