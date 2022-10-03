<template>
  <div class="flex flex-col gap-3 w-full h-[calc(100vh-72px)] px-3 py-3">
    <div class="w-full h-1/2 lg:flex gap-3">
      <!-- Image vulnerability -->
      <div class="w-full lg:w-1/2 h-1/2 lg:h-auto">
        <card class="h-full" :header="$tc('card.image_vulnerability')">
          <div class="w-full h-full flex justify-center items-center">
            <apexchart height="90%" type="donut" :options="imageVuln.chartOptions" :series="imageVuln.series"/>
          </div>
        </card>
      </div>

      <!-- Number of vulnerability with severity -->
      <div class="mt-3 lg:mt-0 w-full lg:w-1/2 h-1/2 lg:h-auto">
        <card class="h-full" :header="$t('card.vulnerability')">
          <div class="w-full h-full flex justify-center items-center">
            <apexchart height="90%" type="donut" :options="vulnerabitily.chartOptions" :series="vulnerabitily.series"/>
          </div>
        </card>
      </div>

    </div>

    <!-- Evolution of the number of vulnerability -->
    <div class="mt-3 lg:mt-0 w-full h-1/2">
      <card class="h-full" :header="$t('card.follow_up_vulnerability')">
        <div class="w-full h-full flex justify-center items-center">
          <apexchart height="90%" type="line" :options="followVuln.chartOptions" :series="followVuln.series"/>
        </div>
      </card>
    </div>
  </div>
</template>

<script>
export default {
  name: 'IndexPage',
  data() {
    return {
      imageVuln: {
        chartOptions: {
          maintainAspectRatio: false,
          labels: ['Vulnerable', 'Safe'],
          chart: {
            type: 'donut',
          },
        },
        series: [45, 55],
      },
      vulnerabitily: {
        chartOptions: {
          labels: ['Critical', 'High', 'Medium', 'Low'],
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
        series: [33, 25, 12, 17],
      },
      followVuln: {
        chartOptions: {
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
          title: {
            text: 'Product Trends by Month',
            align: 'left'
          },
          grid: {
            row: {
              colors: ['#f3f3f3', 'transparent'], // takes an array which will be repeated on columns
              opacity: 0.5
            },
          },
          xaxis: {
            categories: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep'],
          }
        },
        series: [{
          name: "Desktops",
          data: [10, 41, 35, 51, 49, 62, 69, 91, 148]
        }],
      }

    }
  }
}
</script>
