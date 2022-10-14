<template>
  <div v-if="stats" class="flex flex-col gap-3 w-full h-[calc(100vh-72px)] px-3 py-3">
    <div class="w-full h-full grid lg:grid-cols-3 grid-cols-1 grid-rows-2 gap-3">
      <!-- Image vulnerability -->
      <div class="w-full lg:h-auto">
        <card class="h-full" :header="$tc('card.image_vulnerability')">
          <div class="w-full h-full flex justify-center items-center">
            <apexchart height="90%" type="donut" :options="imageVuln.chartOptions" :series="imageVuln.series"/>
          </div>
        </card>
      </div>

      <!-- Number of vulnerability with severity -->
      <div class="mt-3 lg:mt-0 w-full lg:h-auto">
        <card class="h-full" :header="$t('card.vulnerability')">
          <div class="w-full h-full flex justify-center items-center">
            <apexchart height="90%" type="radialBar" :options="vulnerabitily.chartOptions" :series="vulnerabitily.series"/>
          </div>
        </card>
      </div>

      <!-- Image top 5 -->
      <div class="w-full h-full">
        <card class="h-full" :header="$t('card.follow_up_vulnerability_package')">

        </card>
      </div>

      <!-- Evolution of vulnerability -->
      <div class="w-full h-full">
        <card class="h-full" :header="$t('card.follow_up_vulnerability_package')">
          <apexchart v-if="followVuln.chartOptions.xaxis.categories.length === historicalStats?.length" height="90%" type="line" :options="followVuln.chartOptions" :series="followVuln.series"/>
        </card>
      </div>
      <div class="w-full h-full">
        <card class="h-full" :header="$t('card.follow_up_severity')">
          <apexchart v-if="severity.chartOptions.xaxis.categories.length === historicalStats?.length" height="90%" type="line" :options="severity.chartOptions" :series="severity.series"/>
        </card>
      </div>
      <div class="w-full h-full">
        <card class="h-full" :header="$t('card.follow_up_vulnerability_tags')">
          <apexchart v-if="tags.chartOptions.xaxis.categories.length === historicalStats?.length" height="90%" type="line" :options="tags.chartOptions" :series="tags.series"/>
        </card>
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
      this.imageVuln.series = [this.stats.tags.with_vulnerabilities, this.stats.tags.with_outdated_packages, this.stats.tags.total - ( this.stats.tags.with_vulnerabilities + this.stats.tags.with_outdated_packages )]
      for(const [key, value] of Object.entries(this.stats.vulnerabilities.severities)) {
        this.vulnerabitily.chartOptions.labels.push(key)
        this.vulnerabitily.series.push(Math.ceil((value / this.stats.vulnerabilities.total) * 100))
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
