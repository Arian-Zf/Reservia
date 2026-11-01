import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";

// خروجی بیلد مستقیم به پوشه‌ی static جنگو می‌رود:
//   site/style.css  (Tailwind + فونت)   ← در همه‌ی صفحه‌ها
//   site/islands.js (React)             ← فقط صفحه‌ی رزرو
export default defineConfig({
  base: "/static/site/",
  plugins: [react()],
  build: {
    outDir: "../backend/static/site",
    emptyOutDir: true,
    cssCodeSplit: false,
    rollupOptions: {
      input: "src/islands.jsx",
      output: {
        entryFileNames: "islands.js",
        chunkFileNames: "[name].js",
        assetFileNames: "[name][extname]",
      },
    },
  },
});
