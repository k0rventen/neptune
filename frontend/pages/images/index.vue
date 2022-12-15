<template>
  <div class="w-full px-5 py-5 text-white h-screen scrollbar-thin overflow-auto">
    <Loading v-if="isLoading === true"/>
    <div class="text-gray-400">
      <input v-model="search" type="text" class="w-full mb-5 px-6 py-3 rounded-full shadow-md outline-none" placeholder="Rechercher ...">
    </div>
    <div class="w-full grid grid-cols-3 gap-9">
        <div v-for="(tag,index) in value" :key="index" class="col-span-3 md:col-span-1 w-full cursor-pointer shadow-md bg-neptune-blue px-5 rounded-lg py-5 relative overflow-hidden" :class="selectColor(tag.vulnerabilities, tag.outdated_packages)" @click="$router.push({ path: '/images/' + tag.sha } )">
          <svg class="absolute opacity-20 right-0 -bottom-8" width="128" height="128" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg" fill="white"><path d="M11.5 23l-8.5-4.535v-3.953l5.4 3.122 3.1-3.406v8.772zm1-.001v-8.806l3.162 3.343 5.338-2.958v3.887l-8.5 4.534zm-10.339-10.125l-2.161-1.244 3-3.302-3-2.823 8.718-4.505 3.215 2.385 3.325-2.385 8.742 4.561-2.995 2.771 2.995 3.443-2.242 1.241v-.001l-5.903 3.27-3.348-3.541 7.416-3.962-7.922-4.372-7.923 4.372 7.422 3.937v.024l-3.297 3.622-5.203-3.008-.16-.092-.679-.393v.002z"/></svg>
          <p>Nom de l'image : {{tag.image + ':' + tag.tag}}</p>
          <p>Taille de l'image : {{ calcSize(tag.size) }}</p>
          <p>Paquets : {{ tag.packages }}</p>
          <p>Vulnérabilité : {{ tag.vulnerabilities }}</p>
          <p>Paquet obsolète : {{ tag.outdated_packages }}</p>
        </div>
    </div>
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
      isLoading: true
    }
  },
  computed: {
    ...mapState('image', ['images', 'tags']),
  },
  watch: {
    search(newValue) {
      if(newValue === '') {
        this.value = this.tags
      } else {
        this.value = this.tags.filter((el) => {
          const fullname = el.image + ':' + el.tag
          return fullname.toLowerCase().includes(newValue.toLowerCase())
        })
      }
    },
  },
  async mounted() {
    await this.getTags().then(() => {
      this.value = this.tags
    }).finally(() => {
      this.isLoading = false
    })
  },
  methods: {
    ...mapActions('image', ['getImages', 'getTags']),
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
      return 'bg-neptune-blue'
    },
  }
}
</script>

