<template>
  <div class="w-full h-full bg-white shadow-md flex flex-col px-8 relative justify-between py-3">
    <div>
      <div class="w-full flex justify-center items-center h-24">
        <img class="w-12 h-12" src="@/assets/img/logo.png" alt="" />
        <p class="ml-2 text-2xl">Neptune</p>
      </div>
      <hr
        class="h-[1px] border-none bg-gradient-to-r from-transparent via-secondary to-transparent"
      />
      <div class="flex flex-col gap-2 mt-5">
        <div
          v-for="route in elements"
          :key="route.name"
          class="cursor-pointer group bg-white hover:drop-shadow-xl w-full flex items-center hover:font-bold text-secondary gap-3 py-3 px-3 rounded-lg"
          @click="$router.push(route.route)"
        >
          <div class="px-3 py-3 bg-white shadow-md rounded-md">
            <svg
              v-if="route.name === $t('navbar.dashboard')"
              class="fill-current"
              clip-rule="evenodd"
              fill-rule="evenodd"
              stroke-linejoin="round"
              stroke-miterlimit="2"
              viewBox="0 0 24 24"
              xmlns="http://www.w3.org/2000/svg"
              width="12"
              height="12"
            >
              <path
                d="m11.6 11c0-.552-.448-1-1-1-1.655 0-4.945 0-6.6 0-.552 0-1 .448-1 1v9c0 .552.448 1 1 1h6.6c.552 0 1-.448 1-1 0-2.092 0-6.908 0-9zm9.4 6c0-.552-.448-1-1-1h-6c-.538 0-1 .477-1 1v3c0 .552.448 1 1 1h6c.552 0 1-.448 1-1zm0-13c0-.552-.448-1-1-1-1.537 0-4.463 0-6 0-.552 0-1 .448-1 1v9.6c0 .552.448 1 1 1h6c.552 0 1-.448 1-1 0-2.194 0-7.406 0-9.6zm-9.4 0c0-.552-.448-1-1-1-1.655 0-4.945 0-6.6 0-.552 0-1 .448-1 1v3.6c0 .552.448 1 1 1h6.6c.552 0 1-.448 1-1 0-1.017 0-2.583 0-3.6z"
                fill-rule="nonzero"
              />
            </svg>
            <svg
              v-if="route.name === $t('navbar.images')"
              class="fill-current"
              width="12"
              height="12"
              viewBox="0 0 24 24"
              xmlns="http://www.w3.org/2000/svg"
              fill="white"
            >
              <path
                d="M11.5 23l-8.5-4.535v-3.953l5.4 3.122 3.1-3.406v8.772zm1-.001v-8.806l3.162 3.343 5.338-2.958v3.887l-8.5 4.534zm-10.339-10.125l-2.161-1.244 3-3.302-3-2.823 8.718-4.505 3.215 2.385 3.325-2.385 8.742 4.561-2.995 2.771 2.995 3.443-2.242 1.241v-.001l-5.903 3.27-3.348-3.541 7.416-3.962-7.922-4.372-7.923 4.372 7.422 3.937v.024l-3.297 3.622-5.203-3.008-.16-.092-.679-.393v.002z"
              />
            </svg>
            <svg
              v-if="route.name === $t('navbar.vulnerabilities')"
              class="fill-current"
              enable-background="new 0 0 274.989 274.989"
              version="1.1"
              viewBox="0 0 274.99 274.99"
              width="12"
              height="12"
            >
              <path
                d="m179.57 216.04c-5.609 11.237-8.425 16.844-14.02 19.641-5.609 5.603-16.837 5.603-28.068 5.603-14.02 0-22.432 0-28.038-5.603-5.624-2.797-8.432-8.404-14.03-19.641 0 0-2.816-2.781-2.816-5.611l-11.228 2.83 8.429 28.025 16.827 14.049c5.598 14.022 16.835 19.652 30.855 19.652 5.609 0 14.039-2.836 16.835-5.63 5.623-2.816 11.232-8.415 14.04-14.022l16.826-14.049 8.425-28.025-11.222-2.83c-2.815 2.83-2.815 5.611-2.815 5.611zm30.891-190.78c-19.664-16.818-42.103-25.266-72.978-25.266-30.855 0-53.295 8.448-72.948 25.266-16.831 14.021-28.039 36.463-28.039 61.743 0 22.422 2.787 39.249 8.4 47.7 8.426 14.008 14.04 22.428 14.04 28.032l2.797 22.43 39.28 19.663 8.432 16.84c2.782 0 5.607 0 11.222 2.797h16.817c14.039 0 22.459-2.797 30.875-2.797l5.603-16.84 39.291-19.663 2.796-22.43c2.818-5.604 2.818-8.426 2.818-11.216 14.018-19.648 19.633-42.094 19.633-64.517-1e-3 -25.279-8.411-47.721-28.039-61.742zm-115.05 137.48c-16.845 0-22.44-11.216-22.44-28.032 0-8.451 0-16.867 5.595-19.652 2.802-5.626 8.434-8.415 16.845-8.415 16.812 0 25.252 8.415 25.252 25.237 0 19.646-8.44 30.862-25.252 30.862zm50.509 30.855c-2.831 0-5.633 0-8.44-2.806-2.817 2.806-2.817 2.806-5.595 2.806-2.836 0-5.609 0-8.425-2.806-2.797 0-2.797-2.791-2.797-5.618 0-2.776 2.797-8.387 5.613-11.198 5.609-5.621 8.387-11.232 11.204-16.837 2.807 5.604 8.44 11.216 11.231 16.837 5.604 2.811 5.604 8.422 5.604 11.198 0 5.618-2.797 8.424-8.395 8.424zm36.464-30.855c-16.837 0-25.263-11.216-25.263-28.032 0-16.867 8.426-28.068 25.263-28.068 8.409 0 14.018 2.79 16.826 8.415 5.613 2.785 5.613 8.411 5.613 16.821-1e-3 19.648-8.421 30.864-22.439 30.864z"
              />
            </svg>
            <svg
              v-if="route.name === $t('navbar.registry')"
              class="fill-current"
              width="12"
              height="12"
              viewBox="0 0 24 24"
              fill="white"
            >
              <path
                d="M18 10.031v-6.423l-6.036-3.608-5.964 3.569v6.499l-6 3.224v7.216l6.136 3.492 5.864-3.393 5.864 3.393 6.136-3.492v-7.177l-6-3.3zm-1.143.036l-4.321 2.384v-4.956l4.321-2.539v5.111zm-4.895-8.71l4.272 2.596-4.268 2.509-4.176-2.554 4.172-2.551zm-10.172 12.274l4.778-2.53 4.237 2.417-4.668 2.667-4.347-2.554zm4.917 3.587l4.722-2.697v5.056l-4.722 2.757v-5.116zm6.512-3.746l4.247-2.39 4.769 2.594-4.367 2.509-4.649-2.713zm9.638 6.323l-4.421 2.539v-5.116l4.421-2.538v5.115z"
              />
            </svg>
            <svg
              v-if="route.name === $t('navbar.dependencies')"
              class="fill-current"
              xmlns="http://www.w3.org/2000/svg"
              width="12"
              height="12"
              viewBox="0 0 24 24"
            >
              <path
                d="M21.586 10.461l-10.05 10.075c-1.95 1.949-5.122 1.949-7.071 0s-1.95-5.122 0-7.072l10.628-10.585c1.17-1.17 3.073-1.17 4.243 0 1.169 1.17 1.17 3.072 0 4.242l-8.507 8.464c-.39.39-1.024.39-1.414 0s-.39-1.024 0-1.414l7.093-7.05-1.415-1.414-7.093 7.049c-1.172 1.172-1.171 3.073 0 4.244s3.071 1.171 4.242 0l8.507-8.464c.977-.977 1.464-2.256 1.464-3.536 0-2.769-2.246-4.999-5-4.999-1.28 0-2.559.488-3.536 1.465l-10.627 10.583c-1.366 1.368-2.05 3.159-2.05 4.951 0 3.863 3.13 7 7 7 1.792 0 3.583-.684 4.95-2.05l10.05-10.075-1.414-1.414z"
              />
            </svg>
          </div>
          <p>{{ route.name.toUpperCase() }}</p>
        </div>
      </div>
    </div>
    <div>
      
      <select class="w-full border-current border-3 border-gray-400 px-3 py-2 outline-none border rounded-md bg-transparent" v-model="langage">
        <option v-for="locale in availableLocales" :value="locale.code" :key="locale.code">
          {{ locale.name }}
        </option>
      </select>
    </div>
  </div>
</template>

<script>
export default {
  name: 'SidebarComponent',
  props: {
    elements: {
      type: Array,
      default: () => [],
    },
  },
  watch: {
    langage (val) {
      this.$i18n.locale = val
    }
  },
  computed: {
    availableLocales () {
      return this.$i18n.locales
    }
  },
  data() {
    return {
      langage: this.$i18n.locale
    }
  }
}
</script>

<style scoped></style>
