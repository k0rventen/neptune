module.exports = {
  mode: 'jit',
  content: [
    "./components/**/*.{js,vue,ts}",
    "./layouts/**/*.vue",
    "./pages/**/*.vue",
    "./plugins/**/*.{js,ts}",
    "./nuxt.config.{js,ts}",
  ],
  purge: [],
  darkMode: false, // or 'media' or 'class'
  theme: {
    fontFamily: {
      'sans': ['Satoshi'],
    },
    extend: {
      fontFamily: {
        'clash': ['Clash'],
      },
      colors: {
        'primary': '#f8f9fb',
        'secondary': '#919191',
        'neptune-blue': '#559cc4'
      }
    },
  },
  variants: {
    extend: {
      screens: {
        '3xl': '1900px',
      }
    },
  },
  plugins: [
    require('tailwind-scrollbar'),
  ],
}
