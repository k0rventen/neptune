/** @type {import('tailwindcss').Config} */
module.exports = {
  darkMode: 'class',
  content: [],
  theme: {
    extend: {
      colors: {
        'primary': '#2093cd',
        'light-gray': '#f4f7f8',
      },
      gridTemplateRows: {
        'layout': 'auto 1fr 1fr auto'
      }
    },
    fontFamily: {
      sans: ['Montserrat', 'sans-serif']
    }
  },
  plugins: [],
}

