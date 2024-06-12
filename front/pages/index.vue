<script setup lang="ts">
import type { StatType } from "~/type.d";

const {
  current,
  isLoadingData,
  recordStat,
  featured,
  brandTextFeatured,
  changeGraph,
  graphTitle,
  series,
} = useDashboard();

const options = computed(() => {
  const option = {
    theme: {
      mode: "dark",
    },
    dataLabels: {
      enabled: false,
    },
    stroke: {
      curve: "smooth",
    },
    fill: {
      type: "gradient",
      gradient: {
        gradientToColors: ["transparent"],
        shadeIntensity: 0.2,
        opacityFrom: 1,
        opacityTo: 0,
        stops: [50, 100],
      },
    },
    colors: ["#955ab8", "#1b9e72", "#1ac3ed", "#92b01a", "#b01a2c", "#000000"],
    chart: {
      id: "vuechart-example",
      background: "transparent",
    },
    xaxis: {
      categories: [1991, 1992, 1993, 1994, 1995, 1996, 1997, 1998],
    },
  };

  option.xaxis.categories = recordStat.value.map((stat: StatType): string => {
    return dateConverter(stat.timestamp);
  });

  return option;
});
</script>

<template>
  <div
    v-if="!isLoadingData"
    class="flex-1 h-screen overflow-y-auto p-5 grid grid-cols-6 lg:grid-rows-8 gap-5 relative z-[5]"
  >
    <card class="col-span-6 lg:col-span-2 flex items-center gap-5">
      <div
        class="bg-[#242424] rounded h-full aspect-square p-4 items-center justify-center"
      >
        <Icon
          name="iconoir:warning-circle-solid"
          color="white"
          class="opacity-75 h-full w-full"
        />
      </div>
      <div>
        <h1 class="text-xl font-bold font-mattone">
          Vulnerabilities : {{ current.active_vulnerabilities_count }}
        </h1>
        <p class="text-gray-400">You should fix it to avoid problem</p>
      </div>
    </card>
    <card class="col-span-6 lg:col-span-2 flex items-center gap-5">
      <div
        class="bg-[#242424] rounded h-full aspect-square p-4 flex items-center justify-center"
      >
        <Icon
          name="iconoir:box-3d-center"
          color="white"
          class="opacity-75 h-full w-full"
        />
      </div>
      <div>
        <h1 class="text-xl font-bold font-mattone">
          Images: {{ current.tags_total_count }}
        </h1>
        <p class="text-gray-400">Total scan image in your park</p>
      </div>
    </card>
    <card class="col-span-6 lg:col-span-2 flex items-center gap-5">
      <div
        class="bg-[#242424] rounded h-full aspect-square p-4 items-center justify-center"
      >
        <Icon
          name="iconoir:attachment"
          color="white"
          class="opacity-75 h-full w-full"
        />
      </div>
      <div>
        <h1 class="text-xl font-bold font-mattone">
          Packages : {{ current.packages_total_count }}
        </h1>
        <p class="text-gray-400">Amount of library available in your park</p>
      </div>
    </card>
    <card
      class="col-span-6 row-span-5 flex items-center gap-5 w-full min-h-96 lg:min-h-fit"
    >
      <div class="w-full h-full flex gap-5 flex-col">
        <div class="flex w-full justify-between">
          <Icon
            name="ic:sharp-play-arrow"
            color="white"
            class="opacity-75 rotate-180 cursor-pointer"
            @click="changeGraph('left')"
          />
          <p class="text-center">{{ graphTitle }}</p>
          <Icon
            @click="changeGraph('right')"
            name="ic:sharp-play-arrow"
            color="white"
            class="opacity-75 cursor-pointer"
          />
        </div>
        <div class="flex-1">
          <apexchart
            type="area"
            height="100%"
            :options="options"
            :series="series"
          />
        </div>
      </div>
    </card>
    <card class="col-span-6 row-span-2 flex items-center gap-5 w-full">
      <div class="w-full h-full grid grid-cols-5 gap-5">
        <NuxtLink
          v-for="(image, key, index) in featured"
          :to="`/images/${image.sha}`"
        >
          <card
            class="bg-[#242424] relative cursor-pointer p-6 col-span-6 lg:col-span-1 h-full"
          >
            <div
              style="clip-path: polygon(10% 0%, 100% 0%, 90% 100%, 0% 100%)"
              class="bg-red-500 italic text-xs w-fit px-5 absolute -top-1 -right-0"
            >
              <p>{{ brandTextFeatured(index) }}</p>
            </div>
            <p class="font-mattone tracking-wide text-sm">
              Name:
              <span class="font-sans">{{ image.image }}:{{ image.tag }}</span>
            </p>
            <p class="font-mattone tracking-wide text-sm">
              Size:
              <span class="font-sans">{{ useCalcConverter(image.size) }}</span>
            </p>
            <p class="font-mattone tracking-wide text-sm">
              Packages: <span class="font-sans">{{ image.packages }}</span>
            </p>
            <p class="font-mattone tracking-wide text-sm">
              Vulnerabilites:
              <span class="font-sans">{{ image.vulnerabilities }}</span>
            </p>
            <p class="font-mattone tracking-wide text-sm">
              Out. Packages:
              <span class="font-sans">{{ image.outdated_packages }}</span>
            </p>
          </card>
        </NuxtLink>
      </div>
    </card>
  </div>
</template>
