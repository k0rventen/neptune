<template>
  <div class="w-full">
    <Table
      :columns="[
        {label: $t('dependencies.type'), name: 'type'},
        {label: $t('dependencies.name'), name: 'name'},
        {label: $t('dependencies.vulnerability'), name: 'vuln'},
        {label: $t('dependencies.version'), name: 'version'},
        {label: $t('dependencies.minimum_version'), name: 'minimum_version'},
        {label: $t('dependencies.notes'), name: 'notes'},
      ]"
      :data="dependencies"
    >
      <template slot="notes" slot-scope="{item}">
        <input v-model="copyNotes[item.name]" class="w-full outline-none bg-transparent text-center" type="text" @focusout="sendNewNotes(item)">
      </template>
      <template slot="minimum_version" slot-scope="{item}">
        <input v-model="copyMinVersion[item.name]" class="w-full outline-none bg-transparent text-center" type="text" @focusout="sendNewVersion(item)">
      </template>
    </Table>
  </div>
</template>

<script>
import { mapActions, mapState } from 'vuex'

export default {
  name: "DependenciesPage",
  data() {
    return {
      version: '',
      copyMinVersion: [],
      copyNotes: [],
    }
  },
  computed: {
    ...mapState('dependencies', ['dependencies', 'min_version', 'notes']),
  },
  async mounted() {
    await this.getDependencies().then(() => {
      this.copyMinVersion = this.min_version
      this.copyNotes = this.notes
    })
  },
  methods: {
    ...mapActions('dependencies', ['getDependencies', 'setVersion', 'setNotes']),
    sendNewVersion(item) {
      this.setVersion({ id: item.id, version: this.copyMinVersion[item.name], notes: item.notes })
    },
    sendNewNotes(item) {
      this.setNotes({ id: item.id, version: item.minimum_version, notes: this.copyNotes[item.name] })
    },
  },
}
</script>

<style scoped>

</style>
