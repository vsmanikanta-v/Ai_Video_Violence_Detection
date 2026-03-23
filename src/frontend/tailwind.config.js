/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        soft: {
          cream: "#FDF8F3",
          sand: "#F5EDE4",
          sage: "#B8C4B8",
          slate: "#6B7B6E",
          navy: "#3D4F4D",
          coral: "#D4A59A",
          mint: "#C5E0C8",
        },
      },
      fontFamily: {
        sans: ["Inter", "system-ui", "sans-serif"],
      },
    },
  },
  plugins: [],
}
