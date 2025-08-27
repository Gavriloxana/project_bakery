<template>
  <div class="min-h-screen bg-bakery-gradient">
    <!-- Hero Section -->
    <div class="bg-hero-gradient py-16 px-4">
      <div class="max-w-6xl mx-auto text-center">
        <div class="mb-8">
          <h1 class="text-5xl md:text-6xl font-bold text-transparent bg-clip-text bg-gradient-to-r from-amber-600 to-orange-600 mb-4 animate-float font-edu">
            🍰 Sweet Treats perfect eats
          </h1>
          <p class="text-xl text-amber-800 max-w-2xl mx-auto">
            ขนมสดใหม่พร้อมทานทุกวัน
          </p>
        </div>
        
        <!-- Decorative elements -->
        <div class="flex justify-center gap-4 mb-8">
          <div class="w-3 h-3 bg-amber-400 rounded-full animate-bounce-soft"></div>
          <div class="w-3 h-3 bg-orange-400 rounded-full animate-bounce-soft" style="animation-delay: 0.2s"></div>
          <div class="w-3 h-3 bg-pink-300 rounded-full animate-bounce-soft" style="animation-delay: 0.4s"></div>
        </div>
      </div>
    </div>

    <!-- Wave Divider -->
    <div class="wave-divider"></div>

    <!-- Products Section -->
    <div class="py-16 px-4">
      <div class="max-w-7xl mx-auto">
        <div class="text-center mb-12">
          <h2 class="text-3xl font-bold text-amber-800 mb-4">รายการสินค้า</h2>
          <div class="w-24 h-1 bg-gradient-to-r from-amber-400 to-orange-400 mx-auto rounded-full"></div>
        </div>

        <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
          <div 
            v-for="p in products" 
            :key="p.id" 
            class="bg-white rounded-2xl shadow-lg border border-amber-200 transition-all duration-300 hover:shadow-xl hover:scale-105 group overflow-hidden"
          >
            <div class="relative overflow-hidden">
              <img 
                v-if="p.image_url" 
                :src="API + p.image_url" 
                class="w-full h-48 object-cover transition-transform duration-500 group-hover:scale-110" 
                :alt="p.name"
              />
              <div v-else class="w-full h-48 bg-gradient-to-br from-amber-100 to-orange-100 flex items-center justify-center">
                <span class="text-4xl">🍰</span>
              </div>
              
              <!-- Price badge -->
              <div class="absolute top-3 right-3 bg-gradient-to-r from-amber-500 to-orange-500 text-white px-3 py-1 rounded-full font-bold shadow-lg">
                ฿{{ p.price }}
              </div>
            </div>
            
            <div class="p-6">
              <h3 class="font-bold text-lg text-amber-800 mb-3 group-hover:text-amber-600 transition-colors duration-300">
                {{ p.name }}
              </h3>
              
              <div class="space-y-4">
                <!-- Quantity controls -->
                <div class="flex items-center justify-center gap-2">
                  <button 
                    @click="dec(p.id)" 
                    class="w-8 h-8 rounded-full bg-amber-100 hover:bg-amber-200 text-amber-700 font-bold transition-all duration-200 hover:scale-110 flex items-center justify-center"
                  >
                    -
                  </button>
                  <div class="w-12 text-center font-bold text-amber-800 bg-amber-50 rounded-lg py-1">
                    {{ qty[p.id] || 1 }}
                  </div>
                  <button 
                    @click="inc(p.id)" 
                    class="w-8 h-8 rounded-full bg-amber-100 hover:bg-amber-200 text-amber-700 font-bold transition-all duration-200 hover:scale-110 flex items-center justify-center"
                  >
                    +
                  </button>
                </div>
                
                <!-- Add to cart button -->
                <button 
                  @click="addToCart(p, qty[p.id]||1)" 
                  class="w-full inline-flex items-center gap-2 px-6 py-3 rounded-full font-medium transition-all duration-300 transform hover:scale-105 hover:shadow-lg bg-gradient-to-r from-amber-400 to-orange-400 text-white shadow-md hover:from-amber-500 hover:to-orange-500 group-hover:shadow-xl"
                >
                  <span>เพิ่มลงตะกร้า</span>
                  <svg xmlns="http://www.w3.org/2000/svg" class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6v6m0 0v6m0-6h6m-6 0H6" />
                  </svg>
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Floating Cart Button -->
    <NuxtLink 
      to="/cart" 
      class="fixed bottom-6 right-6 bg-gradient-to-r from-amber-500 to-orange-500 text-white rounded-full shadow-2xl px-6 py-4 flex items-center gap-3 hover:shadow-amber-200/50 transition-all duration-300 hover:scale-110 z-50 group"
      aria-label="cart"
    >
      <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor" class="w-6 h-6 group-hover:animate-bounce">
        <path d="M2.25 3h1.386c.51 0 .955.343 1.087.835l.383 1.437M7.5 14.25h9.75m-9.75 0L6.75 6.75m.75 7.5l-1.5-7.5m0 0h13.5m0 0l1.258 6.286a1.125 1.125 0 01-1.102 1.339H7.5" />
      </svg>
      <span class="hidden sm:inline font-medium">เปิดตะกร้า</span>
      
      <!-- Cart count badge -->
      <span 
        v-if="cartCount > 0" 
        class="absolute -top-2 -right-2 bg-gradient-to-r from-pink-400 to-rose-400 text-white text-sm rounded-full px-2 py-1 font-bold shadow-lg animate-bounce-soft"
      >
        {{ cartCount }}
      </span>
    </NuxtLink>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, computed } from 'vue'
import { useCart } from '~/composables/useCart'

const config = useRuntimeConfig()
const API = config.public.apiBase

type Product = { id: string; name: string; price: number; image_url?: string }
const products = ref<Product[]>([])
const qty = ref<Record<string, number>>({})
const { add, items } = useCart()

const cartCount = computed(() => items.value.reduce((n,i)=>n+i.quantity,0))

const fetchProducts = async () => {
  try {
    console.log('Fetching products from:', API + '/products')
    products.value = await $fetch('/products', { baseURL: API })
    console.log('Products fetched successfully:', products.value)
  } catch (error) {
    console.error('Error fetching products:', error)
    // Handle error gracefully;
    products.value = []
  }
}

const addToCart = (p: Product, amount = 1) => { 
  add(p, amount) 
}

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


