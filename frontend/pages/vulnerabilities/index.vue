<template>
  <div class="w-full h-screen overflow-y-auto scrollbar-thin px-5 py-5">
    <div class="relative">
      <input
        v-model="filter.name_filter"
        type="text"
        class="w-full mb-5 px-6 py-3 rounded-full shadow-md outline-none"
        placeholder="Rechercher ..."
      />
      <svg
        class="absolute right-4 top-3 opacity-20"
        width="26"
        height="26"
        clip-rule="evenodd"
        fill-rule="evenodd"
        stroke-linejoin="round"
        stroke-miterlimit="2"
        viewBox="0 0 24 24"
        xmlns="http://www.w3.org/2000/svg"
        @click="openFilter = !openFilter"
      >
        <path
          d="m15.344 17.778c0-.414-.336-.75-.75-.75h-5.16c-.414 0-.75.336-.75.75s.336.75.75.75h5.16c.414 0 .75-.336.75-.75zm2.206-4c0-.414-.336-.75-.75-.75h-9.596c-.414 0-.75.336-.75.75s.336.75.75.75h9.596c.414 0 .75-.336.75-.75zm2.45-4c0-.414-.336-.75-.75-.75h-14.5c-.414 0-.75.336-.75.75s.336.75.75.75h14.5c.414 0 .75-.336.75-.75zm2-4c0-.414-.336-.75-.75-.75h-18.5c-.414 0-.75.336-.75.75s.336.75.75.75h18.5c.414 0 .75-.336.75-.75z"
          fill-rule="nonzero"
        />
      </svg>
    </div>

    <div v-if="openFilter" class="w-full flex gap-3 mb-2">
      <div class="w-1/6">
        <label for="trie" class="block">
          {{ $t('images.severity_filter') }}
        </label>
        <select
          id="trie"
          v-model="filter.severity_filter"
          class="w-full px-3 py-1 rounded-md mb-2 shadow-md"
        >
          <option :value="undefined">{{ $t('images.none') }}</option>
          <option value="unknown">{{ $t('images.unknown') }}</option>
          <option value="low">{{ $t('images.low') }}</option>
          <option value="medium">{{ $t('images.medium') }}</option>
          <option value="high">{{ $t('images.high') }}</option>
          <option value="critical">{{ $t('images.critical') }}</option>
        </select>
      </div>
      <div class="w-1/6">
        <label for="trie" class="block">
          {{ $t('images.state_filter') }}
        </label>
        <select
          id="state"
          v-model="filter.active_filter"
          class="w-full px-3 py-1 rounded-md mb-2 shadow-md"
        >
          <option :value="undefined">{{ $t('images.none') }}</option>
          <option value="true">{{ $t('images.active') }}</option>
          <option value="false">{{ $t('images.inactive') }}</option>
        </select>
      </div>
    </div>

    <div class="w-full shadow-md rounded-xl bg-white px-3 py-3">
      <Table
        v-if="cveTable.length > 0"
        :key="this.refreshKey"
        :columns="[
          {
            label: $t('vulnerability.acknowledged'),
            name: 'ack',
          },
          {
            label: $t('vulnerability.name'),
            name: 'name',
          },
          {
            label: $t('vulnerability.severity'),
            name: 'severity',
          },
          { label: $t('vulnerability.source'), name: 'source' },
          {
            label: $t('vulnerability.affected_tags'),
            name: 'affected_images',
          },
          { label: $t('vulnerability.notes'), name: 'notes' },
        ]"
        :data="cveTable"
      >
        <template slot="severity" slot-scope="{ item }">
          <div class="w-full flex justify-center">
            <div
              class="px-2 py-1 rounded-md text-white w-36 uppercase font-bold"
              :class="colorSeverity(item)"
            >
              <p>
                {{ $t(`vulnerability.state.${item.severity.toLowerCase()}`) }}
              </p>
            </div>
          </div>
        </template>
        <template slot="name" slot-scope="{ item }">
          <a
            target="_blank"
            :href="`https://www.google.com/search?q=${item.name}`"
          >
            <p>{{ item.name }}</p>
          </a>
        </template>
        <template slot="notes" slot-scope="{ item }">
          <input
            v-model="copyNote[item.name]"
            class="w-full outline-none bg-transparent text-center"
            type="text"
            @focusout="sendNewNotes(item)"
          />
        </template>
        <template slot="source" slot-scope="{ item }">
          <NuxtLink :to="'/dependencies?package=' + item.affected_package.name">
            <p>
              {{
                item.affected_package.name + ':' + item.affected_package.version
              }}
            </p>
          </NuxtLink>
        </template>
        <template slot="affected_images" slot-scope="{ item }">
          <VDropdown :distance="6">
            <button
              class="px-2 text-xs py-1 bg-[#A6D1E6] rounded-md text-white uppercase font-bold"
            >
              {{ item.affected_images.length }} {{ $t('vulnerability.tags') }}
            </button>

            <template #popper>
              <div
                v-for="image in item.affected_images"
                :key="image.sha"
                class="px-2 py-2 hover:font-bold cursor-pointer"
                @click="$router.push({ path: '/images/' + image.sha })"
              >
                <p>
                  {{ image.name }}
                </p>
              </div>
            </template>
          </VDropdown>
        </template>
        <template slot="ack" slot-scope="{ item }">
          <button
            class="px-2 py-1 rounded-md text-xs text-white uppercase font-bold"
            :class="item.active ? 'bg-green-600' : 'bg-gray-400'"
            @click="changeAckState(item)"
          >
            {{
              item.active
                ? $t('vulnerability.acknowledged')
                : $t('vulnerability.not_acknowledged')
            }}
          </button>
        </template>
      </Table>
      <div class="w-full flex mt-3 justify-center">
        <Pagination
          v-model="pages"
          :nbPages="this.nbPages"
          @change="getNewPages()"
        />
      </div>
    </div>
  </div>
</template>

<script>
import { mapState, mapActions } from 'vuex'

export default {
  name: 'VunerabilitiesPage',
  data() {
    return {
      copyNote: [],
      cveTable: [],
      filter: {
        name_filter: undefined,
        severity_filter: undefined,
        active_filter: undefined,
      },
      pages: 1,
      nbPages: 0,
      perPage: 50,
      refreshKey: 0,
      delayRequest: undefined,
      openFilter: false,
    }
  },
  computed: {
    ...mapState('vulnerability', ['vuln', 'notes']),
  },
  watch: {
    filter: {
      handler() {
        if (this.delayRequest) clearTimeout(this.delayRequest)
        this.page = 1
        this.delayRequest = setTimeout(() => {
          this.getVulnerabilties({
            page: this.page,
            perPage: this.perPage,
            filter: this.filter,
          }).then(() => {
            this.copyNote = this.notes
            this.nbPages = Math.ceil(this.vuln.total / this.vuln.per_page)
            this.cveTable = this.vuln.items
            this.pages = 1
            this.refreshKey++
          })
        }, 1000)
      },
      deep: true,
    },
  },
  async mounted() {
    await this.getVulnerabilties({
      page: this.pages,
      perPage: this.perPage,
      filter: this.filter,
    })
      .then(() => {
        this.copyNote = this.notes
        this.nbPages = Math.ceil(this.vuln.total / this.vuln.per_page)
        this.cveTable = this.vuln.items
      })
      .finally(() => {
        if (this.$route.query.name) {
          this.filter.name_filter = this.$route.query.name
          this.refreshKey++
        }
      })
  },
  methods: {
    ...mapActions('vulnerability', [
      'getVulnerabilties',
      'setNotes',
      'setAckState',
    ]),
    sendNewNotes(item) {
      this.setNotes({
        cve: item.id,
        notes: this.copyNote[item.name],
        active: item.active,
      })
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
      this.setAckState({
        cve: item.id,
        notes: this.copyNote[item.name],
        active: !item.active,
      })
    },
    getNewPages() {
      this.getVulnerabilties({
        page: this.pages,
        perPage: this.perPage,
        filter: this.filter,
      }).then(() => {
        this.copyNote = this.notes
        this.cveTable = []
        this.cveTable = this.vuln.items
        this.refreshKey++
      })
    },
  },
}
</script>

<style scoped></style>
