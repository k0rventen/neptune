<template>
  <div class="w-full pb-24 lg:pb-5 h-screen px-5 py-5 overflow-y-auto scrollbar-thin">
    <Loading v-if="isLoading" />
    <Modal
      v-if="openRegistriesModal"
      v-model="openRegistriesModal"
      title="Éditions des registries"
    >
      <div class="h-2/3 px-3 py-3 border border-gray-300 my-2 rounded-xl">
        <div class="grid grid-cols-3 gap-5">
          <div
            v-for="registry in registries"
            :key="registry.url"
            class="text-white px-5 rounded-lg py-5 overflow-hidden cursor-pointer bg-neptune-blue relative"
          >
            <svg
              class="absolute opacity-20 -right-5 -bottom-5"
              width="116"
              height="116"
              viewBox="0 0 24 24"
              fill="white"
            >
              <path
                d="M18 10.031v-6.423l-6.036-3.608-5.964 3.569v6.499l-6 3.224v7.216l6.136 3.492 5.864-3.393 5.864 3.393 6.136-3.492v-7.177l-6-3.3zm-1.143.036l-4.321 2.384v-4.956l4.321-2.539v5.111zm-4.895-8.71l4.272 2.596-4.268 2.509-4.176-2.554 4.172-2.551zm-10.172 12.274l4.778-2.53 4.237 2.417-4.668 2.667-4.347-2.554zm4.917 3.587l4.722-2.697v5.056l-4.722 2.757v-5.116zm6.512-3.746l4.247-2.39 4.769 2.594-4.367 2.509-4.649-2.713zm9.638 6.323l-4.421 2.539v-5.116l4.421-2.538v5.115z"
              />
            </svg>
            <p class="truncate">URL : {{ registry.registry }}</p>
            <p class="truncate">Utilisateur : {{ registry.user }}</p>
            <p class="truncate">Mot de passe : {{ registry.password }}</p>
          </div>
        </div>
      </div>
      <div class="h-1/3 px-3 py-3">
        <form @submit.prevent="sendRegisteriesData()">
          <label class="mb-2 gap-3">
            URL :
            <input
              v-model="registry.url"
              type="text"
              class="rounded-md border border-gray-400 outline-none px-2 py-1"
            />
          </label>

          <label for="" class="my-2 gap-3 block">
            Nom d'utilisateur :
            <input
              v-model="registry.user"
              type="text"
              class="rounded-md border border-gray-400 outline-none px-2 py-1"
            />
          </label>

          <label for="" class="mb-2 gap-3 block">
            Mot de passe
            <input
              v-model="registry.password"
              type="password"
              class="rounded-md border border-gray-400 outline-none px-2 py-1"
            />
          </label>
          <button
            type="submit"
            class="px-3 py-1 rounded-md bg-neptune-blue text-white"
          >
            Envoyer
          </button>
        </form>
      </div>
    </Modal>
    <Modal
      v-if="openImagesModal"
      v-model="openImagesModal"
      title="Ajout d'une image en direct"
    >
      <label for="" class="my-2 gap-3 block">
        Nom de l'image :
        <input
              v-model="imageName"
              type="text"
              class="rounded-md border border-gray-400 outline-none px-2 py-1"
            />
      </label>
      <template #footer>
        <button
          class="px-3 py-1 rounded-md bg-neptune-blue text-white"
          @click="sendNewImage()"
        >
          Envoyer
        </button>
      </template>
    </Modal>
    <div v-if="stats" class="grid grid-cols-4 gap-9">
      <div
        class="bg-white px-3 py-3 shadow-md rounded-xl flex justify-between text-secondary col-span-4 lg:col-span-1"
      >
        <div>
          <p>Nombre total de vulnérabilités</p>
          <p class="font-bold">{{ stats.vulnerabilities_total_count }}</p>
        </div>
        <div
          class="bg-neptune-blue px-3 py-3 items-center justify-center rounded-xl max-h-fit"
        >
          <svg
            class="rotate-45"
            fill="white"
            xmlns="http://www.w3.org/2000/svg"
            width="24"
            height="24"
            viewBox="0 0 24 24"
          >
            <path
              d="M7.074 1.408c0-.778.641-1.408 1.431-1.408.942 0 1.626.883 1.38 1.776-.093.336-.042.695.138.995.401.664 1.084 1.073 1.977 1.078.88-.004 1.572-.408 1.977-1.078.181-.299.231-.658.138-.995-.246-.892.436-1.776 1.38-1.776.79 0 1.431.63 1.431 1.408 0 .675-.482 1.234-1.118 1.375-.322.071-.6.269-.769.548-.613 1.017.193 1.917.93 2.823-1.21.562-2.524.846-3.969.846-1.468 0-2.771-.277-3.975-.84.748-.92 1.555-1.803.935-2.83-.168-.279-.446-.477-.768-.548-.636-.14-1.118-.699-1.118-1.374zm13.485 14.044h2.387c.583 0 1.054-.464 1.054-1.037s-.472-1.037-1.054-1.037h-2.402c-.575 0-1.137-.393-1.227-1.052-.092-.677.286-1.147.765-1.333l2.231-.866c.541-.21.807-.813.594-1.346-.214-.533-.826-.795-1.367-.584l-2.294.891c-.329.127-.734.036-.926-.401-.185-.423-.396-.816-.62-1.188-1.714.991-3.62 1.501-5.7 1.501-2.113 0-3.995-.498-5.703-1.496-.217.359-.421.738-.601 1.146-.227.514-.646.552-.941.437l-2.295-.89c-.542-.21-1.153.051-1.367.584-.213.533.053 1.136.594 1.346l2.231.866c.496.192.854.694.773 1.274-.106.758-.683 1.111-1.235 1.111h-2.402c-.582 0-1.054.464-1.054 1.037s.472 1.037 1.054 1.037h2.387c.573 0 1.159.372 1.265 1.057.112.728-.228 1.229-.751 1.462l-2.42 1.078c-.53.236-.766.851-.526 1.373s.865.753 1.395.518l2.561-1.14c.307-.137.688-.106.901.259 1.043 1.795 3.143 3.608 6.134 3.941 2.933-.327 5.008-2.076 6.073-3.837.261-.432.628-.514.963-.364l2.561 1.14c.529.236 1.154.005 1.395-.518.24-.522.004-1.137-.526-1.373l-2.42-1.078c-.495-.221-.867-.738-.763-1.383.128-.803.717-1.135 1.276-1.135z"
            />
          </svg>
        </div>
      </div>
      <div
        class="bg-white px-3 py-3 shadow-md rounded-xl flex justify-between text-secondary col-span-4 lg:col-span-1"
      >
        <div>
          <p>Nombre total d'images</p>
          <p class="font-bold">{{ stats.tags_total_count }}</p>
        </div>
        <div
          class="bg-neptune-blue px-3 py-3 items-center justify-center rounded-xl"
        >
          <svg
            width="24"
            height="24"
            viewBox="0 0 24 24"
            xmlns="http://www.w3.org/2000/svg"
            fill="white"
          >
            <path
              d="M11.5 23l-8.5-4.535v-3.953l5.4 3.122 3.1-3.406v8.772zm1-.001v-8.806l3.162 3.343 5.338-2.958v3.887l-8.5 4.534zm-10.339-10.125l-2.161-1.244 3-3.302-3-2.823 8.718-4.505 3.215 2.385 3.325-2.385 8.742 4.561-2.995 2.771 2.995 3.443-2.242 1.241v-.001l-5.903 3.27-3.348-3.541 7.416-3.962-7.922-4.372-7.923 4.372 7.422 3.937v.024l-3.297 3.622-5.203-3.008-.16-.092-.679-.393v.002z"
            />
          </svg>
        </div>
      </div>
      <div
        class="bg-white px-3 py-3 shadow-md rounded-xl flex justify-between text-secondary col-span-4 lg:col-span-2"
      >
        <div>
          <p>Nombre total de package</p>
          <p class="font-bold">{{ stats.packages_total_count }}</p>
        </div>
        <div
          class="bg-neptune-blue px-3 py-3 items-center justify-center rounded-xl"
        >
          <svg
            xmlns="http://www.w3.org/2000/svg"
            width="24"
            height="24"
            viewBox="0 0 24 24"
            fill="white"
          >
            <path
              d="M15.354 6h-3.554c-2.721-4.496-9.566-4.523-11.293-1.706-1.341 2.186.061 5.062 3.24 5.062 1.307 0 2.52-.593 4.253-.329v3.567l9.033 9.042 6.967-6.966-8.646-8.67zm-11.606 1.871c-1.996 0-2.738-1.6-1.956-2.835 1.076-1.701 5.756-1.94 8.19.964h-1.982v1.529c-1.922-.233-3.2.342-4.252.342zm9.207 2.645c-.817.817-2.206.394-2.446-.72 1.188.093 1.902-.723 1.795-1.708 1.071.285 1.445 1.634.651 2.428z"
            />
          </svg>
        </div>
      </div>
      <div
        class="bg-white px-3 py-3 h-96 shadow-md rounded-xl col-span-4 lg:col-span-2 text-secondary"
      >
        <apexchart
          v-if="
            tags.chartOptions.xaxis.categories.length ===
            historicalStats?.length
          "
          height="90%"
          type="line"
          :options="tags.chartOptions"
          :series="tags.series"
        />
      </div>
      <div
        class="bg-white px-3 py-3 h-96 shadow-md rounded-xl text-white flex justify-center items-center col-span-4 lg:col-span-2"
      >
        <apexchart
          height="90%"
          type="radialBar"
          :options="vulnerabitily.chartOptions"
          :series="vulnerabitily.series"
        />
      </div>
      <div
        class="bg-white px-3 py-3 h-96 shadow-md rounded-xl col-span-4 lg:col-span-2 text-white"
      >
        <apexchart
          v-if="
            severity.chartOptions.xaxis.categories.length ===
            historicalStats?.length
          "
          height="90%"
          type="line"
          :options="severity.chartOptions"
          :series="severity.series"
        />
      </div>
      <div
        class="bg-white px-3 py-3 h-96 shadow-md rounded-xl col-span-4 lg:col-span-2 text-white"
      >
        <apexchart
          v-if="
            followVuln.chartOptions.xaxis.categories.length ===
            historicalStats?.length
          "
          height="90%"
          type="line"
          :options="followVuln.chartOptions"
          :series="followVuln.series"
        />
      </div>
      <div class="bg-white px-3 py-3 shadow-md rounded-xl col-span-4">
        <div class="w-full block md:flex justify-between">
          <p class="mb-3 text-gray-400 underline">Images critiques :</p>
          <div class="flex gap-3">
            <div class="flex items-center gap-1">
              <div class="h-3 w-3 rounded-sm bg-black"></div>
              <p class="text-xs">Le plus de vulnérabilités actives</p>
            </div>
            <div class="flex items-center gap-1">
              <div class="h-3 w-3 rounded-sm bg-red-500"></div>
              <p class="text-xs">Le plus de vulnérabilités</p>
            </div>
            <div class="flex items-center gap-1">
              <div class="h-3 w-3 rounded-sm bg-yellow-400"></div>
              <p class="text-xs">Le plus de package obsolète</p>
            </div>
            <div class="flex items-center gap-1">
              <div class="h-3 w-3 rounded-sm bg-green-500"></div>
              <p class="text-xs">Le plus de package</p>
            </div>
          </div>
        </div>
        <div class="text-white grid grid-cols-4 gap-9">
          <div
            v-for="(image, index) in fiveImg"
            :key="image.image_id"
            class="px-5 rounded-lg py-5 relative overflow-hidden cursor-pointer col-span-4 lg:col-span-1"
            :class="setBgColor(index)"
            @click="$router.push({ path: '/images/' + image.sha })"
          >
            <svg
              v-if="index === 0"
              class="absolute opacity-20 right-0 -bottom-2"
              enable-background="new 0 0 274.989 274.989"
              version="1.1"
              viewBox="0 0 274.99 274.99"
              width="128"
              height="128"
              fill="white"
            >
              <path
                d="m179.57 216.04c-5.609 11.237-8.425 16.844-14.02 19.641-5.609 5.603-16.837 5.603-28.068 5.603-14.02 0-22.432 0-28.038-5.603-5.624-2.797-8.432-8.404-14.03-19.641 0 0-2.816-2.781-2.816-5.611l-11.228 2.83 8.429 28.025 16.827 14.049c5.598 14.022 16.835 19.652 30.855 19.652 5.609 0 14.039-2.836 16.835-5.63 5.623-2.816 11.232-8.415 14.04-14.022l16.826-14.049 8.425-28.025-11.222-2.83c-2.815 2.83-2.815 5.611-2.815 5.611zm30.891-190.78c-19.664-16.818-42.103-25.266-72.978-25.266-30.855 0-53.295 8.448-72.948 25.266-16.831 14.021-28.039 36.463-28.039 61.743 0 22.422 2.787 39.249 8.4 47.7 8.426 14.008 14.04 22.428 14.04 28.032l2.797 22.43 39.28 19.663 8.432 16.84c2.782 0 5.607 0 11.222 2.797h16.817c14.039 0 22.459-2.797 30.875-2.797l5.603-16.84 39.291-19.663 2.796-22.43c2.818-5.604 2.818-8.426 2.818-11.216 14.018-19.648 19.633-42.094 19.633-64.517-1e-3 -25.279-8.411-47.721-28.039-61.742zm-115.05 137.48c-16.845 0-22.44-11.216-22.44-28.032 0-8.451 0-16.867 5.595-19.652 2.802-5.626 8.434-8.415 16.845-8.415 16.812 0 25.252 8.415 25.252 25.237 0 19.646-8.44 30.862-25.252 30.862zm50.509 30.855c-2.831 0-5.633 0-8.44-2.806-2.817 2.806-2.817 2.806-5.595 2.806-2.836 0-5.609 0-8.425-2.806-2.797 0-2.797-2.791-2.797-5.618 0-2.776 2.797-8.387 5.613-11.198 5.609-5.621 8.387-11.232 11.204-16.837 2.807 5.604 8.44 11.216 11.231 16.837 5.604 2.811 5.604 8.422 5.604 11.198 0 5.618-2.797 8.424-8.395 8.424zm36.464-30.855c-16.837 0-25.263-11.216-25.263-28.032 0-16.867 8.426-28.068 25.263-28.068 8.409 0 14.018 2.79 16.826 8.415 5.613 2.785 5.613 8.411 5.613 16.821-1e-3 19.648-8.421 30.864-22.439 30.864z"
                fill="white"
              />
            </svg>
            <svg
              v-if="index === 1"
              class="absolute opacity-20 right-0 -bottom-2"
              width="128"
              height="128"
              viewBox="0 0 24 24"
              xmlns="http://www.w3.org/2000/svg"
              fill-rule="evenodd"
              clip-rule="evenodd"
              fill="white"
            >
              <path
                d="M21.167 21h1.833v2h-22v-2h1.833l7.334-20h3.666l7.334 20zm-4.527-7h-9.274l-1.005 3h11.328l-1.049-3zm-2.919-8h-3.471l-1.005 3h5.525l-1.049-3z"
              />
            </svg>
            <svg
              v-if="index === 2"
              class="absolute opacity-20 right-0 -bottom-3"
              width="128"
              height="128"
              viewBox="0 0 24 24"
              clip-rule="evenodd"
              fill="white"
              stroke-linejoin="round"
              stroke-miterlimit="2"
              xmlns="http://www.w3.org/2000/svg"
            >
              <path
                d="m2.095 19.886 9.248-16.5c.133-.237.384-.384.657-.384.272 0 .524.147.656.384l9.248 16.5c.064.115.096.241.096.367 0 .385-.309.749-.752.749h-18.496c-.44 0-.752-.36-.752-.749 0-.126.031-.252.095-.367zm1.935-.384h15.939l-7.97-14.219zm7.972-6.497c-.414 0-.75.336-.75.75v3.5c0 .414.336.75.75.75s.75-.336.75-.75v-3.5c0-.414-.336-.75-.75-.75zm-.002-3c.552 0 1 .448 1 1s-.448 1-1 1-1-.448-1-1 .448-1 1-1z"
                fill-rule="nonzero"
              />
            </svg>
            <svg
              v-if="index === 3"
              class="absolute opacity-20 right-0 -bottom-8"
              width="128"
              height="128"
              viewBox="0 0 24 24"
              xmlns="http://www.w3.org/2000/svg"
              fill="white"
            >
              <path
                d="M11.5 23l-8.5-4.535v-3.953l5.4 3.122 3.1-3.406v8.772zm1-.001v-8.806l3.162 3.343 5.338-2.958v3.887l-8.5 4.534zm-10.339-10.125l-2.161-1.244 3-3.302-3-2.823 8.718-4.505 3.215 2.385 3.325-2.385 8.742 4.561-2.995 2.771 2.995 3.443-2.242 1.241v-.001l-5.903 3.27-3.348-3.541 7.416-3.962-7.922-4.372-7.923 4.372 7.422 3.937v.024l-3.297 3.622-5.203-3.008-.16-.092-.679-.393v.002z"
              />
            </svg>
            <p>Nom de l'image : {{ image.image + ':' + image.tag }}</p>
            <p>Taille de l'image : {{ calcSize(image.size) }}</p>
            <p>Paquets : {{ image.packages }}</p>
            <p>Vulnérabilité : {{ image.vulnerabilities }}</p>
            <p>Paquet obsolète : {{ image.outdated_packages }}</p>
          </div>
        </div>
      </div>
    </div>
    <div class="w-full grid grid-cols-1 lg:grid-cols-3 mt-3 lg:mt-9 gap-3 lg:gap-9">
      <button
        class="w-full shadow-md rounded-xl bg-neptune-blue text-white px-3 py-2 col-span-3 lg:col-span-1"
        @click="openRegistriesModal = true"
      >
        Ajouter un registry
      </button>
      <button
        class="w-full shadow-md rounded-xl bg-neptune-blue text-white px-3 py-2 col-span-3 lg:col-span-1"
        @click="openImagesModal = true"
      >
        Ajouter une image
      </button>
    </div>
  </div>
</template>

<script>
import { mapState, mapActions } from 'vuex'
import calcSize from '@/mixins/sizeCalc.js'

export default {
  name: 'IndexPage',
  mixins: [calcSize],
  data() {
    return {
      vulnerabitily: {
        chartOptions: {
          labels: [],
          title: {
            text: 'Sévérité des vulnérabilités',
            align: 'center',
            style: {
              fontSize: '14px',
              fontWeight: 'regular',
              fontFamily: undefined,
              color: '#263238'
            }
          },
          chart: {
            type: 'donut',
          },
          legend: {
            show: true,
            position: 'bottom',
          },
          responsive: [
            {
              breakpoint: 480,
              options: {
                chart: {
                  width: 200,
                },
                legend: {
                  position: 'bottom',
                },
              },
            },
          ],
        },
        series: [],
      },
      followVuln: {
        series: [
          {
            name: 'Nombre de package',
            data: [],
          },
          {
            name: 'Package outdated',
            data: [],
          },
          {
            name: 'Package vulnérable',
            data: [],
          },
        ],
        chartOptions: {
          title: {
            text: 'Suivi des stats de package',
            align: 'center',
            style: {
              fontSize: '14px',
              fontWeight: 'regular',
              fontFamily: undefined,
              color: '#263238'
            }
          },
          colors: ['#008FFB', '#FF4560', '#FEB019'],
          chart: {
            height: 350,
            type: 'line',
            zoom: {
              enabled: false,
            },
          },
          dataLabels: {
            enabled: false,
          },
          stroke: {
            curve: 'smooth',
          },
          grid: {
            row: {
              colors: ['#f3f3f3', 'transparent'], // takes an array which will be repeated on columns
              opacity: 0.5,
            },
          },
          xaxis: {
            labels: {
              show: false,
            },
            categories: [],
          },
        },
      },
      severity: {
        series: [
          {
            name: 'Vulnérabilitée total',
            data: [],
          },
          {
            name: 'Vulnérabiilitée active',
            data: [],
          },
          {
            name: 'Vulnérabilité basse',
            data: [],
          },
          {
            name: 'Vulnérabilité moyenne',
            data: [],
          },
          {
            name: 'Vulnérabilité haute',
            data: [],
          },
          {
            name: 'Vulnérabilité critique',
            data: [],
          },
        ],
        chartOptions: {
          title: {
            text: 'Suivi des vulnérabilités',
            align: 'center',
            style: {
              fontSize: '14px',
              fontWeight: 'regular',
              fontFamily: undefined,
              color: '#263238'
            }
          },
          colors: [
            '#008FFB',
            '#FF4560',
            '#FEB019',
            '#546E7A',
            '#32c259',
            '#8d2aa1',
          ],
          chart: {
            height: 350,
            type: 'line',
            zoom: {
              enabled: false,
            },
          },
          dataLabels: {
            enabled: false,
          },
          stroke: {
            curve: 'smooth',
          },
          grid: {
            row: {
              colors: ['#f3f3f3', 'transparent'], // takes an array which will be repeated on columns
              opacity: 0.5,
            },
          },
          xaxis: {
            labels: {
              show: false,
            },
            categories: [],
          },
        },
      },
      tags: {
        series: [
          {
            name: 'Images total',
            data: [],
          },
          {
            name: 'Images avec vulnerabilité',
            data: [],
          },
          {
            name: 'Images outdated',
            data: [],
          },
        ],
        chartOptions: {
          title: {
            text: 'Suivi des stats d\'image',
            align: 'center',
            style: {
              fontSize: '14px',
              fontWeight: 'regular',
              fontFamily: undefined,
              color: '#263238'
            }
          },
          colors: ['#008FFB', '#FF4560', '#FEB019'],
          chart: {
            height: 350,
            type: 'line',
            zoom: {
              enabled: false,
            },
          },
          dataLabels: {
            enabled: false,
          },
          stroke: {
            curve: 'smooth',
          },
          grid: {
            row: {
              colors: ['#f3f3f3', 'transparent'], // takes an array which will be repeated on columns
              opacity: 0.5,
            },
          },
          xaxis: {
            labels: {
              show: false,
            },
            categories: [],
          },
        },
      },
      openRegistriesModal: false,
      openImagesModal: false,
      registry: {
        registry: '',
        user: '',
        password: '',
      },
      imageName: undefined,
      isLoading: false
    }
  },
  computed: {
    ...mapState('statistics', ['stats', 'historicalStats', 'fiveImg']),
    ...mapState('registries', ['registries']),
  },
  async mounted() {
    await this.getRegistries()
    await this.getStats().then(() => {
      for (const [key, value] of Object.entries(this.stats.severities)) {
        this.vulnerabitily.chartOptions.labels.push(key)
        this.vulnerabitily.series.push(
          Math.ceil((value / this.stats.vulnerabilities_total_count) * 100)
        )
      }
    })
    await this.getFiveImg()
    await this.getHistoricalStats().then(() => {
      this.historicalStats.forEach((el) => {
        this.followVuln.chartOptions.xaxis.categories.push(
          this.convertDate(el.timestamp)
        )
        this.followVuln.series[0].data.push(el.packages_total_count)
        this.followVuln.series[1].data.push(el.outdated_packages_count)
        this.followVuln.series[2].data.push(el.vulnerable_packages_count)

        this.severity.chartOptions.xaxis.categories.push(
          this.convertDate(el.timestamp)
        )
        this.severity.series[0].data.push(el.vulnerabilities_total_count)
        this.severity.series[1].data.push(el.active_vulnerabilities_count)
        this.severity.series[2].data.push(el.low_vulnerabilities_count)
        this.severity.series[3].data.push(el.medium_vulnerabilities_count)
        this.severity.series[4].data.push(el.high_vulnerabilities_count)
        this.severity.series[5].data.push(el.critical_vulnerabilities_count)

        this.tags.chartOptions.xaxis.categories.push(
          this.convertDate(el.timestamp)
        )
        this.tags.series[0].data.push(el.tags_total_count)
        this.tags.series[1].data.push(el.vulnerable_tags_count)
        this.tags.series[2].data.push(el.outdated_tags_count)
      })
    })
  },
  methods: {
    ...mapActions('statistics', [
      'getStats',
      'getHistoricalStats',
      'getFiveImg',
    ]),
    ...mapActions('image', ['scanImages']),
    ...mapActions('registries', ['getRegistries', 'sendRegistry']),
    convertDate(date) {
      const options = {
        year: 'numeric',
        month: 'long',
        day: 'numeric',
        hour: 'numeric',
        minute: 'numeric',
      }
      return new Date(date).toLocaleDateString('fr-FR', options)
    },
    setBgColor(index) {
      switch (index) {
        case 0:
          return 'bg-black'
        case 1:
          return 'bg-red-500'
        case 2:
          return 'bg-yellow-400'
        case 3:
          return 'bg-green-500'
      }
    },
    async sendRegisteriesData() {
      await this.sendRegistry(this.registry)
      this.registry = {
        url: '',
        user: '',
        password: '',
      }
      this.openRegistriesModal = false
    },
    async sendNewImage() {
      this.isLoading = true
      this.openImagesModal = false
      await this.scanImages({image: this.imageName, return_error: false}).then(() => {
        this.imageName = undefined
        this.isLoading = false
      })
    }
  },
}
</script>
