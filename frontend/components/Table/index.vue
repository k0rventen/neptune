<template>
  <table class="w-full">
    <thead>
    <tr class="border-b border-[#e9e6e6]">
      <th v-for="column in columns" :key="column.name" class="py-2 w-1/6">{{ column.label }}</th>
    </tr>
    </thead>
    <tbody>
    <tr v-for="(row,index) in data" :key="index" class="border-b border-[#e9e6e6]" :class="[index % 2 ? 'bg-[#e9e6e6]' : 'bg-white']">
      <td v-for="column in columns" :key="column.name" class="text-center py-2">
        <slot :name="column.name" :item="row">
          {{ row[column.name] }}
        </slot>
      </td>
    </tr>
    </tbody>
  </table>
</template>

<script>
export default {
  name: "TableIndex",
  props: {
    data: {
      type: Array,
      require: true,
      default: () => []
    },
    columns: {
      type: Array,
      require: true,
      default: () => []
    }
  }
}
</script>

<style scoped>

</style>
