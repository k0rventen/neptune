<template>
  <div class="w-full h-screen overflow-y-auto scrollbar-thin">
    <Loading v-if="isLoading === true" />
    <div v-if="isLoading === false" class="mt-3 px-3">
      <div
        class="col-span-3 overflow-x-auto md:col-span-1 w-full shadow-md bg-neptune-blue px-5 rounded-lg py-5 relative overflow-hidden bg-neptune-blue text-white"
      >
        <div class="w-2/3 grid grid-cols-2">
          <div>
            <p>
              {{ $t('image_id.image_name') }} :
              {{ currentImage.image + ':' + currentImage.tag }}
            </p>
            <p>
              {{ $t('image_id.image_size') }} :
              {{ calcSize(currentImage.size) }}
            </p>
            <p>
              {{ $t('image_id.add_date') }} :
              {{
                new Date(currentImage.date_added).toLocaleDateString('fr-FR') +
                ' à ' +
                new Date(currentImage.date_added).toLocaleTimeString('fr-FR')
              }}
            </p>
            <p>{{ $t('image_id.distro') }} : {{ currentImage.distro }}</p>
          </div>
          <div>
            <p>
              {{ $tc('image_id.package', currentImage.packages.length) }} : {{ currentImage.packages.length }}
            </p>
            <p>
              {{ $tc('image_id.vulnerabilities', currentImage.vulnerabilities.length) }} :
              {{ currentImage.vulnerabilities.length }}
            </p>
            <p>
              {{ $tc('image_id.active_vulnerability', currentImage.active_vulnerabilities.length) }} :
              {{ currentImage.active_vulnerabilities.length }}
            </p>
            <p>
              {{ $tc('image_id.outdated_packages', currentImage.outdated_packages.length) }} :
              {{ currentImage.outdated_packages.length }}
            </p>
          </div>
        </div>

        <div v-tooltip="`Supprimer l'image`" class="bg-white bg-opacity-20 absolute h-5 w-5 rounded-full right-3 top-3" @click="deleteImg()">
          <svg clip-rule="evenodd" fill-rule="evenodd" stroke-linejoin="round" stroke-miterlimit="2" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg" fill="white"><path d="m12 10.93 5.719-5.72c.146-.146.339-.219.531-.219.404 0 .75.324.75.749 0 .193-.073.385-.219.532l-5.72 5.719 5.719 5.719c.147.147.22.339.22.531 0 .427-.349.75-.75.75-.192 0-.385-.073-.531-.219l-5.719-5.719-5.719 5.719c-.146.146-.339.219-.531.219-.401 0-.75-.323-.75-.75 0-.192.073-.384.22-.531l5.719-5.719-5.72-5.719c-.146-.147-.219-.339-.219-.532 0-.425.346-.749.75-.749.192 0 .385.073.531.219z"/></svg>
        </div>
      </div>
      <div class="w-full grid grid-cols-2 gap-3 mt-3">
        <div
          class="col-span-2 lg:col-span-1 w-full bg-white shadow-md rounded-xl rounded-md px-3 py-3 overflow-x-auto"
        >
          <Table
            :data="tableData"
            :columns="[
              { label: $tc('image_id.package', 2), name: 'package' },
              { label: $t('image_id.version'), name: 'version' },
              { label: $t('image_id.outdated'), name: 'outdated' },
            ]"
          >
            <template slot="outdated" slot-scope="{ item }">
              <div class="flex justify-center items-center">
                <svg v-if="item.outdated" clip-rule="evenodd" fill-rule="evenodd" stroke-linejoin="round" stroke-miterlimit="2" width="24" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><path d="m2.095 19.886 9.248-16.5c.133-.237.384-.384.657-.384.272 0 .524.147.656.384l9.248 16.5c.064.115.096.241.096.367 0 .385-.309.749-.752.749h-18.496c-.44 0-.752-.36-.752-.749 0-.126.031-.252.095-.367zm9.907-6.881c-.414 0-.75.336-.75.75v3.5c0 .414.336.75.75.75s.75-.336.75-.75v-3.5c0-.414-.336-.75-.75-.75zm-.002-3c-.552 0-1 .448-1 1s.448 1 1 1 1-.448 1-1-.448-1-1-1z" fill-rule="nonzero"/></svg>
              </div>
            </template>
            <template slot="package" slot-scope="{ item }">
              <NuxtLink :to="`/dependencies?package=${item.package}`">
                {{ item.package }}
              </NuxtLink>
            </template>
          </Table>
        </div>

        <div
          class="col-span-2 lg:col-span-1 w-full flex flex-col gap-3 overflow-x-auto"
        >
          <div class="w-full bg-white shadow-md rounded-xl px-3 py-3">
            <p class="underline">{{ $tc('image_id.active_vulnerability', 2) }} :</p>
            <Table
              :data="vulnActive"
              :columns="[
                { label: $t('image_id.cve'), name: 'name' },
                { label: $tc('image_id.package', 2), name: 'affected_package' },
                { label: $t('image_id.severity'), name: 'severity' },
                { label: $t('vulnerability.notes'), name: 'notes' },
              ]"
            >
              <template slot="name" slot-scope="{ item }">
                <NuxtLink :to="`/vulnerabilities?name=${item.name}`">
                  <p>{{ item.name }}</p>
                </NuxtLink>
              </template>
              <template slot="severity" slot-scope="{ item }">
                <div class="w-full flex justify-center">
                  <div
                    class="px-2 py-1 rounded-md text-white w-36 uppercase font-bold"
                    :class="colorSeverity(item)"
                  >
                    <p>
                      {{
                        $t(`vulnerability.state.${item.severity.toLowerCase()}`)
                      }}
                    </p>
                  </div>
                </div>
              </template>
              <template slot="notes" slot-scope="{ item }">
                <p class="text-clip">{{ copyNote[item.name] }}</p>
              </template>
              <template slot="affected_package" slot-scope="{ item }">
                <NuxtLink
                  :to="`/dependencies?package=${
                    currentImage.packages.find(
                      (el) => el.id === item.affected_package
                    ).package
                  }`"
                >
                  {{
                    currentImage.packages.find(
                      (el) => el.id === item.affected_package
                    ).package +
                    ':' +
                    currentImage.packages.find(
                      (el) => el.id === item.affected_package
                    ).version
                  }}
                </NuxtLink>
              </template>
            </Table>
          </div>
          <div
            class="col-span-2 lg:col-span-1 w-full bg-white shadow-md rounded-xl px-3 py-3 overflow-x-auto"
          >
            <p class="underline">{{ $tc('image_id.vulnerabilities', 2) }} :</p>
            <Table
              :data="vulnData"
              :columns="[
                { label: $t('image_id.cve'), name: 'name' },
                { label: $tc('image_id.package', 2), name: 'affected_package' },
                { label: $t('image_id.severity'), name: 'severity' },
                { label: $t('vulnerability.notes'), name: 'notes' },
              ]"
            >
              <template slot="name" slot-scope="{ item }">
                <NuxtLink :to="`/vulnerabilities?name=${item.name}`">
                  <p>{{ item.name }}</p>
                </NuxtLink>
              </template>
              <template slot="severity" slot-scope="{ item }">
                <div class="w-full flex justify-center">
                  <div
                    class="px-2 py-1 rounded-md text-white w-36 uppercase font-bold"
                    :class="colorSeverity(item)"
                  >
                    <p>
                      {{
                        $t(`vulnerability.state.${item.severity.toLowerCase()}`)
                      }}
                    </p>
                  </div>
                </div>
              </template>
              <template slot="affected_package" slot-scope="{ item }">
                <p class="text-clip">
                  {{
                    currentImage.packages.find(
                      (el) => el.id === item.affected_package
                    ).package +
                    ':' +
                    currentImage.packages.find(
                      (el) => el.id === item.affected_package
                    ).version
                  }}
                </p>
              </template>
              <template slot="notes" slot-scope="{ item }">
                <p class="text-clip">{{ copyNote[item.name] }}</p>
              </template>
            </Table>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { mapActions, mapState } from 'vuex'
import calcSize from '@/mixins/sizeCalc.js'

export default {
  name: 'ImageDetail',
  mixins: [calcSize],
  data() {
    return {
      isLoading: true,
      copyNote: [],
    }
  },
  computed: {
    ...mapState('image', ['currentImage']),
  },
  async mounted() {
    await this.getCurrentImage(this.$route.params.id).then(() => {
      this.tableData = [
        ...this.currentImage.outdated_packages,
        ...this.currentImage.packages,
      ]
      this.vulnData = [...this.currentImage.vulnerabilities]
      this.vulnActive = [...this.currentImage.active_vulnerabilities]
      this.vulnData.forEach((vuln) => {
        this.copyNote[vuln.name] = vuln.notes
      })
      this.isLoading = false
    })
  },
  methods: {
    ...mapActions('image', ['getCurrentImage', 'removeImg']),
    ...mapActions('vulnerability', ['setNotes']),
    selectColor(vuln, outdated) {
      if (vuln > 0) {
        return 'bg-red-400'
      }
      if (outdated > 0) {
        return 'bg-yellow-400'
      }
      return 'bg-green-400'
    },
    async deleteImg() {
      await this.removeImg(this.$route.params.id).then(() => {
        setTimeout(() => this.$router.push('/images'), 1500)
      })
    },
    sendNewNotes(item) {
      this.setNotes({
        cve: item.id,
        notes: this.copyNote[item.name],
        active: true,
      })
    },
    changeAckState(item) {
      this.setAckState({
        cve: item.id,
        notes: this.copyNote[item.name],
        active: !item.active,
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
  },
}
</script>
