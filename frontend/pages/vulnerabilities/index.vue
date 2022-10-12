<template>
  <div class="w-full h-screen">

    <label class="relative">
      <input v-model="search" type="text" class="my-3 focus:outline-none border border-[#3D3C42] rounded-md w-full px-5 py-1 bg-[#FEFBF6] placeholder-black" :placeholder="$t('images.search')">
      <svg class="absolute top-1 left-1 fill-black" xmlns="http://www.w3.org/2000/svg" width="12" height="12" viewBox="0 0 24 24"><path d="M21.172 24l-7.387-7.387c-1.388.874-3.024 1.387-4.785 1.387-4.971 0-9-4.029-9-9s4.029-9 9-9 9 4.029 9 9c0 1.761-.514 3.398-1.387 4.785l7.387 7.387-2.828 2.828zm-12.172-8c3.859 0 7-3.14 7-7s-3.141-7-7-7-7 3.14-7 7 3.141 7 7 7z"/></svg>
    </label>

    <Table
      :columns="[
        {label: $t('vulnerability.name'), name: 'name', order: true},
        {label: $t('vulnerability.severity'), name: 'severity', order: true},
        {label: $t('vulnerability.source'), name: 'source'},
        {label: $t('vulnerability.affected_tags'), name: 'affected_images', order: true},
        {label: $t('vulnerability.notes'), name: 'notes'},
        {label: $t('vulnerability.acknowledged'), name: 'ack', order: true}
      ]"
      :data="vuln"
      @filter="(value) => test(value)"
    >
      <template slot="severity" slot-scope="{item}">
        <div class="w-full flex justify-center">
          <div class="px-5 py-2 rounded-sm text-white w-36 uppercase font-bold" :class="colorSeverity(item)">
            <p>{{ $t(`vulnerability.state.${item.severity.toLowerCase()}`) }}</p>
          </div>
        </div>
      </template>
      <template slot="name" slot-scope="{item}">
        <a target="_blank" :href="`https://www.google.com/search?q=${item.name}`">
          <p>{{ item.name }}</p>
        </a>
      </template>
      <template slot="notes" slot-scope="{item}">
        <input v-model="copyNote[item.name]" class="w-full outline-none bg-transparent text-center" type="text" @focusout="sendNewNotes(item)">
      </template>
      <template slot="affected_images" slot-scope="{item}">
        <VDropdown
          :distance="6"
        >
          <button class="px-5 py-2 bg-[#A6D1E6] rounded-sm text-white uppercase font-bold">
            {{ item.affected_images.length }} {{ $t('vulnerability.tags') }}
          </button>

          <template #popper>
            <div class="px-3 py-1">
              <p v-for="image in item.affected_images" :key="image" class="cursor-pointer" @click="$router.push({ path: '/images/' + image.sha } )">{{ image.image }}:{{ image.tag }}</p>
            </div>
          </template>
        </VDropdown>

      </template>
      <template slot="ack" slot-scope="{item}">
        <button class="px-5 py-2 bg-[#A6D1E6] rounded-sm text-white uppercase font-bold" :class="item.active ? 'bg-green-600' : 'bg-gray-400'" @click="changeAckState(item)">
          {{ item.active ? $t('vulnerability.acknowledged') : $t('vulnerability.not_acknowledged') }}
        </button>
      </template>



    </Table>
  </div>
</template>

<script>
import { mapState, mapActions } from "vuex";

export default {
  name: "VunerabilitiesPage",
  data() {
    return {
      copyNote: [],
      search: undefined,
    }
  },
  computed: {
    ...mapState('vulnerability', ['vuln', 'notes'])
  },
  async mounted() {
    await this.getVulnerabilties().then(() => {
      this.copyNote = this.notes
    });
  },
  methods: {
    ...mapActions('vulnerability', ['getVulnerabilties', 'setNotes', 'setAckState']),
    sendNewNotes(item) {
      this.setNotes({ cve: item.id, notes: this.copyNote[item.name], active: item.active })
    },
    test(value) {
      console.log(value)
    },
    colorSeverity(item) {
      switch (item.severity) {
        case 'Critical':
          return 'bg-black'
        case 'High':
          return 'bg-red-500'
        case 'Medium':
          return 'bg-yellow-500'
        case 'Low':
          return 'bg-green-500'
        case 'Negligible':
          return 'bg-[#A6D1E6]'
      }
    },
    changeAckState(item) {
      this.setAckState({ cve: item.id, notes: this.copyNote[item.name], active: !item.active })
    }
  },
}
</script>

<style scoped>

</style>
