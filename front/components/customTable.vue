<script setup>
const props = defineProps({
    columns: {
        type: Array,
        required: true
    },
    data: {
        type: Array,
        required: true
    }
})

</script>

<template>
    <table class="w-full bg-white">
        <thead class="border-b-[1px] border-gray-500">
            <tr class="">
                <th v-for="item in props.columns" :key="item.key" class="font-bold text-gray-500 py-2 px-1" :class="{ 'text-left' : item.position !== 'center'}">{{ item.name
                }}</th>
            </tr>
        </thead>
        <tbody class="h-fit">
            <tr class="h-fit" v-for="(row, index) in props.data" :key="index" :class="[index % 2 ? 'bg-[#e9eff2]' : undefined]">
                <td v-for="column in props.columns" :key="column.key" class="py-2 px-1 h-fit">
                    <slot :name="column.key" :item="row">
                        {{ row[column.key] }}
                    </slot>
                </td>
            </tr>
        </tbody>
    </table>
</template>