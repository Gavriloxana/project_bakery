<template>
  <div class="min-h-screen bg-gradient-to-br from-orange-50 via-pink-50 to-amber-50 py-8 px-4">
    <!-- Print Button - Hidden on print -->
    <div class="max-w-sm mx-auto mb-6 print:hidden">
      <button 
        @click="onPrint()" 
        class="w-full bg-rose-300 hover:bg-rose-400 text-rose-800 font-semibold py-3 px-6 rounded-full shadow-lg transition-all duration-300 hover:shadow-xl hover:scale-105 active:scale-95"
      >
        🖨️ พิมพ์ใบเสร็จ
      </button>
    </div>

    <!-- Receipt Container -->
    <div class="max-w-sm mx-auto bg-white shadow-2xl rounded-2xl overflow-hidden border border-amber-100">
      <!-- Header Section -->
      <div class="bg-gradient-to-r from-amber-100 via-rose-100 to-orange-100 px-6 py-8 text-center border-b-2 border-dashed border-amber-200">
        <div class="mb-4">
          <h1 class="text-2xl font-bold text-amber-800 mb-1">🧁 Sweet Dreams</h1>
          <p class="text-sm text-amber-700 font-medium">Artisan Bakery & Café</p>
          <p class="text-xs text-amber-600 mt-1">123 Bakery Street, Bangkok</p>
          <p class="text-xs text-amber-600">Tel: 02-xxx-xxxx</p>
        </div>
        
        <!-- Receipt Info -->
        <div class="bg-white/70 rounded-lg p-3 mt-4 text-xs">
          <div class="grid grid-cols-2 gap-2 text-left">
            <div>
              <span class="text-gray-600">วันที่:</span>
              <span class="font-medium text-gray-800 ml-1">{{ currentDate }}</span>
            </div>
            <div>
              <span class="text-gray-600">เวลา:</span>
              <span class="font-medium text-gray-800 ml-1">{{ currentTime }}</span>
            </div>
            <div>
              <span class="text-gray-600">โต๊ะ:</span>
              <span class="font-medium text-gray-800 ml-1">{{ table || '-' }}</span>
            </div>
            <div>
              <span class="text-gray-600">ใบเสร็จ:</span>
              <span class="font-medium text-gray-800 ml-1">#{{ receiptNumber }}</span>
            </div>
          </div>
        </div>
      </div>

      <!-- Items Section -->
      <div class="px-6 py-4">
        <h3 class="text-sm font-semibold text-gray-700 mb-3 text-center border-b border-gray-200 pb-2">
          รายการสินค้า
        </h3>
        
        <div v-if="orders.length === 0" class="text-center py-8 text-gray-500">
          <div class="text-4xl mb-2">🍰</div>
          <p class="text-sm">ไม่มีรายการสินค้า</p>
        </div>

        <div v-for="o in orders" :key="o.id" class="mb-4">
          <div class="space-y-2">
            <div v-for="item in o.items" :key="item.product_id" class="flex justify-between items-start text-sm">
              <div class="flex-1">
                <div class="font-medium text-gray-800">{{ item.name }}</div>
                <div class="text-gray-500 text-xs">
                  ฿{{ item.unit_price }} × {{ item.quantity }}
                </div>
              </div>
              <div class="font-semibold text-gray-800 ml-2">
                ฿{{ item.subtotal }}
              </div>
            </div>
          </div>
          
          <!-- Order Actions -->
          <div class="flex justify-end mt-2 print:hidden">
            <button 
              @click="remove(o.id)" 
              class="text-red-500 hover:text-red-700 text-xs px-2 py-1 rounded hover:bg-red-50 transition-colors"
            >
              ลบออเดอร์
            </button>
          </div>
          
          <div v-if="orders.length > 1 && o !== orders[orders.length - 1]" class="border-b border-dashed border-gray-200 my-3"></div>
        </div>
      </div>

      <!-- Summary Section -->
      <div class="px-6 py-4 bg-gradient-to-r from-amber-50 to-rose-50 border-t-2 border-dashed border-amber-200">
        <div class="space-y-2">
          <div class="flex justify-between text-sm">
            <span class="text-gray-600">ยอดรวม:</span>
            <span class="font-medium text-gray-800">฿{{ grandTotal }}</span>
          </div>
          <div class="flex justify-between text-sm">
            <span class="text-gray-600">ส่วนลด:</span>
            <span class="font-medium text-gray-800">฿0.00</span>
          </div>
          <div class="flex justify-between text-sm">
            <span class="text-gray-600">ภาษี (7%):</span>
            <span class="font-medium text-gray-800">฿{{ taxAmount }}</span>
          </div>
          <div class="border-t border-dashed border-amber-300 pt-2 mt-3">
            <div class="flex justify-between text-lg font-bold">
              <span class="text-amber-800">รวมทั้งสิ้น:</span>
              <span class="text-amber-800">฿{{ totalWithTax }}</span>
            </div>
          </div>
        </div>
      </div>

      <!-- Footer Section -->
      <div class="px-6 py-6 text-center bg-gradient-to-r from-rose-50 to-amber-50">
        <div class="text-rose-600 font-semibold text-sm mb-2">
          🌟 ขอบคุณที่ใช้บริการ! 🌟
        </div>
        <p class="text-xs text-gray-600 leading-relaxed">
          Thank you for choosing Sweet Dreams Bakery!<br>
          มีความสุขกับของหวานของเรา ✨
        </p>
        <div class="mt-4 text-xs text-gray-500">
          <p>กรุณาเก็บใบเสร็จไว้เป็นหลักฐาน</p>
          <p class="mt-1">Follow us: @sweetdreamsbakery</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'

const route = useRoute()
const config = useRuntimeConfig()
const API = config.public.apiBase

const table = ref((route.query.table||'').toString())
type OrderItem = { product_id: string; name: string; unit_price: number; quantity: number; subtotal: number }
type Order = { id: string; items: OrderItem[]; total_price: number }
const orders = ref<Order[]>([])

// Receipt calculations
const grandTotal = computed(()=> orders.value.reduce((s:number,o:Order)=> s + o.total_price, 0))
const taxAmount = computed(() => Math.round(grandTotal.value * 0.07 * 100) / 100)
const totalWithTax = computed(() => Math.round((grandTotal.value + taxAmount.value) * 100) / 100)

// Receipt info
const currentDate = computed(() => {
  const date = new Date()
  return date.toLocaleDateString('th-TH', { 
    year: 'numeric', 
    month: '2-digit', 
    day: '2-digit' 
  })
})

const currentTime = computed(() => {
  const date = new Date()
  return date.toLocaleTimeString('th-TH', { 
    hour: '2-digit', 
    minute: '2-digit' 
  })
})

const receiptNumber = computed(() => {
  const date = new Date()
  const timestamp = date.getTime().toString().slice(-6)
  return `R${timestamp}`
})

const load = async () => {
  if (!table.value) return
  orders.value = await $fetch(`/pos/orders/by-table/${encodeURIComponent(table.value)}`, { baseURL: API })
}

onMounted(load)

const remove = async (id: string) => {
  await $fetch(`/pos/orders/${id}`, { baseURL: API, method: 'DELETE' })
  await load()
}

onMounted(() => {
  const done = () => {
    if (!table.value) return
    $fetch(`/pos/orders/by-table/${encodeURIComponent(table.value)}`, { baseURL: API, method: 'DELETE' })
  }
  window.addEventListener('afterprint', done)
})

const onPrint = () => {
  window.print()
}
</script>

<style>
/* Print styles */
@media print {
  body {
    margin: 0;
    padding: 0;
  }
  
  .print\:hidden {
    display: none !important;
  }
  
  /* Optimize receipt for printing */
  .max-w-sm {
    max-width: 100% !important;
    margin: 0 !important;
  }
  
  .shadow-2xl, .shadow-lg {
    box-shadow: none !important;
  }
  
  .rounded-2xl {
    border-radius: 0 !important;
  }
  
  .bg-gradient-to-br,
  .bg-gradient-to-r {
    background: white !important;
  }
  
  /* Ensure good contrast for printing */
  .text-amber-800,
  .text-rose-600,
  .text-gray-800 {
    color: #000 !important;
  }
  
  .text-gray-600,
  .text-gray-500 {
    color: #333 !important;
  }
}
</style>
