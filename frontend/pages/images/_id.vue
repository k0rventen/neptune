<template>
  <div class="w-full h-screen overflow-y-auto scrollbar-thin">
    <Loading v-if="isLoading === true" />
    <div v-if="isLoading === false" class="mt-3 px-3">
      <div
        class="col-span-3 overflow-x-auto md:col-span-1 w-full cursor-pointer shadow-md bg-neptune-blue px-5 rounded-lg py-5 relative overflow-hidden bg-neptune-blue text-white"
      >
      <div class="w-2/3 grid grid-cols-2">
        <div>
          <p>
            Nom de l'image : {{ currentImage.image + ':' + currentImage.tag }}
          </p>
          <p>Taille de l'image : {{ calcSize(currentImage.size) }}</p>
          <p>
            Date d'ajout :
            {{
              new Date(currentImage.date_added).toLocaleDateString('fr-FR') +
              ' à ' +
              new Date(currentImage.date_added).toLocaleTimeString('fr-FR')
            }}
          </p>
          <p>Distribution : {{ currentImage.distro }}</p>
        </div>
        <div>
          <p>Paquets : {{ currentImage.packages.length }}</p>
          <p>Vulnérabilité(s) : {{ currentImage.vulnerabilities.length }}</p>
          <p>Vulnérabilité(s) active : {{ currentImage.active_vulnerabilities.length }}</p>
          <p>Paquet obsolète : {{ currentImage.outdated_packages.length }}</p>
        </div>
      </div>
        

        <svg
          class="absolute -bottom-2 right-0 opacity-20"
          xmlns="http://www.w3.org/2000/svg"
          width="128"
          height="128"
          viewBox="0 0 24 24"
          fill="white"
        >
          <path
            d="M12 0c-6.627 0-12 5.373-12 12s5.373 12 12 12 12-5.373 12-12-5.373-12-12-12zm-.001 5.75c.69 0 1.251.56 1.251 1.25s-.561 1.25-1.251 1.25-1.249-.56-1.249-1.25.559-1.25 1.249-1.25zm2.001 12.25h-4v-1c.484-.179 1-.201 1-.735v-4.467c0-.534-.516-.618-1-.797v-1h3v6.265c0 .535.517.558 1 .735v.999z"
          />
        </svg>
      </div>
      <div class="w-full grid grid-cols-2 gap-3 mt-3">
        <div
          class="col-span-2 lg:col-span-1 w-full bg-white shadow-md rounded-xl rounded-md px-3 py-3 overflow-x-auto"
        >
          <Table
            :data="tableData"
            :columns="[
              { label: 'Package', name: 'package' },
              { label: 'Version', name: 'version' },
              { label: 'Obsolète', name: 'outdated' }
            ]"
          >
            <template slot="outdated" slot-scope="{ item }">
              <div class="flex justify-center items-center">
                <svg
                  v-if="item.outdated"
                  clip-rule="evenodd"
                  fill-rule="evenodd"
                  stroke-linejoin="round"
                  stroke-miterlimit="2"
                  width="20"
                  height="20"
                  viewBox="0 0 24 24"
                  xmlns="http://www.w3.org/2000/svg"
                >
                  <path
                    d="m2.25 12.321 7.27 6.491c.143.127.321.19.499.19.206 0 .41-.084.559-.249l11.23-12.501c.129-.143.192-.321.192-.5 0-.419-.338-.75-.749-.75-.206 0-.411.084-.559.249l-10.731 11.945-6.711-5.994c-.144-.127-.322-.19-.5-.19-.417 0-.75.336-.75.749 0 .206.084.412.25.56"
                    fill-rule="nonzero"
                  />
                </svg>
                <svg
                  v-else
                  clip-rule="evenodd"
                  fill-rule="evenodd"
                  stroke-linejoin="round"
                  stroke-miterlimit="2"
                  width="20"
                  height="20"
                  viewBox="0 0 24 24"
                  xmlns="http://www.w3.org/2000/svg"
                >
                  <path
                    d="m12 10.93 5.719-5.72c.146-.146.339-.219.531-.219.404 0 .75.324.75.749 0 .193-.073.385-.219.532l-5.72 5.719 5.719 5.719c.147.147.22.339.22.531 0 .427-.349.75-.75.75-.192 0-.385-.073-.531-.219l-5.719-5.719-5.719 5.719c-.146.146-.339.219-.531.219-.401 0-.75-.323-.75-.75 0-.192.073-.384.22-.531l5.719-5.719-5.72-5.719c-.146-.147-.219-.339-.219-.532 0-.425.346-.749.75-.749.192 0 .385.073.531.219z"
                  />
                </svg>
              </div>
            </template>
            <template slot="package" slot-scope="{ item }">
              <NuxtLink :to="`/dependencies?package=${item.package}`">
                {{  item.package }}
              </NuxtLink>
            </template>
          </Table>
        </div>
        
        <div class="col-span-2 lg:col-span-1 w-full flex flex-col gap-3 overflow-x-auto">
          <div
          class="w-full bg-white shadow-md rounded-xl px-3 py-3"
        >
        <p class="underline">Vulnérabilité(s) active(s) : </p>
          <Table
            :data="vulnActive"
            :columns="[
              { label: 'CVE', name: 'name' },
              { label: 'Package', name: 'affected_package' },
              { label: 'Sévérité', name: 'severity' },
              { label: $t('vulnerability.notes'), name: 'notes' },
            ]"
          >
            <template slot="name" slot-scope="{ item }">
              <a
                :href="`https://www.google.com/search?q=${item.name}`"
                target="_blank"
              >
                <p>{{ item.name }}</p>
              </a>
            </template>
            <template slot="severity" slot-scope="{ item }">
              <p>
                {{ $t(`vulnerability.state.${item.severity.toLowerCase()}`) }}
              </p>
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
        <div
          class="col-span-2 lg:col-span-1 w-full bg-white shadow-md rounded-xl px-3 py-3 overflow-x-auto"
        >
          <p class="underline">Vulnérabilité(s): </p>
          <Table
            :data="vulnData"
            :columns="[
              { label: 'CVE', name: 'name' },
              { label: 'Package', name: 'affected_package' },
              { label: 'Sévérité', name: 'severity' },
              { label: $t('vulnerability.notes'), name: 'notes' },
            ]"
          >
            <template slot="name" slot-scope="{ item }">
              <a
                :href="`https://www.google.com/search?q=${item.name}`"
                target="_blank"
              >
                <p>{{ item.name }}</p>
              </a>
            </template>
            <template slot="severity" slot-scope="{ item }">
              <p>
                {{ $t(`vulnerability.state.${item.severity.toLowerCase()}`) }}
              </p>
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
      this.vulnData = [
        ...this.currentImage.vulnerabilities,
      ]
      this.vulnActive = [
        ...this.currentImage.active_vulnerabilities
      ]
      this.vulnData.forEach((vuln) => {
        this.copyNote[vuln.name] = vuln.notes
      })
      this.isLoading = false
    })
  },
  methods: {
    ...mapActions('image', ['getCurrentImage']),
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
    sendNewNotes(item) {
      this.setNotes({
        cve: item.id,
        notes: this.copyNote[item.name],
        active: true,
      })
    },
  },
}
</script>
