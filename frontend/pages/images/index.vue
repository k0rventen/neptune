<template>
  <div class="w-full">
    <div class="mt-3 px-3 w-full">
      <label class="relative">
        <svg class="absolute top-1 left-1 fill-black" xmlns="http://www.w3.org/2000/svg" width="12" height="12" viewBox="0 0 24 24"><path d="M21.172 24l-7.387-7.387c-1.388.874-3.024 1.387-4.785 1.387-4.971 0-9-4.029-9-9s4.029-9 9-9 9 4.029 9 9c0 1.761-.514 3.398-1.387 4.785l7.387 7.387-2.828 2.828zm-12.172-8c3.859 0 7-3.14 7-7s-3.141-7-7-7-7 3.14-7 7 3.141 7 7 7z"/></svg>
        <input v-model="search" type="text" class="focus:outline-none border border-[#3D3C42] rounded-md w-full px-5 py-1 bg-[#FEFBF6] placeholder-black" :placeholder="$t('images.search')">
        <button class="mt-2 px-3 py-1 rounded-md bg-[#A6D1E6] text-white font-bold transition ease-in hover:shadow-sm hover:-translate-y-0.5" @click="openModalAdd = true">{{ $t('images.add_image') }}</button>
      </label>
      <div class="grid grid-cols-1 md:grid-cols-3 gap-3 mt-3">
        <template v-for="image in value">
          <card-image v-for="(tags,index) in image.tags" :key="index" :header="tags.image.concat(':', tags.tag)" :color="selectColor(tags.vulnerabilities, tags.outdated_packages)" @click.native="$router.push({ path: '/images/' + tags.sha } )" >
            <template #header>
              <div class="bg-white opacity-50 flex justify-center items-center rounded-full px-0.5 py-0.5" @click.stop="deleteImage(tags.sha)">
                <svg clip-rule="evenodd" width="16" height="16" fill="black" stroke-linejoin="round" stroke-miterlimit="2" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><path d="m12 10.93 5.719-5.72c.146-.146.339-.219.531-.219.404 0 .75.324.75.749 0 .193-.073.385-.219.532l-5.72 5.719 5.719 5.719c.147.147.22.339.22.531 0 .427-.349.75-.75.75-.192 0-.385-.073-.531-.219l-5.719-5.719-5.719 5.719c-.146.146-.339.219-.531.219-.401 0-.75-.323-.75-.75 0-.192.073-.384.22-.531l5.719-5.719-5.72-5.719c-.146-.147-.219-.339-.219-.532 0-.425.346-.749.75-.749.192 0 .385.073.531.219z"/></svg>
              </div>
            </template>
            <ul>
              <li>{{ $t('images.added_date') }} : {{ convertDate(tags.date_added) }}</li>
              <li>{{ $t('images.size') }} : {{ calcSize(tags.size) }}</li>
              <li>{{ $tc('images.package', tags.packages) }} : {{ tags.packages }}</li>
              <li>{{ $tc('images.vulnerability', tags.vulnerabilities )}} : {{ tags.vulnerabilities }} </li>
              <li>{{ $tc('images.outdated_package', tags.outdated_packages )}} : {{ tags.outdated_packages }} </li>
            </ul>
          </card-image>
        </template>
      </div>
    </div>

  <Modal v-if="openModalAdd" v-model="openModalAdd" :title="$t('images.add_image')">
    <div class="w-full">
      <p class="mt-3">{{ $t('images.name_of_image') }}</p>
      <input v-model="imageToScan" class="w-full mt-1 px-3 py-1 focus:outline-none border border-[#3D3C42] rounded-md" type="text" :placeholder="'Ex. ubuntu:22.07'">
    </div>
    <template #footer>
      <button class="bg-green-500 w-full text-white font-bold text-white px-3 py-1 rounded-md transition ease-in hover:shadow-sm hover:-translate-y-0.5" @click="sendImage">Envoyer</button>
    </template>
  </Modal>
  </div>
</template>

<script>
import { mapActions, mapState } from 'vuex'
import calcSize from '@/mixins/sizeCalc.js'

export default {
  name: "ImagesPage",
  mixins: [calcSize],
  data() {
    return {
      value: undefined,
      imageToScan: undefined,
      search: undefined,
      openModalAdd: false,
    }
  },
  computed: {
    ...mapState('image', ['images']),
  },
  watch: {
    search(newValue) {
      if(newValue === '') {
        this.value = this.images
      } else {
        this.value = this.images.filter((el) => el.name.toLowerCase().includes(newValue.toLowerCase()) )
      }
    },
  },
  async mounted() {
    await this.getImages().then(() => {
      this.value = this.images
    })
  },
  methods: {
    ...mapActions('image', ['getImages', "scanImages", 'deleteImage']),
    async sendImage() {
      await this.scanImages(this.imageToScan).then(() => {
        this.imageToScan = undefined
      })
    },
    selectColor(vuln, outdated){
      if(vuln > 0) {
        return 'bg-red-400'
      }
      if(outdated > 0) {
        return 'bg-yellow-400'
      }
      return 'bg-green-400'
    },
  }
}
</script>

