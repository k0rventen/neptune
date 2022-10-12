<template>
  <div>
    <navbar
      :elements="[
      { name: $t('navbar.home'), route: '/' },
      { name: $t('navbar.images'), route: '/images' },
      { name: $t('navbar.vulnerabilities'), route: '/vulnerabilities' },
      { name: $t('navbar.dependencies'), route: '/dependencies' }
      ]"
    />
    <Nuxt />
  </div>

</template>

<script>
export default {
  name: "DefaultLayout"
}
</script>
