module.exports = {
  mode: 'jit',
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
    extend: {},
  },
  plugins: [
    require('tailwind-scrollbar'),
  ],
}
