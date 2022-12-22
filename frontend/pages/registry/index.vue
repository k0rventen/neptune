<template>
  <div class="lg:h-screen px-5 py-3">
    <div class="h-2/3 px-3 py-3 border border-gray-300 my-2 rounded-xl overflow-x-scroll scrollbar-thin bg-white">
      <div class="grid grid-cols-3 gap-5">
        <div
          v-for="registry in registries"
          :key="registry.url"
          class="text-white px-5 rounded-lg py-5 overflow-hidden cursor-pointer bg-neptune-blue relative"
        >
          <svg
            class="absolute opacity-20 -right-5 -bottom-5"
            width="116"
            height="116"
            viewBox="0 0 24 24"
            fill="white"
          >
            <path
              d="M18 10.031v-6.423l-6.036-3.608-5.964 3.569v6.499l-6 3.224v7.216l6.136 3.492 5.864-3.393 5.864 3.393 6.136-3.492v-7.177l-6-3.3zm-1.143.036l-4.321 2.384v-4.956l4.321-2.539v5.111zm-4.895-8.71l4.272 2.596-4.268 2.509-4.176-2.554 4.172-2.551zm-10.172 12.274l4.778-2.53 4.237 2.417-4.668 2.667-4.347-2.554zm4.917 3.587l4.722-2.697v5.056l-4.722 2.757v-5.116zm6.512-3.746l4.247-2.39 4.769 2.594-4.367 2.509-4.649-2.713zm9.638 6.323l-4.421 2.539v-5.116l4.421-2.538v5.115z"
            />
          </svg>
          <p class="truncate">URL : {{ registry.registry }}</p>
          <p class="truncate">Utilisateur : {{ registry.user }}</p>
          <p class="truncate">Mot de passe : {{ registry.password }}</p>
        </div>
      </div>
    </div>
          <div class="h-1/3 px-3 py-3">
        <form @submit.prevent="sendRegisteriesData()">
          <label class="mb-2 gap-3">
            URL :
            <input
              v-model="registry.registry"
              type="text"
              class="rounded-md border border-gray-400 outline-none px-2 py-1"
            />
          </label>

          <label for="" class="my-2 gap-3 block">
            Nom d'utilisateur :
            <input
              v-model="registry.user"
              type="text"
              class="rounded-md border border-gray-400 outline-none px-2 py-1"
            />
          </label>

          <label for="" class="mb-2 gap-3 block">
            Mot de passe
            <input
              v-model="registry.password"
              type="password"
              class="rounded-md border border-gray-400 outline-none px-2 py-1"
            />
          </label>
          <button
            type="submit"
            class="px-3 py-1 rounded-md bg-neptune-blue text-white"
          >
            Envoyer
          </button>
        </form>
      </div>
  </div>
</template>

<script>
import { mapState, mapActions } from 'vuex'

export default {
  name: 'RegistryPage',
  data() {
    return {
      registry: {
        registry: undefined,
        user: undefined,
        password: undefined,
      }
    }
  },
  computed: {
    ...mapState('registries', ['registries']),
  },
  methods: {
    ...mapActions('registries', ['getRegistries', 'sendRegistry']),
    async sendRegisteriesData() {
      await this.sendRegistry(this.registry)
      this.registry = {
        registry: '',
        user: '',
        password: '',
      }
    },
  },
  async mounted() {
    await this.getRegistries()
  },
}
</script>
