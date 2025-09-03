import tailwindcss from "@tailwindcss/vite";

export default defineNuxtConfig({
  compatibilityDate: "2024-11-01",
  devtools: { enabled: true },
  css: ["~/assets/css/main.css"],
  runtimeConfig: {
    public: {
      // ลำดับการอ่านค่า: NUXT_PUBLIC_API_BASE > VITE_API_URL > localhost
      apiBase:
        process.env.NUXT_PUBLIC_API_BASE ||
        process.env.VITE_API_URL ||
        "http://localhost:8000",
    },
  },
  vite: {
    plugins: [tailwindcss()],
  },
});
