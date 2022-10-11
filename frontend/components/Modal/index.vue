<template>
  <div class="bg-black absolute top-0 flex items-center justify-center left-0 bg-opacity-25 w-full h-screen">
    <div ref="modals" class="w-[95vmin] h-2/3 bg-white rounded-md px-3 py-3">
      <div class="w-full flex items-center justify-between">
        <p>{{ title }}</p>
        <svg class="w-4 h-4" clip-rule="evenodd" fill-rule="evenodd" stroke-linejoin="round" stroke-miterlimit="2" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg" @click="$emit('close')"><path d="m12 10.93 5.719-5.72c.146-.146.339-.219.531-.219.404 0 .75.324.75.749 0 .193-.073.385-.219.532l-5.72 5.719 5.719 5.719c.147.147.22.339.22.531 0 .427-.349.75-.75.75-.192 0-.385-.073-.531-.219l-5.719-5.719-5.719 5.719c-.146.146-.339.219-.531.219-.401 0-.75-.323-.75-.75 0-.192.073-.384.22-.531l5.719-5.719-5.72-5.719c-.146-.147-.219-.339-.219-.532 0-.425.346-.749.75-.749.192 0 .385.073.531.219z"/></svg>
      </div>
      <hr class="mt-2">
      <div class="w-full h-[calc(100%-33px)] flex flex-col justify-between overflow-y-scroll">
        <slot></slot>
        <slot name="footer"></slot>
      </div>

    </div>
  </div>
</template>

<script>
export default {
  name: "ModalComponent",
  model: {
    prop: 'show',
    event: 'close'
  },
  props: {
    show: {
      type: Boolean,
      default: false
    },
    title: {
      type: String,
      default: 'Modal'
    }
  },
  mounted() {
    this.$el.addEventListener('click', (e) => {
      this.handleClick(e)
    })
  },
  methods: {
    handleClick(e) {
      if(!this.$refs.modals.contains(e.target)) {
        this.$emit('close', false)
      }
    }
  }
}
</script>

<style scoped>
::-webkit-scrollbar {
  display: none;
}
</style>
