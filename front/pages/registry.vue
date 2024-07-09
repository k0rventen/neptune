<script setup>
import { useMutation, useQuery, useQueryClient } from "@tanstack/vue-query";

const queryClient = new useQueryClient();

const formValues = ref({
  registry: "",
  user: "",
  password: "",
});

const { data: registries } = useQuery({
  queryKey: ["registries"],
  queryFn: async () => {
    const res = await fetch("http://localhost:5000/api/registries");
    return res.json();
  },
  refetchOnWindowFocus: false,
});

const mutation = useMutation({
  mutationFn: async (variables) => {
    await fetch("http://localhost:5000/api/registries", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(variables),
    });
  },
  onError: (error, variables, context) => {
    console.log(error);
  },
  onSuccess: (data, variables, context) => {
    queryClient.setQueriesData(["registries"], (oldData) => [
      ...oldData,
      variables,
    ]);
  },
});

const remove = useMutation({
  mutationFn: async (variables) => {
    await fetch("http://localhost:5000/api/registries", {
      method: "DELETE",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(variables),
    });
  },
  onSuccess: (data, variables, context) => {
    queryClient.setQueriesData(["registries"], (oldData) =>
      oldData.filter((registry) => registry.registry !== variables.registry)
    );
  },
});

const sendRegistry = () => {
  mutation.mutate(formValues.value);
};

const deleteRegistry = async (registry) => {
  remove.mutate({ registry });

  await queryClient.invalidateQueries({
    queryKey: ["registries"],
  });
};
</script>

<template>
  <div class="flex-1 p-5 grid grid-cols-1 lg:grid-rows-8 gap-2 relative z-[5]">
    <card class="row-span-5 grid grid-cols-4 grid-rows-3 gap-3">
      <div
        class="bg-[#242424] px-3 py-2 col-span-1 relative overflow-hidden rounded"
        v-for="registry in registries"
      >
        <Icon
          size="12"
          name="akar-icons:cross"
          color="white"
          class="opacity-50 absolute top-3 right-2 cursor-pointer"
          @click="deleteRegistry(registry.registry)"
        />
        <Icon
          size="150"
          name="iconoir:box-iso"
          color="white"
          class="opacity-50 absolute -right-8 -bottom-8"
        />
        <p>Registry: {{ registry.registry }}</p>
        <p>Username: {{ registry.user }}</p>
        <p>Password: {{ registry.password }}</p>
      </div>
    </card>

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
        <form
          class="flex flex-col gap-3 h-full justify-between"
          @submit.prevent="sendRegistry"
        >
          <div class="gap-3 flex flex-col">
            <div class="flex gap-3">
              <label>Repository URL: </label>
              <input
                v-model="formValues.registry"
                class="bg-transparent outline-none border-b-[1px] border-white/15"
                type="text"
              />
            </div>
            <div class="flex gap-3">
              <label>Username: </label>
              <input
                v-model="formValues.user"
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
