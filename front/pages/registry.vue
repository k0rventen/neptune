<script setup>
const formValues = ref({
  url: "",
  username: "",
});
</script>

<template>
  <div class="flex-1 p-5 grid grid-cols-1 lg:grid-rows-8 gap-2 relative z-[5]">
    <card class="row-span-5"> </card>

    <div class="row-span-3">
      <div class="flex gap-2">
        <Icon
          size="24"
          name="iconoir:puzzle"
          color="white"
          class="opacity-75"
        />
        <p class="font-mattone mb-2 text-white opacity-75">Add registry</p>
      </div>

      <card class="h-[calc(100%-32px)]">
        <form class="flex flex-col gap-3 h-full justify-between">
          <div class="gap-3 flex flex-col">
            <div class="flex gap-3">
              <label>Repository URL: </label>
              <input
                v-model="formValues.url"
                class="bg-transparent outline-none border-b-[1px] border-white/15"
                type="text"
              />
            </div>
            <div class="flex gap-3">
              <label>Username: </label>
              <input
                v-model="formValues.username"
                class="bg-transparent outline-none border-b-[1px] border-white/15"
                type="text"
              />
            </div>
            <div class="flex gap-3">
              <label>Password: </label>
              <input
                v-model="formValues.password"
                class="bg-transparent outline-none border-b-[1px] border-white/15"
                type="password"
              />
            </div>
          </div>

          <button
            class="bg-[#1b1c1e] text-white border-white/15 border rounded flex items-center justify-center py-1 pr-4 pl-2 gap-2 w-full mt-5 hover:bg-[#161618] transition ease-in"
            type="submit"
          >
            Validate
          </button>
        </form>
      </card>
    </div>
  </div>
</template>
