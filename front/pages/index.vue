<script setup>
import { useStatStore } from '@/store/statistic.store'
const store = useStatStore()
const router = useRouter()

const { t } = useI18n()


const setColor = (index) => {
    switch (index) {
        case 'most_active_vulnerabilities':
            return 'bg-black order-1'
        case 'most_vulnerabilities':
            return 'bg-red-500 order-2'
        case 'most_outdated_packages':
            return 'bg-yellow-400 order-3'
        case 'most_packages':
            return 'bg-green-500 order-4'
        case 'most_recent':
            return 'bg-primary order-5'
    }
}

const tags = ref({
    options: {
        title: {
            text: t('index.img_follow'),
            align: 'center',
            style: {
                fontSize: '14px',
                fontWeight: 'regular',
                fontFamily: undefined,
                color: '#263238',
            },
        },
        colors: ['#008FFB', '#FF4560', '#FEB019'],
        chart: {
            height: 350,
            type: 'line',
            zoom: {
                enabled: false,
            },
        },
        dataLabels: {
            enabled: false,
        },
        stroke: {
            curve: 'smooth',
        },
        grid: {
            row: {
                colors: ['#f3f3f3', 'transparent'], // takes an array which will be repeated on columns
                opacity: 0.5,
            },
        },
        xaxis: {
            labels: {
                show: false,
            },
            categories: [],
        },
    },
    series: [
        {
            name: t('index.img_total'),
            data: [],
        },
        {
            name: t('index.img_w_vuln'),
            data: [],
        },
        {
            name: t('index.img_w_outdated'),
            data: [],
        },
    ],
})

const vuln = ref({
    options: {
        title: {
            text: t('index.img_follow_vuln'),
            align: 'center',
            style: {
                fontSize: '14px',
                fontWeight: 'regular',
                fontFamily: undefined,
                color: '#263238',
            },
        },
        colors: [
            '#008FFB',
            '#FF4560',
            '#FEB019',
            '#546E7A',
            '#32c259',
            '#8d2aa1',
        ],
        chart: {
            height: 350,
            type: 'line',
            zoom: {
                enabled: false,
            },
        },
        dataLabels: {
            enabled: false,
        },
        stroke: {
            curve: 'smooth',
        },
        grid: {
            row: {
                colors: ['#f3f3f3', 'transparent'], // takes an array which will be repeated on columns
                opacity: 0.5,
            },
        },
        xaxis: {
            labels: {
                show: false,
            },
            categories: [],
        },
    },
    series: [
        {
            name: t('index.amount_of_vuln'),
            data: [],
        },
        {
            name: t('index.active_vuln'),
            data: [],
        },
        {
            name: t('index.low_vuln'),
            data: [],
        },
        {
            name: t('index.medium_vuln'),
            data: [],
        },
        {
            name: t('index.high_vuln'),
            data: [],
        },
        {
            name: t('index.critic_vuln'),
            data: [],
        },
    ],
})

const packages = ref({
    options: {
        title: {
            text: t('index.package_stat'),
            align: 'center',
            style: {
                fontSize: '14px',
                fontWeight: 'regular',
                fontFamily: undefined,
                color: '#263238',
            },
        },
        colors: ['#008FFB', '#FF4560', '#FEB019'],
        chart: {
            height: 350,
            type: 'line',
            zoom: {
                enabled: false,
            },
        },
        dataLabels: {
            enabled: false,
        },
        stroke: {
            curve: 'smooth',
        },
        grid: {
            row: {
                colors: ['#f3f3f3', 'transparent'], // takes an array which will be repeated on columns
                opacity: 0.5,
            },
        },
        xaxis: {
            labels: {
                show: false,
            },
            categories: [],
        },
    },
    series: [
        {
            name: t('index.total_img'),
            data: [],
        },
        {
            name: t('index.img_w_vuln'),
            data: [],
        },
        {
            name: t('index.img_w_outdated'),
            data: [],
        },
    ],
})

await store.getFiveImages()
await store.getStats()
await store.getHistoricalStat().then(() => {
    store.statsHisto.forEach(element => {
        // First chart
        tags.value.options.xaxis.categories.push(
            useDateConverter(element.timestamp)
        )

        tags.value.series[0].data.push(element.tags_total_count)
        tags.value.series[1].data.push(element.vulnerable_tags_count)
        tags.value.series[2].data.push(element.outdated_tags_count)

        // Second chart
        vuln.value.options.xaxis.categories.push(
            useDateConverter(element.timestamp)
        )
        vuln.value.series[0].data.push(element.vulnerabilities_total_count)
        vuln.value.series[1].data.push(element.active_vulnerabilities_count)
        vuln.value.series[2].data.push(element.low_vulnerabilities_count)
        vuln.value.series[3].data.push(element.medium_vulnerabilities_count)
        vuln.value.series[4].data.push(element.high_vulnerabilities_count)
        vuln.value.series[5].data.push(element.critical_vulnerabilities_count)

        // Last chart
        packages.value.options.xaxis.categories.push(
            useDateConverter(element.timestamp)
        )
        packages.value.series[0].data.push(element.packages_total_count)
        packages.value.series[1].data.push(element.outdated_packages_count)
        packages.value.series[2].data.push(element.vulnerable_packages_count)
    });
})
</script>

<template>
    <div class="w-full grid grid-cols-4 grid-row-layout gap-5 h-full">
        <div
            class="w-full p-5 bg-white dark:bg-[#303030] dark:text-white shadow-md flex justify-between items-center col-span-4 lg:col-span-1">
            <div>
                <p>{{ $t('index.card.amount_vuln') }}</p>
                <p>{{ store.stats.vulnerabilities_total_count }}</p>
            </div>
            <div class="bg-primary w-fit h-fit p-4 rounded-sm">
                <svg class="fill-white w-8 h-8" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24">
                    <path
                        d="M20.763 10.377c-.694.519-1.537.801-2.403.801-1.607 0-2.415-1.963-1.282-3.095.614-.615 1.406-1.009 2.266-1.133 1.621-.233 2.334-2.244 1.142-3.437s-3.203-.479-3.437 1.142c-.123.857-.52 1.653-1.132 2.266-1.138 1.138-3.095.329-3.095-1.282 0-.869.28-1.708.801-2.403.983-1.312.061-3.236-1.623-3.236-1.683 0-2.606 1.923-1.623 3.237.519.693.801 1.537.801 2.403 0 1.61-1.956 2.421-3.095 1.282-.614-.614-1.008-1.405-1.132-2.266-.233-1.621-2.243-2.334-3.436-1.141s-.48 3.203 1.141 3.436c.857.123 1.653.52 2.266 1.132 1.138 1.139.329 3.095-1.282 3.095-.869 0-1.707-.28-2.403-.801-1.313-.983-3.237-.061-3.237 1.623 0 1.683 1.923 2.606 3.237 1.623.693-.519 1.537-.801 2.403-.801 1.61 0 2.421 1.956 1.282 3.095-.614.615-1.406 1.009-2.266 1.133-1.621.233-2.334 2.244-1.142 3.437s3.203.479 3.437-1.142c.123-.857.52-1.653 1.132-2.266 1.139-1.138 3.095-.329 3.095 1.282 0 .869-.28 1.708-.801 2.404-.981 1.308-.064 3.235 1.623 3.235 1.677 0 2.611-1.919 1.621-3.24-.518-.689-.799-1.528-.799-2.39 0-1.615 1.957-2.432 3.095-1.293.615.615 1.009 1.406 1.133 2.267.233 1.621 2.244 2.334 3.437 1.142 1.19-1.19.483-3.206-1.146-3.437-.854-.121-1.646-.515-2.255-1.125-1.143-1.141-.337-3.102 1.274-3.102.87 0 1.708.28 2.404.801 1.309.981 3.236.064 3.236-1.623 0-1.686-1.926-2.605-3.237-1.623zm-10.728 4.296c-.547 0-.99-.443-.99-.99s.443-.99.99-.99.99.443.99.99-.443.99-.99.99zm1.262-3.143c-.858 0-1.553-.695-1.553-1.553s.695-1.553 1.553-1.553 1.553.695 1.553 1.553-.695 1.553-1.553 1.553zm2.928 2.969c-.727 0-1.315-.589-1.315-1.315s.589-1.315 1.315-1.315 1.315.589 1.315 1.315-.589 1.315-1.315 1.315z" />
                </svg>

            </div>
        </div>
        <div
            class="w-full h-full p-5 bg-white dark:bg-[#303030] dark:text-white shadow-md flex justify-between items-center col-span-4 lg:col-span-1">
            <div>
                <p>{{ $t('index.card.amount_img') }}</p>
                <p>{{ store.stats.tags_total_count }}</p>
            </div>
            <div class="bg-primary w-fit h-fit p-4 rounded-sm">
                <svg class="fill-white w-8 h-8" xmlns="http://www.w3.org/2000/svg" fill-rule="evenodd" clip-rule="evenodd"
                    viewBox="0 0 24 24">
                    <path
                        d="M11.5 23l-8.5-4.535v-3.953l5.4 3.122 3.1-3.406v8.772zm1-.001v-8.806l3.162 3.343 5.338-2.958v3.887l-8.5 4.534zm-10.339-10.125l-2.161-1.244 3-3.302-3-2.823 8.718-4.505 3.215 2.385 3.325-2.385 8.742 4.561-2.995 2.771 2.995 3.443-2.242 1.241v-.001l-5.903 3.27-3.348-3.541 7.416-3.962-7.922-4.372-7.923 4.372 7.422 3.937v.024l-3.297 3.622-5.203-3.008-.16-.092-.679-.393v.002z" />
                </svg>
            </div>
        </div>
        <div
            class="w-full h-full p-5 bg-white dark:bg-[#303030] dark:text-white shadow-md flex justify-between items-center col-span-4 lg:col-span-2">
            <div>
                <p>{{ $t('index.card.amount_pkg') }}</p>
                <p>{{ store.stats.packages_total_count }}</p>
            </div>
            <div class="bg-primary w-fit h-fit p-4 rounded-sm">
                <svg class="fill-white w-8 h-8" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24">
                    <path
                        d="M15.354 6h-3.554c-2.721-4.496-9.566-4.523-11.293-1.706-1.341 2.186.061 5.062 3.24 5.062 1.307 0 2.52-.593 4.253-.329v3.567l9.033 9.042 6.967-6.966-8.646-8.67zm-11.606 1.871c-1.996 0-2.738-1.6-1.956-2.835 1.076-1.701 5.756-1.94 8.19.964h-1.982v1.529c-1.922-.233-3.2.342-4.252.342zm9.207 2.645c-.817.817-2.206.394-2.446-.72 1.188.093 1.902-.723 1.795-1.708 1.071.285 1.445 1.634.651 2.428z" />
                </svg>
            </div>
        </div>
        <div
            class="w-full h-full max-h-fit p-5 bg-white dark:bg-[#303030] dark:text-white shadow-md flex justify-between items-center col-span-4 md:col-span-2">
            <apexchart class="w-full" height="100%" type="line" :options="tags.options" :series="tags.series" />
        </div>
        <div
            class="w-full h-full max-h-fit p-5 bg-white dark:bg-[#303030] dark:text-white shadow-md flex justify-between items-center col-span-4 md:col-span-2">

        </div>
        <div
            class="w-full h-full max-h-fit p-5 bg-white dark:bg-[#303030] dark:text-white shadow-md flex justify-between items-center col-span-4 md:col-span-2">
            <apexchart class="w-full" height="100%" type="line" :options="vuln.options" :series="vuln.series" />
        </div>
        <div
            class="w-full h-full max-h-fit p-5 bg-white dark:bg-[#303030] dark:text-white shadow-md flex justify-between items-center col-span-4 md:col-span-2">
            <apexchart class="w-full" height="100%" type="line" :options="packages.options" :series="packages.series" />
        </div>
        <div class="w-full h-full p-5 bg-white dark:bg-[#303030] dark:text-white shadow-md col-span-4 text-white">
            <div class="lg:flex items-center justify-between">
                <p class="text-black dark:text-white underline underline-offset-4">{{ $t('index.topfiveimg')}}</p>
                <div class="text-black dark:text-white flex flex-col lg:flex-row mt-3 lg:mt-0 gap-3">
                    <div class="flex items-center gap-1">
                        <div class="h-3 w-3 rounded-sm bg-black"></div>
                        <p class="text-xs">
                            {{ $t('index.the_most_vulnerable_active') }}
                        </p>
                    </div>
                    <div class="flex items-center gap-1">
                        <div class="h-3 w-3 rounded-sm bg-red-500"></div>
                        <p class="text-xs">{{ $t('index.the_most_vulnerable') }}</p>
                    </div>
                    <div class="flex items-center gap-1">
                        <div class="h-3 w-3 rounded-sm bg-yellow-400"></div>
                        <p class="text-xs">{{ $t('index.the_most_outdated') }}</p>
                    </div>
                    <div class="flex items-center gap-1">
                        <div class="h-3 w-3 rounded-sm bg-green-500"></div>
                        <p class="text-xs">{{ $t('index.the_most_package') }}</p>
                    </div>
                    <div class="flex items-center gap-1">
                        <div class="h-3 w-3 rounded-sm bg-primary"></div>
                        <p class="text-xs">{{ $t('index.the_most_recent') }}</p>
                    </div>
                </div>
            </div>
            <div class="grid grid-cols-1 lg:grid-cols-5 gap-5 mt-3 font-light">
                <div v-for="image, index in store.mostPopular" :class="setColor(index)" @click="
                    router.push({
                        path: '/images/' + image.sha,
                    })" class="w-full h-full p-3 rounded-sm cursor-pointer">
                    <p>{{ $t('index.card.img_name') }}: {{ image.image }}:{{ image.tag }}</p>
                    <p>{{ $t('index.card.img_size') }}: {{ useCalcConverter(image.size) }}</p>
                    <p>{{ $t('index.card.packages') }}: {{ image.packages }}</p>
                    <p>{{ $t('index.card.vulnerabilities') }}: {{ image.vulnerabilities }}</p>
                    <p>{{ $t('index.card.outdated_package') }}: {{ image.outdated_packages }}</p>
                </div>

            </div>
        </div>
    </div>
</template>