<template>
  <table class="w-full">
    <thead>
    <tr class="border-b border-[#e9e6e6]">
      <th v-for="column in columns" :key="column.name" class="py-2 w-1/6">
        <div class="flex gap-3 justify-center items-center">
          {{ column.label }}
          <svg v-if="column.order" xmlns="http://www.w3.org/2000/svg" width="12" height="12" viewBox="0 0 24 24"><path d="M12 3l12 18h-24z" @click="$emit('filter', column.name)"/></svg>
        </div>

      </th>
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
