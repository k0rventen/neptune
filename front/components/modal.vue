<script setup lang="ts">
const props: { visible: boolean } = defineProps({
  visible: {
    type: Boolean,
    required: true,
  },
});

const emit = defineEmits(["close", "submit"]);
</script>

<template>
  <Teleport v-if="visible" to="body">
    <div
      class="w-full h-screen bg-black/50 fixed top-0 left-0 z-[99999] backdrop-blur-md flex justify-center items-center"
      @click="emit('close')"
    >
      <card @click.stop>
        <slot />
      </card>
    </div>
  </Teleport>
</template>
