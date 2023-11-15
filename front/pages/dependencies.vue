<script setup>
import { useDepStore } from '@/store/dependencies.store'

const localPath = useLocalePath()

const depStore = useDepStore()

const { t } = useI18n()

const getVersionBg = (version) => {
    if (version.vulnerabilities.length > 0) {
        return 'bg-red-500'
    } if (version.outdated === true) {
        return 'bg-yellow-500'
    } else {
        return 'bg-green-500'
    }
}

const removeUseless = (version) => {
      let res = version
      if (res.includes('ubuntu')) {
        res = res.replace('ubuntu', '')
      }
      if (res.length > 13) {
        return res.slice(0, 13) + '...'
      }
    return res
}

const pagination = reactive({
    page: 1,
    perPage: 40,
})

const filter = reactive({
    name_filter: undefined,
    with_outdated_versions: undefined,
    with_vulnerable_versions: undefined,
    type_filter: undefined
})

const columns = [
    {
        name: t('dependencies.name'),
        key: 'name'
    },
    {
        name: t('dependencies.type'),
        key: 'type'
    },
    {
        name: t('dependencies.added_date'),
        key: 'date_added',
    },
    {
        name: t('dependencies.versions'),
        key: 'versions',
    }
]

const delay = ref(undefined)
const delayTypeTime = ref(undefined)
const openParam = ref(false)

const delaySearch = (input) => {
    clearTimeout(delay.value)
    delay.value = setTimeout(async () => {
        filter.name_filter = input.target.value
        await depStore.getPackages({ ...pagination, filter })
        pagination.page = 1
        refresh.value++
    }, 750)
}

const delayType = (input) => {
    clearTimeout(delay.value)
    delayTypeTime.value = setTimeout(async () => {
        filter.type_filter = input.target.value
        await depStore.getPackages({ ...pagination, filter })
        pagination.page = 1
        refresh.value++
    }, 750)
}

await depStore.getPackages({ ...pagination, filter })

watch(pagination, async () => {
    await depStore.getPackages({ ...pagination, filter })
})

watch(filter, async () => {
    await depStore.getPackages({ ...pagination, filter })
})

</script>

<template>
        <div class="relative bg-white rounded shadow  px-2">
        <div class="flex items-center">
            <input class="w-full py-2 outline-none" type="text" :placeholder="$t('dependencies.dependency_name')"
            @input="delaySearch">
            <svg @click="openParam = !openParam" class="w-8 h-8 fill-gray-500" version="1.0" xmlns="http://www.w3.org/2000/svg"
                viewBox="0 0 1280.000000 1278.000000" preserveAspectRatio="xMidYMid meet">
                <metadata>
                    Created by potrace 1.15, written by Peter Selinger 2001-2017
                </metadata>
                <g transform="translate(0.000000,1278.000000) scale(0.100000,-0.100000)" stroke="none">
                    <path d="M7235 12766 c-16 -8 -42 -26 -56 -42 -14 -16 -153 -267 -309 -559
    -156 -291 -298 -553 -316 -582 -53 -84 -49 -83 -328 -94 l-247 -11 -53 26
    c-53 26 -59 34 -416 549 -200 287 -373 536 -386 553 -29 39 -80 64 -132 64
    -43 0 -1174 -376 -1213 -403 -58 -41 -70 -89 -59 -235 24 -296 71 -892 81
    -1029 l12 -153 -29 -57 c-28 -55 -38 -64 -234 -200 -113 -78 -221 -147 -240
    -153 -82 -24 -92 -21 -736 246 -661 274 -642 267 -720 232 -38 -18 -781 -942
    -796 -990 -8 -29 -8 -48 0 -77 8 -25 152 -223 402 -552 338 -446 391 -521 401
    -564 14 -65 14 -65 -116 -375 -115 -277 -141 -316 -219 -344 -23 -8 -324 -66
    -671 -128 -660 -118 -663 -119 -707 -179 -52 -70 -181 -1268 -139 -1293 6 -4
    293 -110 637 -236 344 -126 640 -238 657 -248 66 -38 81 -81 141 -413 31 -169
    56 -328 56 -355 0 -31 -9 -65 -23 -91 -15 -29 -167 -177 -492 -479 -259 -240
    -479 -451 -490 -467 -13 -21 -19 -47 -18 -81 0 -46 25 -97 255 -544 141 -271
    268 -506 283 -522 14 -15 45 -33 68 -39 39 -11 87 -2 667 129 654 148 677 151
    750 117 39 -19 504 -499 532 -549 38 -70 36 -90 -66 -488 -235 -917 -230 -897
    -217 -940 6 -22 22 -51 34 -65 12 -14 242 -149 511 -300 443 -249 494 -275
    535 -275 27 0 59 8 76 18 17 11 230 222 475 471 245 249 461 461 482 471 73
    39 93 37 459 -45 189 -42 355 -83 368 -92 69 -45 73 -54 286 -694 201 -603
    207 -619 245 -653 22 -20 55 -38 77 -42 91 -17 658 19 1020 65 164 21 199 38
    227 113 9 24 75 322 146 662 86 406 137 630 149 650 39 62 68 77 373 193 329
    126 371 135 444 96 18 -10 248 -191 510 -403 263 -212 491 -393 508 -403 22
    -13 45 -17 83 -14 51 3 62 11 349 228 583 441 638 484 657 511 11 14 22 48 24
    75 5 44 -15 102 -227 658 -128 336 -235 626 -237 645 -10 69 13 112 173 332
    86 117 166 224 178 236 35 39 95 65 151 64 27 0 326 -30 663 -67 l612 -66 43
    19 c23 11 50 28 60 39 14 16 364 954 422 1131 22 65 8 120 -43 172 -20 21
    -268 208 -551 416 -508 373 -514 378 -539 433 l-25 55 12 215 c16 281 18 294
    55 348 30 43 53 56 613 337 321 161 590 299 599 306 22 19 54 85 54 112 0 42
    -259 1217 -275 1248 -9 17 -32 41 -53 55 -42 27 1 24 -1013 89 -389 25 -396
    27 -455 83 -43 41 -223 380 -230 434 -4 27 0 60 8 84 8 22 162 289 342 593
    314 528 328 554 328 602 -1 27 -7 60 -14 74 -13 25 -850 884 -898 921 -15 12
    -45 21 -80 23 l-57 4 -564 -313 c-310 -172 -582 -319 -604 -327 -69 -24 -114
    -9 -300 95 -188 105 -208 120 -237 177 -26 50 -25 37 -49 751 -20 590 -21 611
    -43 655 -37 75 36 53 -984 296 -172 40 -323 74 -335 74 -12 -1 -35 -7 -52 -14z
    m-385 -2650 c275 -36 503 -87 740 -166 1259 -416 2223 -1500 2484 -2792 57
    -283 70 -419 70 -748 1 -310 -4 -386 -45 -635 -192 -1169 -955 -2197 -2024
    -2725 -405 -200 -755 -305 -1245 -372 -153 -21 -711 -17 -880 5 -874 119
    -1636 499 -2230 1113 -849 878 -1212 2088 -990 3300 146 797 579 1558 1196
    2103 609 537 1352 856 2169 930 151 14 608 6 755 -13z" />
                </g>
            </svg>
        </div>

        <div v-if="openParam" class="py-2">
            <div class="flex gap-2">
                <label for="outdatedV">{{  $t('dependencies.dependency_w_outdated') }}</label>
                <input v-model="filter.with_outdated_versions" type="checkbox" id="outdatedV" name="outdatedV">
            </div>
            <div class="flex gap-2">
                <label for="vulnerableV">{{  $t('dependencies.dependency_w_vuln') }}</label>
                <input v-model="filter.with_vulnerable_versions" type="checkbox" id="vulnerableV" name="vulnerableV">
            </div>
            <div class="flex gap-2 items-center">
                <label for="vulnerableV">{{  $t('dependencies.type') }}</label>
                <input @input="delayType" class="ml-3 border border-2 border-[#8f8f9d] rounded outline-none" type="text" id="package" name="package">
            </div>
        </div>
        </div>
        <div class="bg-white p-5 mt-5 rounded shadow">
            <custom-table :columns="columns" :data="depStore.dependencies.items">
                <template #date_added="{ item }">
                    {{ useDateConverter(item.date_added) }} 
                </template>
                <template #versions="{ item }">
                    <VDropdown class="w-fit" v-for="version in item.versions" :key="version.id">
                        <button class="py-1 px-2 text-xs text-white rounded-md max-w-prose" :class="getVersionBg(version)">
                            {{ removeUseless(version.version) }}
                        </button>

                        <template #popper>
                            <div class="px-2 py-1 outline-none">
                            <p class="text-center">{{ version.version }}</p>
                            <hr v-if="version.vulnerabilities.length > 0" />
                            <NuxtLink
                                v-for="vuln in version.vulnerabilities"
                                :key="vuln.id"
                                :to="localPath(`/vulnerabilities?name=${vuln.name}`)"
                            >
                                <p>
                                {{ vuln.name }}
                                </p>
                            </NuxtLink>

                            <div class="mt-2">
                                <p>Image concernés:</p>
                                <hr />
                                <p
                                v-for="tag in version.tags"
                                :key="tag.sha"
                                class="cursor-pointer"
                                >
                                {{ tag.name }}
                                </p>
                            </div>
                            </div>
                        </template>
                    </VDropdown>
                </template>
        </custom-table>
        <div class="w-full flex justify-center">
            <paginate class="mt-3" v-model="pagination.page"
                :nbPages="Math.ceil(depStore.dependencies.total / depStore.dependencies.per_page)" :key="refresh">
            </paginate>
        </div>
    </div>
    
</template>