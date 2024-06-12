<script setup lang="ts">
import { useInfiniteQuery } from "@tanstack/vue-query";

const searchValue: Ref<string> = ref("");
const hasVuln: Ref<boolean> = ref(false);
const isTyping = ref();

const queryParams = computed(() => {
  return {
    name_filter: searchValue.value,
    has_vuln: hasVuln.value,
  };
});

const fetchProjects = async ({ pageParam = 0 }) => {
  let url = `http://localhost:5000/api/tags?page=${pageParam}&per_page=20`;

  console.log(queryParams.value);

  Object.entries(queryParams.value).forEach(([key, value]) => {
    if (value) {
      url += `&${key}=${value}`;
    }
  });

  const res = await fetch(url);

  return res.json();
};

const { data, fetchNextPage, hasNextPage } = useInfiniteQuery({
  queryKey: ["images", queryParams],
  queryFn: fetchProjects,
  getNextPageParam: (lastPage) => lastPage.nextPage,
  initialPageParam: 0,
});

const delaySearch = (value: string) => {
  clearTimeout(isTyping.value);
  isTyping.value = setTimeout(() => {
    searchValue.value = value;
  }, 500);
};
</script>

<template>
  <div class="w-full h-screen p-5 gap-5 relative z-[5]">
    <searchbar :value="searchValue" @input="delaySearch" />
    <label class="text-white flex gap-3 items-center mt-3">
      <input class="block" type="checkbox" @click="hasVuln = !hasVuln" />
      Has vulnerabilities
    </label>
    <div class="mt-5 grid grid-cols-3 gap-5">
      <template v-for="items in data?.pages">
        <NuxtLink v-for="image in items.items" :to="`/images/${image.sha}`">
          <card class="relative cursor-pointer">
            <div
              style="clip-path: polygon(10% 0%, 100% 0%, 90% 100%, 0% 100%)"
              class="bg-red-500 italic text-xs w-fit px-5 absolute -top-1 -right-0"
            >
              <p>NEW !</p>
            </div>
            <p class="font-mattone tracking-wide">
              {{ image.image }}:{{ image.tag }}
            </p>
            <div class="bg-white/15 h-[1px] w-full my-3" />
            <p class="text-md font-mattone">
              Image size:
              <span class="font-sans">{{ useCalcConverter(image.size) }}</span>
            </p>
            <p class="text-md font-mattone">
              Packages: <span class="font-sans">{{ image.packages }}</span>
            </p>
            <p class="text-md font-mattone">
              Vulnerabilities:
              <span class="font-sans">{{ image.vulnerabilities }}</span>
            </p>
            <p class="text-md font-mattone">
              Active vulnerabilities:
              <span class="font-sans">{{ image.active_vulnerabilities }}</span>
            </p>
            <p class="text-md font-mattone">
              Outdated Packages:
              <span class="font-sans">{{ image.outdated_packages }}</span>
            </p>
            <p class="text-md font-mattone">
              Date:
              <span class="font-sans">{{
                dateConverter(image.date_added)
              }}</span>
            </p>
          </card>
        </NuxtLink>
      </template>
    </div>
  </div>
</template>
