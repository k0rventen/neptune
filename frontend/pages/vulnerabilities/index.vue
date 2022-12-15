<template>
  <div class="w-full h-screen overflow-y-auto scrollbar-thin px-5 py-5">

    <label class="relative">
      <input v-model="search" type="text" class="w-full mb-5 px-6 py-3 rounded-full shadow-md outline-none" placeholder="Rechercher ...">
    </label>

    <div class="w-full shadow-md rounded-xl bg-white px-3 py-3">
      <Table
      v-if="cveTable.length > 0"
      :columns="[
        {label: $t('vulnerability.name'), name: 'name', sorter: (row1 , row2) => row1.name.localeCompare(row2.name) },
        {label: $t('vulnerability.severity'), name: 'severity', sorter: (row1, row2) => {
          const severity = {
            'critical': 1,
            'high': 2,
            'medium': 3,
            'low': 4,
            'negligible': 5,
            'unknown': 6
          }
          return severity[row1.severity.toLowerCase()] - severity[row2.severity.toLowerCase()]
        }},
        {label: $t('vulnerability.source'), name: 'source'},
        {label: $t('vulnerability.affected_tags'), name: 'affected_images', sorter: (row1, row2) => row1.affected_images.length - row2.affected_images.length },
        {label: $t('vulnerability.notes'), name: 'notes'},
        {label: $t('vulnerability.acknowledged'), name: 'ack', sorter: (row1, row2) => (row1.ack === row2.ack) ? 0 : x ? -1 : 1},
      ]"
      :data="cveTable"
    >
      <template slot="severity" slot-scope="{item}">
        <div class="w-full flex justify-center">
          <div class="px-5 py-2 rounded-full text-white w-36 uppercase font-bold" :class="colorSeverity(item)">
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
          <button class="px-5 py-2 bg-[#A6D1E6] rounded-full text-white uppercase font-bold">
            {{ $t('vulnerability.tags') }}
          </button>

          <template #popper>
            <p>{{ item }}</p>
          </template>
        </VDropdown>

      </template>
      <template slot="ack" slot-scope="{item}">
        <button class="px-5 py-2 bg-[#A6D1E6] rounded-full text-white uppercase font-bold" :class="item.active ? 'bg-green-600' : 'bg-gray-400'" @click="changeAckState(item)">
          {{ item.active ? $t('vulnerability.acknowledged') : $t('vulnerability.not_acknowledged') }}
        </button>
      </template>
    </Table>
    </div>
    <div class="flex justify-center w-full mt-3">
      <Pagination v-model="pages" :nbPages="5"/>
    </div>
  </div>
</template>

<script>
import { mapState, mapActions } from "vuex";

export default {
  name: "VunerabilitiesPage",
  data() {
    return {
      copyNote: [],
      cveTable: [],
      search: undefined,
      pages: 1,
    }
  },
  computed: {
    ...mapState('vulnerability', ['vuln', 'notes'])
  },
  async mounted() {
    await this.getVulnerabilties().then(() => {
      this.copyNote = this.notes
      this.cveTable = this.vuln
    });
  },
  methods: {
    ...mapActions('vulnerability', ['getVulnerabilties', 'setNotes', 'setAckState']),
    sendNewNotes(item) {
      this.setNotes({ cve: item.id, notes: this.copyNote[item.name], active: item.active })
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
        case 'Unknown':
          return 'bg-[#eac7ff]'
      }
    },
    changeAckState(item) {
      this.setAckState({ cve: item.id, notes: this.copyNote[item.name], active: !item.active })
    },
  },
}
</script>

<style scoped>

</style>
