// https://nuxt.com/docs/api/configuration/nuxt-config
export default defineNuxtConfig({
  ssr: false,

  runtimeConfig: {
    public: {
      apiBase: ''
    }
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
    strategy: 'prefix_except_default',
    defaultLocale: 'en',
    locales : ['fr', 'en', 'it'],
    vueI18n: './i18n.config.ts'
  },

  plugins: [
    { src: '@/plugins/apexcharts.ts', mode: 'client' },
  ]
})