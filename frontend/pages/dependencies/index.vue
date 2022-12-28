<template>
  <div class="w-full h-screen px-5 py-5 overflow-y-auto scrollbar-thin">
    <Loading v-if="isLoading" />
    <div class="w-full relative">
      <input
        v-model="filter.name_filter"
        type="text"
        class="w-full mb-2 px-6 py-3 rounded-full shadow-md outline-none"
        :placeholder="$t('dependencies.search')"
      />
    </div>
    <div class="mb-2">
      <input v-model="filter.with_outdated_versions" type="checkbox" id="outdatedV" name="outdatedV">
      <label for="outdatedV">{{  $t('dependencies.with_outdated_version') }}</label>
      <input v-model="filter.with_vulnerable_versions" type="checkbox" id="vulnerableV" name="vulnerableV">
      <label for="vulnerableV">{{  $t('dependencies.with_vulnerable_version') }}</label>
    </div>
    
    <div class="w-full shadow-md rounded-xl bg-white overflow-x-auto px-3 py-3">
      <Table
        v-if="dependencies.items && dependencies.items?.length > 0"
        :key="refreshKey"
        :columns="[
          {
            label: $t('dependencies.type'),
            name: 'type',
            sorter: (row1, row2) => row1.type.localeCompare(row2.type),
          },
          { label: $t('dependencies.name'), name: 'name' },
          { label: $t('dependencies.version'), name: 'version' },
          {
            label: $t('dependencies.minimum_version'),
            name: 'minimum_version',
          },
          { label: $t('dependencies.notes'), name: 'notes' },
        ]"
        :data="dependencies.items"
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
              <button
                class="py-1 px-2 text-xs text-white rounded-md max-w-prose"
                :class="bgFinder(version)"
              >
                <p>{{ removeUseless(version.version) }}</p>
              </button>

              <template #popper>
                <div class="px-2 py-1 outline-none">
                  <p class="text-center">{{ version.version }}</p>
                  <hr v-if="version.vulnerabilities.length > 0" />
                  <a
                    v-for="vuln in version.vulnerabilities"
                    :key="vuln.id"
                    :href="`https://www.google.com/search?client=firefox-b-d&q=${vuln.name}`"
                  >
                    <p>
                      {{ vuln.name }}
                    </p>
                  </a>

                  <div class="mt-2">
                    <p>{{ $t('dependencies.concerned_image') }} :</p>
                    <hr />
                    <p
                      v-for="tag in version.tags"
                      :key="tag.sha"
                      class="cursor-pointer"
                      @click="$router.push({ path: '/images/' + tag.sha })"
                    >
                      {{ tag.name }}
                    </p>
                  </div>
                </div>
              </template>
            </VDropdown>
          </div>
        </template>
      </Table>
      <div class="w-full flex mt-2 justify-center">
        <Pagination
          v-model="page"
          :nbPages="this.nbPages"
          @change="getNewPages()"
        />
      </div>
    </div>
  </div>
</template>

<script>
import { mapActions, mapMutations, mapState } from 'vuex'

export default {
  name: 'DependenciesPage',
  data() {
    return {
      version: '',
      copyMinVersion: [],
      copyNotes: [],
      page: 1,
      nbPages: 0,
      perPage: 25,
      isLoading: true,
      refreshKey: 0,
      delayRequest: undefined,
      filter: {
        name_filter: undefined,
        with_outdated_versions: undefined,
        with_vulnerable_versions: undefined,
      }
    }
  },
  watch: {
    filter: {
      handler() {
        if (this.delayRequest) clearTimeout(this.delayRequest)
        this.page = 1
        this.delayRequest = setTimeout(() => {
          this.getDependencies({
            page: this.page,
            perPage: this.perPage,
            filter: this.filter,
          }).then(() => {
            this.copyMinVersion = this.min_version
            this.nbPages = Math.ceil(this.dependencies.total / this.perPage)
            this.copyNotes = this.notes
            this.refreshKey++
          })
        }, 1000)
      },
      deep: true,
    },
  },
  computed: {
    ...mapState('dependencies', ['dependencies', 'min_version', 'notes']),
  },
  async mounted() {
    await this.getDependencies({ page: this.page, perPage: this.perPage })
      .then(() => {
        this.copyMinVersion = this.min_version
        this.nbPages = Math.ceil(this.dependencies.total / this.perPage)
        this.copyNotes = this.notes
        this.isLoading = false
      }).finally(() => {
        if(this.$route.query.package) {
          this.filter.name_filter = this.$route.query.package
        }
      })
      
  },
  methods: {
    ...mapActions('dependencies', [
      'getDependencies',
      'setVersion',
      'setNotes',
    ]),
    ...mapMutations('dependencies', ['updateOutdated']),
    sendNewVersion(item) {
      this.setVersion({
        id: item.id,
        version: this.copyMinVersion[item.name],
        notes: item.notes,
      })
      this.updateOutdated({
        id: item.id,
        version: this.copyMinVersion[item.name],
      })
      this.refreshKey++
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
      if (res.includes('ubuntu')) {
        res = res.replace('ubuntu', '')
      }
      if (res.length > 13) {
        return res.slice(0, 13) + '...'
      }
      return res
    },
    bgFinder(version) {
      if (version.vulnerabilities.length > 0) {
        return 'bg-red-500'
      }
      if (version.outdated === true) {
        return 'bg-yellow-500'
      } else {
        return 'bg-green-500'
      }
    },
    getNewPages() {
      this.isLoading = true
      this.getDependencies({ page: this.page, perPage: this.perPage }).then(
        () => {
          this.copyMinVersion = this.min_version
          this.copyNotes = this.notes
          this.isLoading = false
          this.refreshKey++
        }
      )
    },
  },
}
</script>

<style scoped></style>
