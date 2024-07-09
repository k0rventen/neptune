<script setup lang="ts">
import { useInfiniteQuery } from "@tanstack/vue-query";

const {
  fetchProjects,
  delaySearch,
  columns,
  queryParams,
  searchValue,
  withOutdated,
  withVulnerabilities,
  delaySearchPackage,
  typePackages,
} = usePackages();

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
    <div class="my-3 flex gap-5 text-white">
      <label class="flex gap-2">
        <input type="checkbox" v-model="withOutdated" />
        With outdated packages
      </label>
      <label class="flex gap-2">
        <input type="checkbox" v-model="withVulnerabilities" />
        With vulnerabilities
      </label>
      <div class="gap-2 flex">
        <label>Dependency type : </label>
        <input
          @input="(event: Event) => delaySearchPackage((event?.target as HTMLInputElement)?.value)"
          class="bg-transparent outline-none border-b-[1px] border-white/15"
          type="text"
        />
      </div>
    </div>

    <card class="flex flex-col items-center">
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
                        <NuxtLink
                          v-for="tag in version.tags"
                          :key="tag.sha"
                          :to="`/images/${tag.sha}`"
                        >
                          <li class="cursor-pointer ml-2">- {{ tag.name }}</li>
                        </NuxtLink>
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
    </card>
  </div>
</template>
