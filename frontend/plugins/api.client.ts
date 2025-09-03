// frontend/plugins/api.client.ts
export default defineNuxtPlugin(() => {
  const { public: pub } = useRuntimeConfig();
  const api = $fetch.create({
    baseURL: pub.apiBase,
    credentials: "include",
  });
  return {
    provide: { api },
  };
});

// วิธีใช้ในหน้า/คอมโพเนนต์:
// const { $api } = useNuxtApp();
// const products = await $api('/products'); // จะอิง baseURL จาก env อัตโนมัติ
