<template>
  <div class="w-full h-screen px-5 py-5 overflow-y-auto scrollbar-thin">
    <Loading v-if="isLoading" />
    <div class="w-full shadow-md rounded-xl bg-white overflow-x-auto px-3 py-3">
      <Table
        v-if="dependencies.length > 0"
        :columns="[
          { label: $t('dependencies.type'), name: 'type' },
          { label: $t('dependencies.name'), name: 'name' },
          { label: $t('dependencies.version'), name: 'version' },
          {
            label: $t('dependencies.minimum_version'),
            name: 'minimum_version',
          },
          { label: $t('dependencies.notes'), name: 'notes' },
        ]"
        :data="dependencies"
      >
        <template slot="notes" slot-scope="{ item }">
          <input
            v-model="copyNotes[item.name]"
            class="w-full outline-none bg-transparent text-center"
            type="text"
            @focusout="sendNewNotes(item)"
          />
        </template>
        <template slot="minimum_version" slot-scope="{ item }">
          <input
            v-model="copyMinVersion[item.name]"
            class="w-full outline-none bg-transparent text-center"
            type="text"
            @focusout="sendNewVersion(item)"
          />
        </template>
        <template slot="version" slot-scope="{ item }">
            <div class="flex gap-3">
              <VDropdown :key="version.id" v-for="version in item.versions">
                <button class="py-1 px-2 text-xs text-white rounded-md max-w-prose" :class="bgFinder(version)">
                  <p>{{ removeUseless(version.version) }}</p>
                </button>

                <template #popper>
                  <div class="px-2 py-1 outline-none">
                    <p class="text-center">{{ version.version }}</p>
                    <hr v-if="version.vulnerabilities.length > 0">
                    <a v-for="vuln in version.vulnerabilities" :key="vuln.id" :href="`https://www.google.com/search?client=firefox-b-d&q=${vuln.name}`">
                      <p >
                        {{  vuln.name }}
                      </p>
                    </a>
                    
                    <div class="mt-2">
                      <p>Image(s) concerné(s) :</p>
                      <hr>
                        <p v-for="tag in version.tags" :key="tag.sha" class="cursor-pointer" @click="$router.push({ path: '/images/' + tag.sha })">
                          {{ tag.name }}
                        </p>
                    </div>
                    
                  </div>
                </template>
              </VDropdown>
          </div>
        </template>
      </Table>
    </div>
  </div>
</template>

<script>
import { mapActions, mapState } from 'vuex'

export default {
  name: 'DependenciesPage',
  data() {
    return {
      version: '',
      copyMinVersion: [],
      copyNotes: [],
      page: 1,
      isLoading: true
    }
  },
  computed: {
    ...mapState('dependencies', ['dependencies', 'min_version', 'notes']),
  },
  async mounted() {
    await this.getDependencies().then(() => {
      this.copyMinVersion = this.min_version
      this.copyNotes = this.notes
      this.isLoading = false
    }).finally(() => {
      if(this.$route.query.package) {
        const rows = [...document.getElementById('c-table').rows]
        rows.forEach((el) => {
          if(el.cells[1].innerText === this.$route.query.package) {
            el.scrollIntoView()
          }
        })
      }
    })
  },
  methods: {
    ...mapActions('dependencies', [
      'getDependencies',
      'setVersion',
      'setNotes',
    ]),
    sendNewVersion(item) {
      this.setVersion({
        id: item.id,
        version: this.copyMinVersion[item.name],
        notes: item.notes,
      })
    },
    sendNewNotes(item) {
      this.setNotes({
        id: item.id,
        version: item.minimum_version,
        notes: this.copyNotes[item.name],
      })
    },
    removeUseless(version) {
      let res = version
      if(res.includes('ubuntu')) {
        res = res.replace('ubuntu', '')
      }
      if (res.length > 13) {
        return res.slice(0, 13) + '...'
      }
      return res
    },
    bgFinder (version) {
      if (version.vulnerabilities.length > 0) {
        return 'bg-red-500'
      }
      if (version.oudated === true) {
        return 'bg-yellow-500'
      } else {
        return 'bg-green-500'
      }
    }
  },
}
</script>

<style scoped></style>
