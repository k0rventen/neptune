<template>
  <table id="c-table" class="w-full">
    <thead>
    <tr v-if="data" class="border-b border-[#e9e6e6]">
      <th v-for="column in columns" :key="column.name" class="py-2 w-1/6">
        <div class="flex gap-3 justify-center items-center cursor-pointer" @click="column.sorter ? order(column.name) : () => {}">
          {{ column.label }}
          <svg v-if="activeFilter?.name === column.name" :class="activeFilter?.name === column.name && activeFilter.order === 'asc' ? 'rotate-180' : undefined" xmlns="http://www.w3.org/2000/svg" width="12" height="12" viewBox="0 0 24 24"><path d="M12 3l12 18h-24z"/></svg>
        </div>

      </th>
    </tr>
    </thead>
    <tbody>
    <tr v-for="(row,index) in dataCopy ? dataCopy : data" :key="index" class="border-b border-[#e9e6e6]" :class="[index % 2 ? 'bg-[#e9e6e6]' : undefined]">
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
  },
  data() {
    return {
      activeFilter: undefined,
      dataCopy: undefined
    }
  },
  mounted() {
    this.dataCopy = [...this.data]
  },
  methods: {
    order(value) {
      this.dataCopy = [...this.data]
      if(this.activeFilter?.name === value) {
        this.activeFilter.order = this.activeFilter.order === 'asc' ? 'desc' : this.activeFilter = undefined
      } else {
        this.activeFilter = {
          name: value,
          order: 'asc'
        }
      }


      if(this.activeFilter) {
        this.dataCopy = this.dataCopy.sort((a,b) => {
          return this.columns.find((column) => column.name === value).sorter(a,b)
        })
        if(this.activeFilter?.order === 'desc') {
          this.dataCopy = this.dataCopy.reverse()
        }
      }

    },
  }
}
</script>

<style scoped>

</style>
