<template>
  <div class="w-full h-screen">
    <Table
      :columns="[
        {label: $t('vulnerability.name'), name: 'vuln'},
        {label: $t('vulnerability.severity'), name: 'severity'},
        {label: $t('vulnerability.source'), name: 'source'},
        {label: $t('vulnerability.affected_tags'), name: 'tags'},
        {label: $t('vulnerability.notes'), name: 'note'},
        {label: $t('vulnerability.acknowledged'), name: 'ack'}
      ]"
      :data="[{vuln: 'Test', severity: 'High'}]"
    >
      <template slot="severity" slot-scope="{item}">
        <div class="w-full flex justify-center">
          <div class="px-5 py-2 rounded-sm text-white w-36 uppercase font-bold" :class="colorSeverity(item)">
            <p>{{ $t(`vulnerability.state.${item.severity.toLowerCase()}`) }}</p>
          </div>
        </div>

      </template>
      <template slot="note" slot-scope="{item}">
        <input class="w-full" type="text" @focusout="sendNewNotes(item)">
      </template>
      <template slot="ack" slot-scope="{item}">
        <button class="px-5 py-2 bg-[#A6D1E6] rounded-sm text-white uppercase font-bold" @change="sendAck(item)">
          Test
        </button>
      </template>



    </Table>
  </div>
</template>

<script>
import { mapState, mapActions } from "vuex";

export default {
  name: "VunerabilitiesPage",
  async mounted() {
    // await this.getVulnerabilties();
  },
  methods: {
    ...mapActions('vulnerability', ['getVulnerabilties']),
    sendNewNotes() {
      console.log('test')
    },

    colorSeverity(item) {
      switch (item.severity) {
        case 'High':
          return 'bg-red-500'
        case 'Medium':
          return 'bg-yellow-500'
        case 'Low':
          return 'bg-green-500'
        case 'Negligible':
          return 'bg-[#A6D1E6]'
      }
    }
  },
  computed: {
    ...mapState('vulnerability', ['vuln'])
  }
}
</script>

<style scoped>

</style>
