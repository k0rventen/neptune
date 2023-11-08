// https://nuxt.com/docs/api/configuration/nuxt-config
export default defineNuxtConfig({
  ssr: false,

  runtimeConfig: {
    public: {
      apiBase: ''
    }
  },

  alias: {
    pinia: "/node_modules/@pinia/nuxt/node_modules/pinia/dist/pinia.mjs"
  },

  css: [
    '@/assets/css/main.css'
  ],

  modules: [
    '@nuxtjs/tailwindcss',
    '@pinia/nuxt',
    '@nuxtjs/i18n',
    'floating-vue/nuxt'
  ],

  i18n: {
    defaultLocale: 'en',
    locales : ['fr', 'en', 'it'],
    vueI18n: './i18n.config.ts'
  },

  plugins: [
    { src: '@/plugins/apexcharts.ts', mode: 'client' },
  ]
})
