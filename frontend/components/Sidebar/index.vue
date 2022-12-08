<template>
  <div class="w-full h-full bg-white shadow-md flex flex-col px-8">
    <div class="w-full flex justify-center items-center h-24">
      <img class="w-12 h-12" src="@/assets/img/logo.png" alt="">
      <p class="ml-2 text-2xl">Neptune</p>
    </div>
    <hr class="h-[1px] border-none bg-gradient-to-r from-transparent via-secondary to-transparent">
    <div class="flex flex-col gap-2 mt-5">
      <div v-for="route in elements" :key="route.name" class="hover:bg-white w-full flex items-center hover:font-bold text-secondary gap-3 py-3 px-3 rounded-lg group hover:drop-shadow-md transition ease-in hover:-translate-y-1" @click="$router.push(route.route)">
        <div class="px-3 py-3 group-hover:bg-neptune-blue bg-white shadow-md rounded-md">
          <svg class="fill-current" width="12" height="12" viewBox="0 0 24 24"><path d="M24 24H0v-2h1C3.996 17.096 4.945 9.015 5 6h7c.054 2.94 1.005 10.982 4 16h1.742l-.642-1.093c-1.195-2.145-1.948-4.546-2.501-6.924.268-1.659.385-3.106.401-3.983h5c.04 2.205.753 8.236 3 12h1v2zM5.713 18h2l-1.167 3 4.167-5h-2l1.167-3-4.167 5zM18.637 5.085c.238-.522.759-.885 1.363-.885s1.125.363 1.363.885c.154-.08.328-.125.512-.125.621 0 1.125.511 1.125 1.14 0 .629-.504 1.14-1.125 1.14-.184 0-.358-.045-.512-.125C21.125 7.637 20.604 8 20 8s-1.125-.363-1.363-.885c-.154.08-.328.125-.512.125A1.133 1.133 0 0 1 17 6.1c0-.629.504-1.14 1.125-1.14.184 0 .358.045.512.125zM8 5c.198-2.182 1.785-4 3.5-4 .246 0 .478.059.683.164a2 2 0 0 1 3.634 0 1.5 1.5 0 1 1 0 2.672A2 2 0 0 1 14 5c-2.345 0-3.722-2.951-5 0H8z"/></svg>
        </div>
        <p>{{ route.name.toUpperCase() }}</p>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "SidebarComponent",
  props: {
    elements: {
      type: Array,
      default: () => []
    }
  }
}
</script>

<style scoped>

</style>
