<template>
  <div class="shadow px-5 py-5 bg-white text-black">
    <div class="w-full flex justify-between items-center">
      <NuxtLink to="/">
        <div class="flex items-center gap-3">
          <img src="~/assets/img/logo.png" alt="logo" class="w-10 h-10" />
          <p class="text-2xl">Neptune</p>
        </div>
      </NuxtLink>
      <div class="px-3 py-3" @click="openNav = !openNav">
        <svg
          width="25px"
          clip-rule="evenodd"
          fill-rule="evenodd"
          stroke-linejoin="round"
          stroke-miterlimit="2"
          viewBox="0 0 24 24"
          xmlns="http://www.w3.org/2000/svg"
        >
          <path
            d="m21 15.75c0-.414-.336-.75-.75-.75h-16.5c-.414 0-.75.336-.75.75s.336.75.75.75h16.5c.414 0 .75-.336.75-.75zm0-4c0-.414-.336-.75-.75-.75h-16.5c-.414 0-.75.336-.75.75s.336.75.75.75h16.5c.414 0 .75-.336.75-.75zm0-4c0-.414-.336-.75-.75-.75h-16.5c-.414 0-.75.336-.75.75s.336.75.75.75h16.5c.414 0 .75-.336.75-.75z"
            fill-rule="nonzero"
          />
        </svg>
      </div>
    </div>
    <div class="w-full" v-if="openNav">
      <p
        v-for="item in elements"
        :key="item.name"
        class="py-3 w-full"
        @click="
          $router.push(item.route)
          openNav = false
        "
      >
        {{ item.name }}
      </p>
      <select
        class="w-full border-current border-3 border-gray-400 px-3 py-2 outline-none border rounded-md bg-transparent"
        v-model="langage"
      >
        <option
          v-for="locale in availableLocales"
          :value="locale.code"
          :key="locale.code"
        >
          {{ locale.name }}
        </option>
      </select>
    </div>
  </div>
</template>

<script>
export default {
  name: 'NavbarComponent',
  props: {
    elements: {
      type: Array,
      default: () => [],
    },
  },
  watch: {
    langage(val) {
      this.$i18n.locale = val
    },
  },
  data() {
    return {
      openNav: false,
      langage: this.$i18n.locale,
    }
  },
  computed: {
    availableLocales() {
      return this.$i18n.locales
    },
  },
}
</script>
