<template>
  <div
    class="w-full px-5 py-5 pb-28 lg:pb-5 text-white h-screen scrollbar-thin overflow-auto"
  >
    <Modal
      v-if="openImagesModal"
      v-model="openImagesModal"
      :title="$t('images.modal.add_image_directly')"
      class="text-gray-500"
    >
      <label for="" class="my-2 gap-3 block">
        {{$t('images.image_name')}} :
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
          {{$t('images.send')}}
        </button>
      </template>
    </Modal>
    <div class="text-gray-400">
      <div class="relative mb-2">
        <input
          v-model="filter.name_filter"
          type="text"
          class="w-full px-6 py-3 rounded-full shadow-md outline-none"
          :placeholder="$t('images.search')"
        />
      </div>
      <button class="bg-neptune-blue text-white px-3 py-1 rounded-md mb-2" @click="openImagesModal = true">
       {{ $t('images.add_image') }}
      </button>
    </div>
    <div class="w-full grid grid-cols-3 gap-3 lg:gap-9">
      <div
        v-for="(tag, index) in value"
        :key="index"
        class="col-span-3 md:col-span-1 w-full cursor-pointer shadow-md bg-neptune-blue px-5 rounded-lg py-5 relative overflow-hidden"
        :class="selectColor(tag.active_vulnerabilities, tag.outdated_packages)"
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
        <p>{{  $t('images.image_name') }} : {{ tag.image + ':' + tag.tag }}</p>
        <p>{{ $t('images.image_size') }} : {{ calcSize(tag.size) }}</p>
        <p>{{ $tc('images.package', tag.packages) }} : {{ tag.packages }}</p>
        <p>{{ $tc('images.vulnerabilities', tag.vulnerabilities) }} : {{ tag.vulnerabilities }}</p>
        <p>{{ $tc('images.active_vulnerability', tag.active_vulnerabilities) }} : {{ tag.active_vulnerabilities }}</p>
        <p>{{ $tc('images.outdated_packages', tag.outdated_packages) }} : {{ tag.outdated_packages }}</p>
        <p>{{ $t('images.add_date') }} : {{ new Date(tag.date_added).toLocaleDateString('fr-FR') + ' ' + $t('images.at') + ' ' + new Date(tag.date_added).toLocaleTimeString('fr-FR')  }}</p>
        <p>{{ $t('images.sha') }} : {{ shaCut(tag.sha) }}</p>
      </div>
    </div>
    <div class="w-full flex justify-center mt-2">
      <Pagination v-model="page" :nbPages="nbPages" @change="getNewPage()" />
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
      search: undefined,
      openImagesModal: false,
      isLoading: true,
      backupTags: undefined,
      selectedOrder: 'ASC',
      openFilter: false,
      page: 1,
      imageName: undefined,
      filter: {
        name_filter: undefined,
      },
      delayRequest: undefined,
      perPage: 20,
      nbPages: 0,
    }
  },
  computed: {
    ...mapState('image', ['images', 'tags']),
  },
  watch: {
    filter: {
      handler() {
        clearTimeout(this.delayRequest)
        this.delayRequest = setTimeout(() => {
          this.getTags({page: this.page, perPage: this.perPage, filter: this.filter }).then(() => {
            this.value = this.tags.items
            this.nbPages = Math.ceil(this.tags.total / this.tags.per_page)
            this.backupTags = [...this.tags.items]
            this.page = 1
          })
        }, 1000)
      },
      deep: true,
    },
  },
  async mounted() {
    await this.getTags({page: this.page, perPage: this.perPage, filter: this.filter })
      .then(() => {
        this.value = this.tags.items
        this.nbPages = Math.ceil(this.tags.total / this.tags.per_page)
        this.backupTags = [...this.tags.items]
      })
      .finally(() => {
        this.isLoading = false
      })
  },
  methods: {
    ...mapActions('image', ['scanImages']),
    ...mapActions('image', ['getTags']),
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
    },
    getNewPage() {
      this.getTags({page: this.page, perPage: this.perPage }).then(() => {
        this.value = this.tags.items
        this.nbPages = Math.ceil(this.tags.total / this.tags.per_page)
        this.backupTags = [...this.tags.items]
      })
    },
    shaCut(sha) {
      return sha.split(':')[1].substring(0, 10)
    },
  },
}
</script>
