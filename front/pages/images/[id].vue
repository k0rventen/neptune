<script setup lang="ts">
import { useQuery } from "@tanstack/vue-query";
import type { RouteLocationNormalizedLoaded } from "vue-router";

const route: RouteLocationNormalizedLoaded = useRoute();

const { data: image, isLoading } = useQuery({
  queryKey: ["images", { id: route.params.id }],
  queryFn: async () => {
    const res = await fetch(
      `http://localhost:5000/api/tags/${route.params.id}`
    );
    return res.json();
  },
});
</script>

<template>
  <div class="w-full p-5 gap-5 relative z-[5]">
    <card v-if="!isLoading" class="w-full h-fit grid grid-cols-3">
      <div>
        <p class="font-mattone">
          Name :
          <span class="font-sans">{{ image.image }}:{{ image.tag }}</span>
        </p>
        <p class="font-mattone">
          Size :
          <span class="font-sans">{{ useCalcConverter(image.size) }}</span>
        </p>
        <p class="font-mattone">
          System :
          <span class="font-sans">{{ image.distro }}</span>
        </p>
      </div>
      <div>
        <p class="font-mattone">
          Packages :
          <span class="font-sans">{{ image.packages.length }}</span>
        </p>
        <p class="font-mattone">
          Vulnerabilities :
          <span class="font-sans">{{ image.vulnerabilities.length }}</span>
        </p>
        <p class="font-mattone">
          Active vulnerabilities :
          <span class="font-sans">{{
            image.active_vulnerabilities.length
          }}</span>
        </p>
      </div>
      <div>
        <p class="font-mattone">
          Outdated packages :
          <span class="font-sans">{{ image.outdated_packages.length }}</span>
        </p>
        <p class="font-mattone">
          Added date :
          <span class="font-sans">{{ dateConverter(image.date_added) }}</span>
        </p>
      </div>
    </card>
  </div>
</template>
