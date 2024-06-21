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

const isOpenModal = ref(false);
const imageName = ref();

const fetchProjects = async ({ pageParam = 0 }) => {
  let url = `http://localhost:5000/api/tags?page=${pageParam}&per_page=20`;

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
  getNextPageParam: (lastPage) => {
    if ((lastPage.current_page + 1) * 40 - lastPage.total < 40) {
      return lastPage.current_page + 1;
    }
    return undefined;
  },
  initialPageParam: 1,
});

const delaySearch = (value: string) => {
  clearTimeout(isTyping.value);
  isTyping.value = setTimeout(() => {
    searchValue.value = value;
  }, 500);
};

const sendNewImg = async () => {
  await fetch("http://localhost:5000/api/scan", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      name: imageName.value,
    }),
  });
};

// less than 1 week
const isNew = (date: string) => {
  const now = new Date();
  const dateAdded = new Date(date);
  const diff = now.getTime() - dateAdded.getTime();
  return diff < 604800000;
};
</script>

<template>
  <div class="w-full h-screen p-5 gap-5 relative z-[5]">
    <Modal :visible="isOpenModal" @close="isOpenModal = !isOpenModal">
      <div>
        <label>Image name : </label>
        <input
          v-model="imageName"
          class="bg-transparent outline-none border-b-[1px] border-white/15"
          type="text"
        />
      </div>
      <button
        class="bg-[#1b1c1e] text-white border-white/15 border rounded flex items-center justify-center py-1 pr-4 pl-2 gap-2 w-full mt-5 hover:bg-[#161618] transition ease-in"
        @click="sendNewImg"
      >
        <Icon name="iconoir:plus" class="w-6 h-6" />
        Add the image
      </button>
    </Modal>

    <searchbar :value="searchValue" @input="delaySearch" />
    <div class="flex items-center mt-3 gap-3">
      <button
        class="bg-[#1b1c1e] text-white border-white/15 border rounded flex items-center justify-center py-1 pr-4 pl-2 gap-2 hover:bg-[#161618] transition ease-in"
        @click="isOpenModal = true"
      >
        <Icon
          name="iconoir:plus"
          class="w-6 h-6 hover:bg-[#161618] transition ease-in"
        />
        Add new image
      </button>
      <label class="text-white flex gap-3 items-center">
        <input class="block" type="checkbox" @click="hasVuln = !hasVuln" />
        Has vulnerabilities
      </label>
    </div>
    <div class="mt-3 grid grid-cols-3 gap-5">
      <template v-for="items in data?.pages">
        <NuxtLink v-for="image in items.items" :to="`/images/${image.sha}`">
          <card class="relative cursor-pointer">
            <div
              v-if="isNew(image.date_added)"
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
