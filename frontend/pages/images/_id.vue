<template>
  <div v-if="!isLoading" class="w-full">
    <div class="mt-3 px-3">
      <div class="col-span-3 md:col-span-1 w-full cursor-pointer shadow-md bg-neptune-blue px-5 rounded-lg py-5 relative overflow-hidden bg-neptune-blue text-white">
        <p>Nom de l'image : {{( currentImage.image + ':' + currentImage.tag )}}</p>
        <p>Taille de l'image : {{ calcSize(currentImage.size)}}</p>
        <p>Date d'ajout : {{ new Date(currentImage.date_added).toLocaleDateString('fr-FR') + ' à ' + new Date(currentImage.date_added).toLocaleTimeString('fr-FR') }}</p>
        <svg class="absolute -bottom-2 right-0 opacity-20" xmlns="http://www.w3.org/2000/svg" width="128" height="128" viewBox="0 0 24 24" fill="white"><path d="M12 0c-6.627 0-12 5.373-12 12s5.373 12 12 12 12-5.373 12-12-5.373-12-12-12zm-.001 5.75c.69 0 1.251.56 1.251 1.25s-.561 1.25-1.251 1.25-1.249-.56-1.249-1.25.559-1.25 1.249-1.25zm2.001 12.25h-4v-1c.484-.179 1-.201 1-.735v-4.467c0-.534-.516-.618-1-.797v-1h3v6.265c0 .535.517.558 1 .735v.999z"/></svg>
      </div>
      <div class="w-full grid grid-cols-2 gap-9 mt-6">
        <div class="w-full h-96 bg-red-600">
          <Table></Table>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { mapActions, mapState } from 'vuex'
import calcSize from '@/mixins/sizeCalc.js'

export default {
  name: "ImageDetail",
  mixins: [calcSize],
  data() {
    return {
      isLoading: true,
    }
  },
  computed: {
    ...mapState('image', ['currentImage']),
  },
  async mounted() {
    await this.getCurrentImage(this.$route.params.id).then(() => {
      this.isLoading = false
    })
  },
  methods: {
    ...mapActions('image', ['getCurrentImage']),
    selectColor(vuln, outdated){
      if(vuln > 0) {
        return 'bg-red-400'
      }
      if(outdated > 0) {
        return 'bg-yellow-400'
      }
      return 'bg-green-400'
    },
  },
}
</script>
