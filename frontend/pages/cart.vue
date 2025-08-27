<template>
  <div class="min-h-screen bg-bakery-gradient py-8">
    <div class="max-w-4xl mx-auto px-4">
      <!-- Header Section -->
      <div class="text-center mb-12">
        <h1 class="text-4xl md:text-5xl font-bold text-transparent bg-clip-text bg-gradient-to-r from-amber-600 to-orange-600 mb-4">
          🛒 ตะกร้าสินค้า
        </h1>
        <div class="w-24 h-1 bg-gradient-to-r from-amber-400 to-orange-400 mx-auto rounded-full"></div>
      </div>

      <!-- Empty Cart State -->
      <div 
        v-if="items.length === 0" 
        class="bg-white rounded-2xl shadow-lg border border-amber-200 transition-all duration-300 hover:shadow-xl hover:scale-105 p-12 text-center"
      >
        <div class="text-6xl mb-4">🍰</div>
        <h3 class="text-2xl font-bold text-amber-800 mb-4">ยังไม่มีสินค้าในตะกร้า</h3>
        <p class="text-amber-700 mb-8">มาเลือกขนมแสนอร่อยกันเถอะ!</p>
        <NuxtLink 
          to="/menu" 
          class="inline-flex items-center gap-2 px-6 py-3 rounded-full font-medium transition-all duration-300 transform hover:scale-105 hover:shadow-lg bg-gradient-to-r from-amber-400 to-orange-400 text-white shadow-md hover:from-amber-500 hover:to-orange-500"
        >
          <span>เลือกสินค้า</span>
          <svg xmlns="http://www.w3.org/2000/svg" class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 7l5 5m0 0l-5 5m5-5H6" />
          </svg>
        </NuxtLink>
      </div>

      <!-- Cart Items -->
      <div v-else class="bg-white rounded-2xl shadow-lg border border-amber-200 transition-all duration-300 hover:shadow-xl hover:scale-105 p-8">
        <div class="overflow-x-auto">
          <table class="w-full">
            <thead>
              <tr class="border-b border-amber-200">
                <th class="py-4 text-left text-amber-700 font-semibold">สินค้า</th>
                <th class="py-4 text-left text-amber-700 font-semibold">ราคา</th>
                <th class="py-4 text-left text-amber-700 font-semibold">จำนวน</th>
                <th class="py-4 text-left text-amber-700 font-semibold">รวม</th>
                <th class="py-4 text-left text-amber-700 font-semibold"></th>
              </tr>
            </thead>
            <tbody>
              <tr 
                v-for="it in items" 
                :key="it.id" 
                class="border-b border-amber-100 hover:bg-amber-50/50 transition-colors duration-200"
              >
                <td class="py-4">
                  <div class="flex items-center gap-4">
                    <div class="w-16 h-16 rounded-xl overflow-hidden bg-gradient-to-br from-amber-100 to-orange-100 flex items-center justify-center">
                      <img 
                        v-if="it.image_url" 
                        :src="API + it.image_url" 
                        class="w-full h-full object-cover" 
                        :alt="it.name"
                      />
                      <span v-else class="text-2xl">🍰</span>
                    </div>
                    <span class="font-semibold text-amber-800">{{ it.name }}</span>
                  </div>
                </td>
                <td class="py-4">
                  <span class="font-medium text-amber-700">฿{{ it.price }}</span>
                </td>
                <td class="py-4">
                  <input 
                    type="number" 
                    min="1" 
                    v-model.number="it.quantity" 
                    class="w-20 border border-amber-200 rounded-lg px-3 py-2 text-center focus:outline-none focus:ring-2 focus:ring-amber-300 focus:border-transparent transition-all duration-200" 
                  />
                </td>
                <td class="py-4">
                  <span class="font-bold text-amber-600">฿{{ (it.price * it.quantity).toFixed(2) }}</span>
                </td>
                <td class="py-4">
                  <button 
                    @click="remove(it.id)" 
                    class="text-red-500 hover:text-red-700 hover:bg-red-50 p-2 rounded-full transition-all duration-200 hover:scale-110"
                    title="ลบสินค้า"
                  >
                    <svg xmlns="http://www.w3.org/2000/svg" class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
                    </svg>
                  </button>
                </td>
              </tr>
            </tbody>
          </table>
        </div>

        <!-- Order Details -->
        <div class="mt-8 p-6 bg-gradient-to-r from-amber-50 to-orange-50 rounded-2xl border border-amber-200">
          <div class="flex flex-col sm:flex-row gap-4 sm:items-center sm:justify-between mb-6">
            <div class="flex items-center gap-3">
              <label class="text-sm font-medium text-amber-700">โต๊ะ/ชื่อลูกค้า</label>
              <input 
                v-model="table" 
                placeholder="เช่น โต๊ะ 5 หรือ ชื่อลูกค้า" 
                class="border border-amber-200 rounded-lg px-4 py-2 focus:outline-none focus:ring-2 focus:ring-amber-300 focus:border-transparent transition-all duration-200" 
              />
            </div>
            <div class="text-2xl font-bold text-transparent bg-clip-text bg-gradient-to-r from-amber-600 to-orange-600">
              รวม: ฿{{ total.toFixed(2) }}
            </div>
          </div>

          <div class="flex justify-end">
            <button 
              @click="checkout" 
              class="inline-flex items-center gap-2 px-6 py-3 rounded-full font-medium transition-all duration-300 transform hover:scale-105 hover:shadow-lg bg-gradient-to-r from-emerald-400 to-teal-400 text-white shadow-md hover:from-emerald-500 hover:to-teal-500 text-lg px-8 py-4"
            >
              <span>สั่งซื้อ</span>
              <svg xmlns="http://www.w3.org/2000/svg" class="w-6 h-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" />
              </svg>
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- Success Modal -->
    <div 
      v-if="successOpen" 
      class="fixed inset-0 bg-black/50 backdrop-blur-sm flex items-center justify-center p-4 z-50"
    >
      <div class="bg-white rounded-2xl shadow-lg border border-amber-200 transition-all duration-300 hover:shadow-xl hover:scale-105 p-8 w-full max-w-md text-center transform transition-all duration-300 scale-100">
        <div class="text-6xl mb-4">🎉</div>
        <h3 class="text-2xl font-bold text-amber-800 mb-2">สั่งรายการสำเร็จ!</h3>
        <p class="text-amber-700 mb-6">ขอบคุณที่ใช้บริการของเรา</p>
        <div class="text-xl font-bold text-amber-600 mb-6">ยอดรวม ฿{{ lastTotal.toFixed(2) }}</div>
        <button 
          @click="successOpen = false" 
          class="inline-flex items-center gap-2 px-6 py-3 rounded-full font-medium transition-all duration-300 transform hover:scale-105 hover:shadow-lg bg-gradient-to-r from-amber-400 to-orange-400 text-white shadow-md hover:from-amber-500 hover:to-orange-500 w-full"
        >
          ปิด
        </button>
      </div>
    </div>

    <!-- Error Modal -->
    <div 
      v-if="errorOpen" 
      class="fixed inset-0 bg-black/50 backdrop-blur-sm flex items-center justify-center p-4 z-50"
    >
      <div class="bg-white rounded-2xl shadow-lg border border-amber-200 transition-all duration-300 hover:shadow-xl hover:scale-105 p-8 w-full max-w-md text-center transform transition-all duration-300 scale-100">
        <div class="text-6xl mb-4">⚠️</div>
        <h3 class="text-2xl font-bold text-amber-800 mb-2">สั่งซื้อไม่สำเร็จ</h3>
        <p class="text-amber-700 mb-6">{{ errorMsg }}</p>
        <button 
          @click="errorOpen = false" 
          class="inline-flex items-center gap-2 px-6 py-3 rounded-full font-medium transition-all duration-300 transform hover:scale-105 hover:shadow-lg bg-gradient-to-r from-pink-400 to-rose-400 text-white shadow-md hover:from-pink-500 hover:to-rose-500 w-full"
        >
          ลองใหม่
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useCart } from '~/composables/useCart'

const config = useRuntimeConfig()
const API = config.public.apiBase

const { items, remove, total, clear } = useCart()
const table = ref('')
const successOpen = ref(false)
const errorOpen = ref(false)
const errorMsg = ref('')
const lastTotal = ref(0)

const checkout = async () => {
  if (items.value.length === 0) return
  const payload = {
    items: items.value.map(i => ({ product_id: i.id, quantity: i.quantity })),
    table: table.value || ''
  }
  try {
    const res = await $fetch('/pos/checkout', { baseURL: API, method: 'POST', body: payload })
    lastTotal.value = res.total_price
    successOpen.value = true
    errorOpen.value = false
    clear()
  } catch (e) {
    errorMsg.value = e?.data?.detail || 'สั่งซื้อไม่สำเร็จ กรุณาลองใหม่'
    errorOpen.value = true
  }
}
</script>
