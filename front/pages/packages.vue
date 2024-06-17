<script setup lang="ts">
import { useInfiniteQuery } from "@tanstack/vue-query";

const { fetchProjects, delaySearch, columns, queryParams, searchValue } =
  usePackages();

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

const allPackages = computed(() => {
  return packages.value?.pages.map((page) => page.items).flat();
});
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
            <div class="flex gap-3">
              <template v-for="version in item.versions">
                <VDropdown :distance="6">
                  <button
                    :class="
                      version.vulnerabilities.length > 0
                        ? 'bg-[#cf463c] hover:bg-[#7e2e28]'
                        : 'bg-[#1b9e72] hover:bg-[#0f6b4a]'
                    "
                    class="text-white rounded border border-white/15 w-fit px-2 py-1 relative z-10 transition ease-in"
                  >
                    {{ version.version }}
                  </button>
                  <template #popper>
                    <div class="p-2 text-xs">
                      <template v-if="version.vulnerabilities.length > 0">
                        <p>Vulnerabilities :</p>
                        <ul>
                          <NuxtLink
                            v-for="vuln in version.vulnerabilities"
                            :key="vuln.id"
                            :to="`/vulnerabilities?name=${vuln.name}`"
                          >
                            <li class="ml-2">- {{ vuln.name }}</li>
                          </NuxtLink>
                        </ul>
                      </template>

                      <p>Related Images:</p>
                      <ul>
                        <li
                          v-for="tag in version.tags"
                          :key="tag.sha"
                          class="cursor-pointer ml-2"
                        >
                          - {{ tag.name }}
                        </li>
                      </ul>
                    </div>
                  </template>
                </VDropdown>
              </template>
            </div>
          </template>
        </Table>
      </ClientOnly>
      <button
        class="bg-[#242424] text-white rounded border border-white/15 w-fit px-4 py-2"
        v-if="hasNextPage"
        @click="() => fetchNextPage()"
      >
        Load More...
      </button>
    </div>
  </div>
</template>
