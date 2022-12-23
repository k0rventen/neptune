<template>
  <div
    class="w-full px-5 py-5 pb-28 lg:pb-5 text-white h-screen scrollbar-thin overflow-auto"
  >
    <Modal
      v-if="openImagesModal"
      v-model="openImagesModal"
      title="Ajout d'une image en direct"
      class="text-gray-500"
    >
      <label for="" class="my-2 gap-3 block">
        Nom de l'image :
        <input
          v-model="imageName"
          type="text"
          class="rounded-md border border-gray-400 outline-none px-2 py-1"
        />
      </label>
      <template #footer>
        <button
          class="px-3 py-1 rounded-md bg-neptune-blue text-white"
          @click="sendNewImage()"
        >
          Envoyer
        </button>
      </template>
    </Modal>
    <div class="text-gray-400">
      <div class="relative mb-2">
        <input
          v-model="search"
          type="text"
          class="w-full px-6 py-3 rounded-full shadow-md outline-none"
          placeholder="Rechercher ..."
        />
        <svg
          class="absolute right-4 top-1/4 opacity-20"
          width="26"
          height="26"
          clip-rule="evenodd"
          fill-rule="evenodd"
          stroke-linejoin="round"
          stroke-miterlimit="2"
          viewBox="0 0 24 24"
          xmlns="http://www.w3.org/2000/svg"
          @click="openFilter = !openFilter"
        >
          <path
            d="m15.344 17.778c0-.414-.336-.75-.75-.75h-5.16c-.414 0-.75.336-.75.75s.336.75.75.75h5.16c.414 0 .75-.336.75-.75zm2.206-4c0-.414-.336-.75-.75-.75h-9.596c-.414 0-.75.336-.75.75s.336.75.75.75h9.596c.414 0 .75-.336.75-.75zm2.45-4c0-.414-.336-.75-.75-.75h-14.5c-.414 0-.75.336-.75.75s.336.75.75.75h14.5c.414 0 .75-.336.75-.75zm2-4c0-.414-.336-.75-.75-.75h-18.5c-.414 0-.75.336-.75.75s.336.75.75.75h18.5c.414 0 .75-.336.75-.75z"
            fill-rule="nonzero"
          />
        </svg>
      </div>
      <button class="bg-neptune-blue text-white px-3 py-1 rounded-md mb-2" @click="openImagesModal = true">
        Ajouter une image
      </button>

      <div v-if="openFilter" class="w-full flex gap-3">
        <div class="w-1/6">
          <label for="trie" class="block"> Trier par : </label>
          <select
            id="trie"
            v-model="selectedFilter"
            class="w-full px-3 py-1 rounded-md mb-2 shadow-md"
            placeholder="Trier par"
          >
            <option value="0">Aucun</option>
            <option value="1">Vulnerabilités</option>
            <option value="2">Outdated</option>
            <option value="3">Taille</option>
            <option value="4">Sévérité</option>
            <option value="5">Vulnérabilités actives</option>
          </select>
        </div>

        <div
          v-if="selectedFilter !== '0' && selectedFilter !== undefined"
          class="w-1/6"
        >
          <label for="sorting" class="block"> Ordre : </label>
          <select
            id="sorting"
            v-model="selectedOrder"
            class="w-full px-3 py-1 rounded-md mb-2 shadow-md"
            placeholder="ASC"
            @change="() => (value = value.reverse())"
          >
            <option value="ASC">ASC</option>
            <option value="DESC">DESC</option>
          </select>
        </div>
      </div>
    </div>
    <div class="w-full grid grid-cols-3 gap-3 lg:gap-9">
      <div
        v-for="(tag, index) in value"
        :key="index"
        class="col-span-3 md:col-span-1 w-full cursor-pointer shadow-md bg-neptune-blue px-5 rounded-lg py-5 relative overflow-hidden"
        :class="selectColor(tag.vulnerabilities, tag.outdated_packages)"
        @click="$router.push({ path: '/images/' + tag.sha })"
      >
        <svg
          class="absolute opacity-20 right-0 -bottom-8"
          width="128"
          height="128"
          viewBox="0 0 24 24"
          xmlns="http://www.w3.org/2000/svg"
          fill="white"
        >
          <path
            d="M11.5 23l-8.5-4.535v-3.953l5.4 3.122 3.1-3.406v8.772zm1-.001v-8.806l3.162 3.343 5.338-2.958v3.887l-8.5 4.534zm-10.339-10.125l-2.161-1.244 3-3.302-3-2.823 8.718-4.505 3.215 2.385 3.325-2.385 8.742 4.561-2.995 2.771 2.995 3.443-2.242 1.241v-.001l-5.903 3.27-3.348-3.541 7.416-3.962-7.922-4.372-7.923 4.372 7.422 3.937v.024l-3.297 3.622-5.203-3.008-.16-.092-.679-.393v.002z"
          />
        </svg>
        <p>Nom de l'image : {{ tag.image + ':' + tag.tag }}</p>
        <p>Taille de l'image : {{ calcSize(tag.size) }}</p>
        <p>Paquets : {{ tag.packages }}</p>
        <p>Vulnérabilité(s) : {{ tag.vulnerabilities }}</p>
        <p>Vulnérabilité(s) active : {{ tag.active_vulnerabilities }}</p>
        <p>Paquet obsolète : {{ tag.outdated_packages }}</p>
      </div>
    </div>
  </div>
</template>

<script>
import { mapActions, mapState } from 'vuex'
import calcSize from '@/mixins/sizeCalc.js'

export default {
  name: 'ImagesPage',
  mixins: [calcSize],
  data() {
    return {
      value: undefined,
      imageToScan: undefined,
      search: undefined,
      openImagesModal: false,
      isLoading: true,
      selectedFilter: '0',
      backupTags: undefined,
      selectedOrder: 'ASC',
      openFilter: false,
    }
  },
  computed: {
    ...mapState('image', ['images', 'tags']),
  },
  watch: {
    search(newValue) {
      if (newValue === '') {
        this.value = this.tags
      } else {
        this.value = this.tags.filter((el) => {
          const fullname = el.image + ':' + el.tag
          return fullname.toLowerCase().includes(newValue.toLowerCase())
        })
      }
    },
    selectedFilter(newValue) {
      this.selectedOrder = 'ASC'
      if (newValue === '0') {
        this.value = this.tags
      } else if (newValue === '1') {
        this.value = this.backupTags.sort((a, b) =>
          a.vulnerabilities > b.vulnerabilities
            ? 1
            : b.vulnerabilities > a.vulnerabilities
            ? -1
            : 0
        )
      } else if (newValue === '2') {
        this.value = this.backupTags.sort((a, b) =>
          a.outdated_packages > b.outdated_packages
            ? 1
            : b.outdated_packages > a.outdated_packages
            ? -1
            : 0
        )
      } else if (newValue === '3') {
        this.value = this.backupTags.sort((a, b) =>
          a.size > b.size ? 1 : b.size > a.size ? -1 : 0
        )
      } else if (newValue === '4') {
        this.value = this.backupTags.sort((a, b) => {
          if (a.vulnerabilities > 0) {
            return 1
          } else if (b.vulnerabilities > 0) {
            return -1
          }

          if (a.outdated_packages > 0) {
            return 1
          } else if (b.outdated_packages > 0) {
            return -1
          } else {
            return 0
          }
        })
      } else if (newValue === '5') {
        this.value = this.backupTags.sort((a, b) =>
          a.active_vulnerabilities > b.active_vulnerabilities
            ? 1
            : b.active_vulnerabilities > a.active_vulnerabilities
            ? -1
            : 0
        )
      }
    },
  },
  async mounted() {
    await this.getTags()
      .then(() => {
        this.value = this.tags
        this.backupTags = [...this.tags]
      })
      .finally(() => {
        this.isLoading = false
      })
  },
  methods: {
    ...mapActions('image', ['scanImages']),
    ...mapActions('image', ['getImages', 'getTags']),
    async sendImage() {
      await this.scanImages(this.imageToScan).then(() => {
        this.imageToScan = undefined
      })
    },
    selectColor(vuln, outdated) {
      if (vuln > 0) {
        return 'bg-red-400'
      }
      if (outdated > 0) {
        return 'bg-yellow-400'
      }
      return 'bg-green-500'
    },
    async sendNewImage() {
      this.isLoading = true
      this.openImagesModal = false
      await this.scanImages({image: this.imageName, return_error: false}).then(() => {
        this.imageName = undefined
        this.isLoading = false
      })
    }
  },
}
</script>
