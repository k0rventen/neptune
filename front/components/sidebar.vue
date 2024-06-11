<script setup></script>

<template>
  <div
    class="bg-[#1b1c1e] min-h-screen border-r-[1px] border-white/15 min-w-16 flex flex-col align-center py-5 px-3 relative z-10"
  >
    <div class="relative">
      <div class="bg-[#242424] h-fit w-fit p-2 rounded-md">
        <Icon
          size="24"
          name="iconoir:planet"
          color="white"
          class="opacity-75"
        />
      </div>
    </div>
    <div class="bg-white/15 h-[1px] w-full my-3" />
    <div class="flex flex-col gap-3">
      <NuxtLink
        to="/"
        class="bg-[#242424] group ease-in transition hover:bg-[#955ab8] h-fit w-fit p-2 rounded-md relative"
      >
        <Icon
          size="24"
          name="iconoir:graph-up"
          color="white"
          class="opacity-75"
        />
        <div
          class="hidden group-hover:block absolute translate-x-full -right-5 top-1/2 -translate-y-1/2 origin-top-left bg-[#1b1c1e] border-white/15 border px-4 py-1 rounded text-white"
        >
          <p>Dashboard</p>
        </div>
      </NuxtLink>
      <NuxtLink
        to="/images"
        class="bg-[#242424] group ease-in transition hover:bg-[#955ab8] h-fit w-fit p-2 rounded-md relative"
      >
        <Icon
          size="24"
          name="iconoir:box-3d-center"
          color="white"
          class="opacity-75"
        />
        <div
          class="hidden group-hover:block absolute translate-x-full -right-5 top-1/2 -translate-y-1/2 origin-top-left bg-[#1b1c1e] border-white/15 border px-4 py-1 rounded text-white"
        >
          <p>Images</p>
        </div>
      </NuxtLink>
      <NuxtLink
        to="/vulnerabilities"
        class="bg-[#242424] group ease-in transition hover:bg-[#955ab8] h-fit w-fit p-2 rounded-md relative"
      >
        <Icon
          size="24"
          name="iconoir:wrench"
          color="white"
          class="opacity-75"
        />
        <div
          class="hidden group-hover:block absolute translate-x-full -right-5 top-1/2 -translate-y-1/2 origin-top-left bg-[#1b1c1e] border-white/15 border px-4 py-1 rounded text-white"
        >
          <p>Vulnerabilities</p>
        </div>
      </NuxtLink>
      <NuxtLink
        to="/packages"
        class="bg-[#242424] group ease-in transition hover:bg-[#955ab8] h-fit w-fit p-2 rounded-md relative"
      >
        <Icon
          size="24"
          name="iconoir:attachment"
          color="white"
          class="opacity-75"
        />
        <div
          class="hidden group-hover:block absolute translate-x-full -right-5 top-1/2 -translate-y-1/2 origin-top-left bg-[#1b1c1e] border-white/15 border px-4 py-1 rounded text-white"
        >
          <p>Packages</p>
        </div>
      </NuxtLink>
      <NuxtLink
        to="/registry"
        class="bg-[#242424] group ease-in transition hover:bg-[#955ab8] h-fit w-fit p-2 rounded-md relative"
      >
        <Icon
          size="24"
          name="iconoir:puzzle"
          color="white"
          class="opacity-75"
        />
        <div
          class="hidden group-hover:block absolute translate-x-full -right-5 top-1/2 -translate-y-1/2 origin-top-left bg-[#1b1c1e] border-white/15 border px-4 py-1 rounded text-white"
        >
          <p>Registry</p>
        </div>
      </NuxtLink>
    </div>
  </div>
</template>
