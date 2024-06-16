<script setup lang="ts">
import { useInfiniteQuery } from "@tanstack/vue-query";
import type { TableColumns } from "~/type";

const searchValue = ref<string>();

const columns: TableColumns[] = [
  {
    name: "Name",
    key: "name",
  },
  {
    name: "Dependencies type",
    key: "type",
  },
  {
    name: "Date added",
    key: "date_added",
  },
  {
    name: "Versions",
    key: "versions",
  },
];

const data = [
  {
    name: "test",
    dependencies: "test",
    date_added: "test",
    versions: "test",
  },
];

const queryParams = computed(() => {
  return {
    name_filter: searchValue.value,
    with_outdated_versions: "",
    with_vulnerable_versions: "",
    type_filter: "",
  };
});

const fetchProjects = async ({ pageParam = 0 }) => {
  let url = `http://localhost:5000/api/packages?page=${pageParam}&per_page=40`;

  Object.entries(queryParams.value).forEach(([key, value]) => {
    if (value) {
      url += `&${key}=${value}`;
    }
  });

  const res = await fetch(url);

  return res.json();
};

const {
  data: packages,
  fetchNextPage,
  hasNextPage,
} = useInfiniteQuery({
  queryKey: ["packages", queryParams],
  queryFn: fetchProjects,
  getNextPageParam: (lastPage) => {
    if ((lastPage.current_page + 1) * 40 - lastPage.total < 40) {
      return lastPage.current_page + 1;
    }
    return undefined;
  },
  initialPageParam: 1,
});

const isTyping = ref();

const loadMore = () => {
  fetchNextPage();
};

const allPackages = computed(() => {
  return packages.value?.pages.map((page) => page.items).flat();
});

const delaySearch = (value: string) => {
  clearTimeout(isTyping.value);
  isTyping.value = setTimeout(() => {
    searchValue.value = value;
  }, 500);
};
</script>

<template>
  <div class="w-full h-full p-5 gap-5 relative z-[5]">
    <searchbar :value="searchValue" @input="delaySearch" />
    <div
      class="h-full mt-3 p-5 bg-[#1b1c1e] border-[1px] border-white/15 flex flex-col items-center gap-5"
    >
      <ClientOnly>
        <Table :columns="columns" :data="allPackages">
          <template #date_added="{ item }">
            {{ new Date(item.date_added).toLocaleDateString() }}
          </template>
          <template #versions="{ item }">
            {{ item.versions.join(", ") }}
          </template>
        </Table>
      </ClientOnly>
      <button
        class="bg-[#242424] text-white rounded border border-white/15 w-fit px-4 py-2"
        v-if="hasNextPage"
        @click="loadMore"
      >
        Load More...
      </button>
    </div>
  </div>
</template>
