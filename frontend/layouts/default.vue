<template>
  <div class="bg-primary w-full h-screen overflow-hidden lg:flex">
    <Navbar class="lg:hidden" 
    :elements="[
      { name: $t('navbar.dashboard'), route: '/' },
      { name: $t('navbar.images'), route: '/images' },
      { name: $t('navbar.vulnerabilities'), route: '/vulnerabilities' },
      { name: $t('navbar.dependencies'), route: '/dependencies' },
      { name: $t('navbar.registry'), route: '/registry'}
    ]"
    />
    <div class="w-1/5 bg-red-600 h-screen hidden lg:block">
      <Sidebar :elements="[
      { name: $t('navbar.dashboard'), route: '/' },
      { name: $t('navbar.images'), route: '/images' },
      { name: $t('navbar.vulnerabilities'), route: '/vulnerabilities' },
      { name: $t('navbar.dependencies'), route: '/dependencies' },
      { name: $t('navbar.registry'), route: '/registry'}
      ]"/>
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
