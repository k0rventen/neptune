<script setup lang="ts">
import {
  useInfiniteQuery,
  useMutation,
  useQueryClient,
} from "@tanstack/vue-query";

const queryClient = useQueryClient();

const { delaySearch, searchValue, columns, queryParams, fetchVulnerabilities } =
  useVulnerabilities();

const {
  data: vulnerabilites,
  fetchNextPage,
  hasNextPage,
} = useInfiniteQuery({
  queryKey: ["vulnerabilities", queryParams],
  queryFn: fetchVulnerabilities,
  getNextPageParam: (lastPage) => {
    if ((lastPage.current_page + 1) * 40 - lastPage.total < 40) {
      return lastPage.current_page + 1;
    }
    return undefined;
  },
  initialPageParam: 1,
  refetchOnWindowFocus: false,
});

const mutation = useMutation({
  mutationFn: async (data: any) => {
    await fetch(`http://localhost:5000/api/vulnerabilities/${data.id}`, {
      method: "PUT",
      body: JSON.stringify({
        active: !data.active,
        notes: data.notes,
      }),
      headers: {
        "Content-Type": "application/json",
      },
    });
  },
  onSuccess: () => {
    queryClient.invalidateQueries({
      queryKey: ["vulnerabilities", queryParams],
    });
  },
});

const allVulnerabilities = computed(() => {
  return vulnerabilites.value?.pages.map((page) => page.items).flat();
});

const changeStatus = (item: any) => {
  mutation.mutate(item);
};
</script>

<template>
  <div class="w-full h-full p-5 gap-5 relative z-[5]">
    <searchbar :value="searchValue" @input="delaySearch" />
    <card class="flex flex-col items-center mt-5">
      <ClientOnly>
        <Table :columns="columns" :data="allVulnerabilities">
          <template #active="{ item }">
            <button
              class="rounded px-2 w-fit"
              :class="[item.active ? 'bg-green-500' : 'bg-red-500']"
              @click="changeStatus(item)"
            >
              <p>{{ item.active ? "Active" : "Inactive" }}</p>
            </button>
          </template>
          <template #affected_images="{ item }">
            <div class="rounded">
              <p>{{ item.affected_images.length }}</p>
            </div>
          </template>
          <template #affected_package="{ item }">
            <div class="rounded">
              <p>{{ item.affected_package.name }}</p>
            </div>
          </template>
          <template #notes="{ item }">
            <input
              class="bg-transparent outline-none border-b-[1px] border-white/15 w-full"
              type="text"
            />
          </template>
        </Table>
      </ClientOnly>

      <button
        class="bg-[#242424] text-white rounded border border-white/15 w-fit px-4 py-2"
        v-if="hasNextPage"
        @click="() => fetchNextPage()"
      >
        Load More...
      </button></card
    >
  </div>
</template>
