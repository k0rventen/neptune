<template>
  <div class="w-full h-screen px-5 mt-5 overflow-x-scroll">
    <div v-if="this.stats" class="grid grid-cols-4 gap-9">
      <div class="bg-white px-3 py-3 shadow-md rounded-xl flex justify-between text-secondary">
        <div>
          <p>Nombre total de vulnérabilités</p>
          <p class="font-bold">{{ this.stats.vulnerabilities_total_count }}</p>
        </div>
        <div class="bg-neptune-blue px-3 py-3 items-center justify-center rounded-xl">
          <svg class="rotate-45" fill="white" xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24"><path d="M7.074 1.408c0-.778.641-1.408 1.431-1.408.942 0 1.626.883 1.38 1.776-.093.336-.042.695.138.995.401.664 1.084 1.073 1.977 1.078.88-.004 1.572-.408 1.977-1.078.181-.299.231-.658.138-.995-.246-.892.436-1.776 1.38-1.776.79 0 1.431.63 1.431 1.408 0 .675-.482 1.234-1.118 1.375-.322.071-.6.269-.769.548-.613 1.017.193 1.917.93 2.823-1.21.562-2.524.846-3.969.846-1.468 0-2.771-.277-3.975-.84.748-.92 1.555-1.803.935-2.83-.168-.279-.446-.477-.768-.548-.636-.14-1.118-.699-1.118-1.374zm13.485 14.044h2.387c.583 0 1.054-.464 1.054-1.037s-.472-1.037-1.054-1.037h-2.402c-.575 0-1.137-.393-1.227-1.052-.092-.677.286-1.147.765-1.333l2.231-.866c.541-.21.807-.813.594-1.346-.214-.533-.826-.795-1.367-.584l-2.294.891c-.329.127-.734.036-.926-.401-.185-.423-.396-.816-.62-1.188-1.714.991-3.62 1.501-5.7 1.501-2.113 0-3.995-.498-5.703-1.496-.217.359-.421.738-.601 1.146-.227.514-.646.552-.941.437l-2.295-.89c-.542-.21-1.153.051-1.367.584-.213.533.053 1.136.594 1.346l2.231.866c.496.192.854.694.773 1.274-.106.758-.683 1.111-1.235 1.111h-2.402c-.582 0-1.054.464-1.054 1.037s.472 1.037 1.054 1.037h2.387c.573 0 1.159.372 1.265 1.057.112.728-.228 1.229-.751 1.462l-2.42 1.078c-.53.236-.766.851-.526 1.373s.865.753 1.395.518l2.561-1.14c.307-.137.688-.106.901.259 1.043 1.795 3.143 3.608 6.134 3.941 2.933-.327 5.008-2.076 6.073-3.837.261-.432.628-.514.963-.364l2.561 1.14c.529.236 1.154.005 1.395-.518.24-.522.004-1.137-.526-1.373l-2.42-1.078c-.495-.221-.867-.738-.763-1.383.128-.803.717-1.135 1.276-1.135z"/></svg>
        </div>
      </div>
      <div class="bg-white px-3 py-3 shadow-md rounded-xl flex justify-between text-secondary">
        <div>
          <p>Nombre total d'images</p>
          <p class="font-bold">{{ this.stats.tags_total_count }}</p>
        </div>
        <div class="bg-neptune-blue px-3 py-3 items-center justify-center rounded-xl">
          <svg width="24" height="24" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg" fill="white"><path d="M11.5 23l-8.5-4.535v-3.953l5.4 3.122 3.1-3.406v8.772zm1-.001v-8.806l3.162 3.343 5.338-2.958v3.887l-8.5 4.534zm-10.339-10.125l-2.161-1.244 3-3.302-3-2.823 8.718-4.505 3.215 2.385 3.325-2.385 8.742 4.561-2.995 2.771 2.995 3.443-2.242 1.241v-.001l-5.903 3.27-3.348-3.541 7.416-3.962-7.922-4.372-7.923 4.372 7.422 3.937v.024l-3.297 3.622-5.203-3.008-.16-.092-.679-.393v.002z"/></svg>
        </div>
      </div>
      <div class="bg-white px-3 py-3 shadow-md rounded-xl flex justify-between col-span-2 text-secondary">
        <div>
          <p>Nombre total de package</p>
          <p class="font-bold">{{ this.stats.packages_total_count }}</p>
        </div>
        <div class="bg-neptune-blue px-3 py-3 items-center justify-center rounded-xl">
          <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="white"><path d="M15.354 6h-3.554c-2.721-4.496-9.566-4.523-11.293-1.706-1.341 2.186.061 5.062 3.24 5.062 1.307 0 2.52-.593 4.253-.329v3.567l9.033 9.042 6.967-6.966-8.646-8.67zm-11.606 1.871c-1.996 0-2.738-1.6-1.956-2.835 1.076-1.701 5.756-1.94 8.19.964h-1.982v1.529c-1.922-.233-3.2.342-4.252.342zm9.207 2.645c-.817.817-2.206.394-2.446-.72 1.188.093 1.902-.723 1.795-1.708 1.071.285 1.445 1.634.651 2.428z"/></svg>
        </div>
      </div>
      <div class="bg-white px-3 py-3 h-96 shadow-md rounded-xl col-span-2 text-secondary">
        <p class="font-bold">Schéma de l'évolution des images au cours du temps </p>
        <apexchart v-if="tags.chartOptions.xaxis.categories.length === historicalStats?.length" height="90%" type="line" :options="tags.chartOptions" :series="tags.series"/>
      </div>
      <div class="bg-white px-3 py-3 h-96 shadow-md rounded-xl text-white">
        <div class="w-full h-full bg-neptune-blue rounded-xl px-5 py-5 relative overflow-hidden">
          <img class="absolute opacity-20 -right-24 -bottom-12" src="@/assets/img/docker.webp" alt="docker">
          <p class="font-bold text-3xl mb-5">What's is Neptune ?</p>
          <p>Neptune est un outils permettant d'avoir un visuelle sur les images de son parc.</p>
          <p>L'outils permet également de pouvoir configurer des alertes sur les versions de certain package</p>
          <p>Vous avez également accès à des graphiques de vos images.</p>
        </div>
      </div>
      <div class="bg-white px-3 py-3 h-96 shadow-md rounded-xl text-white flex justify-center items-center">
        <apexchart height="90%" type="radialBar" :options="vulnerabitily.chartOptions" :series="vulnerabitily.series"/>
      </div>
      <div class="bg-white px-3 py-3 h-96 shadow-md rounded-xl col-span-2 text-white">
        <apexchart v-if="severity.chartOptions.xaxis.categories.length === historicalStats?.length" height="90%" type="line" :options="severity.chartOptions" :series="severity.series"/>
      </div>
      <div class="bg-white px-3 py-3 h-96 shadow-md rounded-xl col-span-2 text-white">
        <apexchart v-if="followVuln.chartOptions.xaxis.categories.length === historicalStats?.length" height="90%" type="line" :options="followVuln.chartOptions" :series="followVuln.series"/>
      </div>
      <div class="bg-white px-3 py-3 shadow-md rounded-xl col-span-4 text-white grid grid-cols-5 gap-9">
        <div class="w-full bg-neptune-blue px-5 rounded-lg py-5 relative overflow-hidden">
          <svg class="absolute opacity-20 right-0 -bottom-8" width="128" height="128" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg" fill="white"><path d="M11.5 23l-8.5-4.535v-3.953l5.4 3.122 3.1-3.406v8.772zm1-.001v-8.806l3.162 3.343 5.338-2.958v3.887l-8.5 4.534zm-10.339-10.125l-2.161-1.244 3-3.302-3-2.823 8.718-4.505 3.215 2.385 3.325-2.385 8.742 4.561-2.995 2.771 2.995 3.443-2.242 1.241v-.001l-5.903 3.27-3.348-3.541 7.416-3.962-7.922-4.372-7.923 4.372 7.422 3.937v.024l-3.297 3.622-5.203-3.008-.16-.092-.679-.393v.002z"/></svg>
          <p>Nom de l'image : </p>
          <p>Taille de l'image : </p>
          <p>Paquets : </p>
          <p>Vulnérabilité :</p>
          <p>Paquet obsolète : </p>
        </div>
        <div class="w-full bg-neptune-blue px-5 rounded-lg py-5 relative overflow-hidden">
          <svg class="absolute opacity-20 right-0 -bottom-8" width="128" height="128" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg" fill="white"><path d="M11.5 23l-8.5-4.535v-3.953l5.4 3.122 3.1-3.406v8.772zm1-.001v-8.806l3.162 3.343 5.338-2.958v3.887l-8.5 4.534zm-10.339-10.125l-2.161-1.244 3-3.302-3-2.823 8.718-4.505 3.215 2.385 3.325-2.385 8.742 4.561-2.995 2.771 2.995 3.443-2.242 1.241v-.001l-5.903 3.27-3.348-3.541 7.416-3.962-7.922-4.372-7.923 4.372 7.422 3.937v.024l-3.297 3.622-5.203-3.008-.16-.092-.679-.393v.002z"/></svg>
          <p>Nom de l'image : </p>
          <p>Taille de l'image : </p>
          <p>Paquets : </p>
          <p>Vulnérabilité :</p>
          <p>Paquet obsolète : </p>
        </div>
        <div class="w-full bg-neptune-blue px-5 rounded-lg py-5 relative overflow-hidden">
          <svg class="absolute opacity-20 right-0 -bottom-8" width="128" height="128" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg" fill="white"><path d="M11.5 23l-8.5-4.535v-3.953l5.4 3.122 3.1-3.406v8.772zm1-.001v-8.806l3.162 3.343 5.338-2.958v3.887l-8.5 4.534zm-10.339-10.125l-2.161-1.244 3-3.302-3-2.823 8.718-4.505 3.215 2.385 3.325-2.385 8.742 4.561-2.995 2.771 2.995 3.443-2.242 1.241v-.001l-5.903 3.27-3.348-3.541 7.416-3.962-7.922-4.372-7.923 4.372 7.422 3.937v.024l-3.297 3.622-5.203-3.008-.16-.092-.679-.393v.002z"/></svg>
          <p>Nom de l'image : </p>
          <p>Taille de l'image : </p>
          <p>Paquets : </p>
          <p>Vulnérabilité :</p>
          <p>Paquet obsolète : </p>
        </div>
        <div class="w-full bg-neptune-blue px-5 rounded-lg py-5 relative overflow-hidden">
          <svg class="absolute opacity-20 right-0 -bottom-8" width="128" height="128" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg" fill="white"><path d="M11.5 23l-8.5-4.535v-3.953l5.4 3.122 3.1-3.406v8.772zm1-.001v-8.806l3.162 3.343 5.338-2.958v3.887l-8.5 4.534zm-10.339-10.125l-2.161-1.244 3-3.302-3-2.823 8.718-4.505 3.215 2.385 3.325-2.385 8.742 4.561-2.995 2.771 2.995 3.443-2.242 1.241v-.001l-5.903 3.27-3.348-3.541 7.416-3.962-7.922-4.372-7.923 4.372 7.422 3.937v.024l-3.297 3.622-5.203-3.008-.16-.092-.679-.393v.002z"/></svg>
          <p>Nom de l'image : </p>
          <p>Taille de l'image : </p>
          <p>Paquets : </p>
          <p>Vulnérabilité :</p>
          <p>Paquet obsolète : </p>
        </div>
        <div class="w-full bg-neptune-blue px-5 rounded-lg py-5 relative overflow-hidden">
          <svg class="absolute opacity-20 right-0 -bottom-8" width="128" height="128" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg" fill="white"><path d="M11.5 23l-8.5-4.535v-3.953l5.4 3.122 3.1-3.406v8.772zm1-.001v-8.806l3.162 3.343 5.338-2.958v3.887l-8.5 4.534zm-10.339-10.125l-2.161-1.244 3-3.302-3-2.823 8.718-4.505 3.215 2.385 3.325-2.385 8.742 4.561-2.995 2.771 2.995 3.443-2.242 1.241v-.001l-5.903 3.27-3.348-3.541 7.416-3.962-7.922-4.372-7.923 4.372 7.422 3.937v.024l-3.297 3.622-5.203-3.008-.16-.092-.679-.393v.002z"/></svg>
          <p>Nom de l'image : </p>
          <p>Taille de l'image : </p>
          <p>Paquets : </p>
          <p>Vulnérabilité :</p>
          <p>Paquet obsolète : </p>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { mapState, mapActions } from "vuex";

export default {
  name: 'IndexPage',
  data() {
    return {
      imageVuln: {
        chartOptions: {
          legend: {
            show: false,
          },
          maintainAspectRatio: false,
          labels: ['Vulnerable', 'Oudated', 'Secure'],
          chart: {
            type: 'donut',
          },
        },
        series: [],
      },
      vulnerabitily: {
        chartOptions: {
          labels: [],
          chart: {
            type: 'donut',
          },
          responsive: [{
            breakpoint: 480,
            options: {
              chart: {
                width: 200
              },
              legend: {
                position: 'bottom'
              }
            }
          }]
        },
        series: [],
      },
      followVuln: {
        series: [
          {
          name: "Nombre de package",
          data: []
          },
          {
            name: "Package outdated",
            data: []
          },
          {
            name: "Package vulnérable",
            data: []
          },
        ],
        chartOptions: {
          colors: ['#008FFB', '#FF4560', '#FEB019'],
          chart: {
            height: 350,
            type: 'line',
            zoom: {
              enabled: false
            }
          },
          dataLabels: {
            enabled: false
          },
          stroke: {
            curve: 'smooth'
          },
          grid: {
            row: {
              colors: ['#f3f3f3', 'transparent'], // takes an array which will be repeated on columns
              opacity: 0.5
            },
          },
          xaxis: {
            labels: {
              show: false,
            },
            categories: [],
          }
        },
      },
      severity: {
        series: [
          {
            name: "Vulnérabilitée total",
            data: []
          },
          {
            name: "Vulnérabiilitée active",
            data: []
          },
          {
            name: "Vulnérabilité basse",
            data: []
          },
          {
            name: "Vulnérabilité moyenne",
            data: []
          },
          {
            name: "Vulnérabilité haute",
            data: []
          },
          {
            name: "Vulnérabilité critique",
            data: []
          },
        ],
        chartOptions: {
          colors: ['#008FFB', '#FF4560', '#FEB019', '#546E7A', '#32c259' , '#8d2aa1' ],
          chart: {
            height: 350,
            type: 'line',
            zoom: {
              enabled: false
            }
          },
          dataLabels: {
            enabled: false
          },
          stroke: {
            curve: 'smooth'
          },
          grid: {
            row: {
              colors: ['#f3f3f3', 'transparent'], // takes an array which will be repeated on columns
              opacity: 0.5
            },
          },
          xaxis: {
            labels: {
              show: false,
            },
            categories: [],
          }
        },
      },
      tags: {
        series: [
          {
            name: "Images total",
            data: []
          },
          {
            name: "Images avec vulnerabilité",
            data: []
          },
          {
            name: "Images outdated",
            data: []
          },
        ],
        chartOptions: {
          colors: ['#008FFB', '#FF4560', '#FEB019'],
          chart: {
            height: 350,
            type: 'line',
            zoom: {
              enabled: false
            }
          },
          dataLabels: {
            enabled: false
          },
          stroke: {
            curve: 'smooth'
          },
          grid: {
            row: {
              colors: ['#f3f3f3', 'transparent'], // takes an array which will be repeated on columns
              opacity: 0.5
            },
          },
          xaxis: {
            labels: {
              show: false
            },
            categories: [],
          }
        },
      }
    }
  },
  methods: {
    ...mapActions('statistics', ['getStats', 'getHistoricalStats']),
    convertDate(date) {
      const options = { year: 'numeric', month: 'long', day: 'numeric', hour: 'numeric', minute: 'numeric' };
      return new Date(date).toLocaleDateString('fr-FR', options)
    },
  },
  computed: {
    ...mapState('statistics', ['stats', 'historicalStats']),
  },
  async mounted() {
    await this.getStats().then(() => {
      this.imageVuln.series = [this.stats.vulnerable_tags_count, this.stats.outdated_tags_count, this.tags_total_count - ( this.stats.vulnerable_tags_count + this.stats.outdated_tags_count )]
      for(const [key, value] of Object.entries(this.stats.severities)) {
        this.vulnerabitily.chartOptions.labels.push(key)
        this.vulnerabitily.series.push(Math.ceil((value / this.stats.vulnerabilities_total_count) * 100))
      }
    });
    await this.getHistoricalStats().then(() => {
      this.historicalStats.forEach((el) => {
        this.followVuln.chartOptions.xaxis.categories.push(this.convertDate(el.timestamp))
        this.followVuln.series[0].data.push(el.packages_total_count)
        this.followVuln.series[1].data.push(el.outdated_packages_count)
        this.followVuln.series[2].data.push(el.vulnerable_packages_count)

        this.severity.chartOptions.xaxis.categories.push(this.convertDate(el.timestamp))
        this.severity.series[0].data.push(el.vulnerabilities_total_count)
        this.severity.series[1].data.push(el.active_vulnerabilities_count)
        this.severity.series[2].data.push(el.low_vulnerabilities_count)
        this.severity.series[3].data.push(el.medium_vulnerabilities_count)
        this.severity.series[4].data.push(el.high_vulnerabilities_count)
        this.severity.series[5].data.push(el.critical_vulnerabilities_count)

        this.tags.chartOptions.xaxis.categories.push(this.convertDate(el.timestamp))
        this.tags.series[0].data.push(el.tags_total_count)
        this.tags.series[1].data.push(el.vulnerable_tags_count)
        this.tags.series[2].data.push(el.outdated_tags_count)
      })
    })
  },
}
</script>
