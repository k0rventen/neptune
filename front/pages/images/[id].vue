<script setup lang="ts">
import { useMutation, useQuery, useQueryClient } from "@tanstack/vue-query";
import type { RouteLocationNormalizedLoaded } from "vue-router";

const route: RouteLocationNormalizedLoaded = useRoute();
const { columns, activeVulnColumn } = useImage();
const queryClient = useQueryClient();

const { data: image, isLoading } = useQuery({
  queryKey: ["images", { id: route.params.id }],
  queryFn: async () => {
    const res = await fetch(
      `http://localhost:5000/api/tags/${route.params.id}`
    );
    return res.json();
  },
  refetchOnWindowFocus: false,
});

const mutation = useMutation({
  mutationFn: async (data: any) => {
    await fetch(`http://localhost:5000/api/vulnerabilities/${data.id}`, {
      method: "PUT",
      body: JSON.stringify({
        active: !data.active,
      }),
      headers: {
        "Content-Type": "application/json",
      },
    });
  },
  onSuccess: () => {
    queryClient.invalidateQueries({
      queryKey: ["images", { id: route.params.id }],
    });
  },
});

const vulnerabiltiesTable = computed(() => {
  return [
    ...image.value.vulnerabilities,
    ...image.value.active_vulnerabilities,
  ];
});
</script>

<template>
  <div v-if="!isLoading" class="w-full p-5 gap-5 relative z-[5]">
    <card class="w-full h-fit grid grid-cols-3">
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
    <div class="grid grid-cols-2 w-full mt-5 gap-5">
      <card>
        <Table :columns="columns" :data="image.packages">
          <template #outdated="{ item }">
            <button
              class="rounded px-2 w-fit"
              :class="[item.outdated ? 'bg-red-500' : 'bg-green-500']"
            >
              <p>{{ item.outdated ? "Outdated" : "Up to date" }}</p>
            </button>
          </template>
        </Table>
      </card>
      <card>
        <Table :columns="activeVulnColumn" :data="vulnerabiltiesTable">
          <template #active="{ item }">
            <button
              class="rounded px-2 w-fit"
              :class="[item.active ? 'bg-green-500' : 'bg-red-500']"
              @click="mutation.mutate(item)"
            >
              <p>{{ item.active ? "Active" : "Inactive" }}</p>
            </button>
          </template>
        </Table>
      </card>
    </div>
  </div>
</template>
