<template>
    <div class="flex items-center">
        <svg @click="downgradeOffset()" width="25" clip-rule="evenodd" fill-rule="evenodd" stroke-linejoin="round" stroke-miterlimit="2" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><path d="m13.789 7.155c.141-.108.3-.157.456-.157.389 0 .755.306.755.749v8.501c0 .445-.367.75-.755.75-.157 0-.316-.05-.457-.159-1.554-1.203-4.199-3.252-5.498-4.258-.184-.142-.29-.36-.29-.592 0-.23.107-.449.291-.591 1.299-1.002 3.945-3.044 5.498-4.243z"/></svg>
        <button v-if="offset > 0" :key="index" class="px-3 py-1">
            ...
        </button>
        <button v-for="index in 5" :key="index" class="px-3 py-1" :class="{'bg-[#a6d1e6] rounded-md text-white' : index === currentPage - offset }" @click="setPage(index)">
            {{ index + offset }}
        </button>
        <button v-if="offset + 5 !== nbPages" :key="index" class="px-3 py-1">
            ...
        </button>
        <svg @click="upgradeOffset()" width="25" class="rotate-180" clip-rule="evenodd" fill-rule="evenodd" stroke-linejoin="round" stroke-miterlimit="2" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><path d="m13.789 7.155c.141-.108.3-.157.456-.157.389 0 .755.306.755.749v8.501c0 .445-.367.75-.755.75-.157 0-.316-.05-.457-.159-1.554-1.203-4.199-3.252-5.498-4.258-.184-.142-.29-.36-.29-.592 0-.23.107-.449.291-.591 1.299-1.002 3.945-3.044 5.498-4.243z"/></svg>
    </div>
</template>

<script>
export default {
    name: "PaginationComponent",
    model: {
        prop: 'currentPage',
        event: 'change',
    },
    props: {
        nbPages: {
            type: Number,
            required: true
        },
        currentPage: {
            type: Number,
            required: true
        }
    },
    data () {
        return {
            offset : 0
        }
    },
    methods: {
        downgradeOffset() {
            if(this.currentPage - 1 > 0) {
                if(this.offset - 1 >= 0) {
                    if(this.currentPage - 5 <= this.nbPages - 5) {
                        this.offset--
                    }
                }
                this.$emit('change', this.currentPage - 1)
            } 
        },
        upgradeOffset() {
            if(this.currentPage + 1 <= this.nbPages) {
                if(this.offset + 5 < this.nbPages) {
                    this.offset++
                }
                this.$emit('change', this.currentPage + 1)
            }
        },
        setPage(index) {
            this.$emit('change', index + this.offset)
            if(this.offset + index - 1 > this.nbPages - 5) {
                this.offset = this.nbPages - 5
            } else {
                this.offset = index + this.offset - 1
            }
        }
    }
}
</script>