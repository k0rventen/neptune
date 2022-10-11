<template>
  <div v-if="!isLoading" class="w-full">
    <div class="mt-3 px-3">
      <card-image :header="currentImage.distro.name.toLowerCase().concat(':', currentImage.distro.version)" :color="selectColor(currentImage.vulnerabilities.length, currentImage.outdated_packages.length)" >
        <ul>
          <li>{{$t('images.name_of_image')}} : {{ currentImage.distro.name.toLowerCase() }}:{{currentImage.distro.version}}</li>
          <li>{{$t('images.added_date')}} : {{ convertDate(currentImage.date_added)}} </li>
          <li>{{ $t('images.size') }} : {{ calcSize(currentImage.size) }}</li>
        </ul>
      </card-image>

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
