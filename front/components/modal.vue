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
        <div class="flex w-full gap-1 justify-center items-center mb-3">
          <Icon
            size="24"
            name="iconoir:planet"
            color="white"
            class="opacity-75"
          />
          <p>Neptune</p>
        </div>
        <div class="h-[1px] w-full bg-white opacity-75 mb-3" />
        <slot />
      </card>
    </div>
  </Teleport>
</template>
