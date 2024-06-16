<script setup lang="ts">
import type { TableColumns } from "~/type";

const props = defineProps<{
  columns: TableColumns[];
  data: any;
}>();

console.log(props.data);
</script>

<template>
  <table class="w-full text-white">
    <tr class="border-b-[1px] border-white/15">
      <th v-for="column in columns" class="text-left pb-2.5" :key="column.key">
        {{ column.name }}
      </th>
    </tr>
    <tr v-for="(row, index) in data" :key="index">
      <td v-for="column in columns" class="py-2.5" :key="column.key">
        <slot :name="column.key" :item="row">
          {{ row[column.key] }}
        </slot>
      </td>
    </tr>
  </table>
</template>
