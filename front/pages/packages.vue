<script setup lang="ts">
import type { TableColumns } from "~/type";

const columns: TableColumns[] = [
  {
    name: "Name",
    key: "name",
  },
  {
    name: "Dependencies type",
    key: "dependencies",
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

const searchValue = ref<string>();
const isTyping = ref();

const delaySearch = (value: string) => {
  clearTimeout(isTyping.value);
  isTyping.value = setTimeout(() => {
    searchValue.value = value;
  }, 500);
};
</script>

<template>
  <div
    class="w-full scrollbar scrollbar-thumb-[#1b1c1e] scrollbar-track-[1b1c1e] overflow-y-scroll p-5 gap-5 relative z-[5]"
  >
    <searchbar :value="searchValue" @input="delaySearch" />
    <div class="h-full mt-3 p-5 bg-[#1b1c1e] border-[1px] border-white/15">
      <ClientOnly>
        <Table :columns="columns" :data="data" />
      </ClientOnly>
    </div>
  </div>
</template>
