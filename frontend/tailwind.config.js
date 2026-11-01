/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "../backend/templates/**/*.html",
    "../backend/web/forms.py",
    "./src/**/*.{js,jsx}",
  ],
  theme: {
    extend: {
      fontFamily: {
        sans: ['"Vazirmatn Variable"', "Vazirmatn", "Tahoma", "system-ui", "sans-serif"],
      },
      colors: {
        cream: { 50: "#fffaf6", 100: "#fbf3ec", 200: "#f4e6da" },
        plum: { 700: "#4a2636", 800: "#3a1c2a", 900: "#2a1620" },
        gold: { 400: "#d4a373", 500: "#b8895a" },
      },
      keyframes: {
        fadeUp: { "0%": { opacity: 0, transform: "translateY(18px)" }, "100%": { opacity: 1, transform: "none" } },
        float: { "0%,100%": { transform: "translateY(0)" }, "50%": { transform: "translateY(-10px)" } },
      },
      animation: {
        "fade-up": "fadeUp .8s ease-out both",
        float: "float 6s ease-in-out infinite",
      },
    },
  },
  plugins: [],
};
