<template>
  <div></div>
</template>

<script>
export default {
  name: "ImageDetail",
  mounted() {
    console.log(this.$route.params.id);
  },
}
</script>
