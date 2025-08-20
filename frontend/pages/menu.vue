<template>
  <div class="p-4 max-w-6xl mx-auto">
    <h1 class="text-2xl font-bold mb-4">เมนูสินค้า</h1>
    <div class="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-4">
      <div v-for="p in products" :key="p.id" class="bg-white rounded shadow overflow-hidden">
        <img v-if="p.image_url" :src="API + p.image_url" class="w-full h-36 object-cover" />
        <div class="p-3">
          <div class="font-semibold">{{ p.name }}</div>
          <div class="text-sm text-gray-600">฿{{ p.price }}</div>
          <div class="mt-2 flex items-center gap-2">
            <div class="inline-flex items-center border rounded">
              <button class="px-2" @click="dec(p.id)">-</button>
              <div class="w-10 text-center">{{ qty[p.id] || 1 }}</div>
              <button class="px-2" @click="inc(p.id)">+</button>
            </div>
            <button @click="addToCart(p, qty[p.id]||1)" class="bg-indigo-600 text-white text-sm px-3 py-1 rounded">เพิ่มลงตะกร้า</button>
          </div>
        </div>
      </div>
    </div>

    <NuxtLink to="/cart" class="fixed bottom-6 right-6 bg-indigo-600 text-white rounded-full shadow-lg px-4 py-3 flex items-center gap-2" aria-label="cart">
      <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor" class="w-6 h-6">
        <path d="M2.25 3h1.386c.51 0 .955.343 1.087.835l.383 1.437M7.5 14.25h9.75m-9.75 0L6.75 6.75m.75 7.5l-1.5-7.5m0 0h13.5m0 0l1.258 6.286a1.125 1.125 0 01-1.102 1.339H7.5" />
      </svg>
      <span class="hidden sm:inline">เปิดตะกร้า</span>
    </NuxtLink>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useCart } from '~/composables/useCart'

const config = useRuntimeConfig()
const API = config.public.apiBase

type Product = { id: string; name: string; price: number; image_url?: string }
const products = ref<Product[]>([])
const qty = ref<Record<string, number>>({})
const { add } = useCart()

const fetchProducts = async () => {
  products.value = await $fetch('/products', { baseURL: API })
}

const addToCart = (p: Product, amount = 1) => { add(p, amount) }

const inc = (id: string) => {
  qty.value[id] = (qty.value[id] || 1) + 1
}
const dec = (id: string) => {
  const next = (qty.value[id] || 1) - 1
  qty.value[id] = next < 1 ? 1 : next
}

onMounted(fetchProducts)
</script>

<style scoped>
body { background: #f8fafc; }
</style>


