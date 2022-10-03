<template>
  <div>
    <navbar
      :elements="[
      { name: $t('navbar.home'), route: '/' },
      { name: $t('navbar.images'), route: '/images' }
      ]
    "/>
    <Nuxt />
  </div>

</template>

<script>
export default {
  name: "DefaultLayout"
}
</script>
