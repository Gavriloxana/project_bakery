<template>
  <!-- Background with bakery theme -->
  <div class="min-h-screen bg-gradient-to-br from-orange-50 via-pink-50 to-yellow-50 py-8 px-4">
    <!-- Print Button - Hidden during print -->
    <div class="flex justify-center mb-8 print:hidden">
      <button 
        @click="onPrint()" 
        class="bg-gradient-to-r from-pink-200 to-rose-200 hover:from-pink-300 hover:to-rose-300 text-rose-800 font-semibold px-8 py-3 rounded-full shadow-lg hover:shadow-xl transform hover:scale-105 transition-all duration-200 flex items-center gap-2"
      >
        <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 17h2a2 2 0 002-2v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2m2 4h6a2 2 0 002-2v-4a2 2 0 00-2-2H9a2 2 0 00-2 2v4a2 2 0 002 2zm8-12V5a2 2 0 00-2-2H9a2 2 0 00-2 2v4h10z"></path>
        </svg>
        พิมพ์ใบเสร็จ
      </button>
    </div>

    <!-- Receipt Container -->
    <div class="max-w-sm mx-auto bg-white shadow-2xl rounded-t-3xl rounded-b-lg overflow-hidden print:shadow-none print:max-w-none print:mx-0">
      <!-- Header with Bakery Branding -->
      <div class="bg-gradient-to-r from-amber-100 via-orange-100 to-pink-100 px-6 py-8 text-center border-b-4 border-dashed border-amber-200">
        <!-- Bakery Logo/Icon -->
        <div class="flex justify-center mb-3">
          <div class="w-16 h-16 bg-gradient-to-br from-orange-200 to-pink-200 rounded-full flex items-center justify-center shadow-lg">
            <svg class="w-8 h-8 text-amber-700" fill="currentColor" viewBox="0 0 24 24">
              <path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm-2 15l-5-5 1.41-1.41L10 14.17l7.59-7.59L19 8l-9 9z"/>
            </svg>
          </div>
        </div>
        
        <!-- Bakery Name -->
        <h1 class="text-2xl font-bold text-amber-800 mb-1" style="font-family: 'Georgia', serif;">Sweet Dreams Bakery</h1>
        <p class="text-sm text-amber-600 font-medium">~ Freshly Baked with Love ~</p>
        <p class="text-xs text-amber-500 mt-2">123 Baker Street, Sweet Town</p>
        <p class="text-xs text-amber-500">Tel: (555) 123-CAKE</p>
      </div>

      <!-- Receipt Details -->
      <div class="px-6 py-4 bg-cream-50 border-b border-amber-100">
        <div class="flex justify-between items-center mb-2">
          <span class="text-sm font-semibold text-amber-800">Receipt #:</span>
          <span class="text-sm text-amber-700">#{{ String(Date.now()).slice(-6) }}</span>
        </div>
        <div class="flex justify-between items-center mb-2">
          <span class="text-sm font-semibold text-amber-800">Table:</span>
          <span class="text-sm text-amber-700">{{ table || 'N/A' }}</span>
        </div>
        <div class="flex justify-between items-center mb-2">
          <span class="text-sm font-semibold text-amber-800">Date:</span>
          <span class="text-sm text-amber-700">{{ formatDate(new Date()) }}</span>
        </div>
        <div class="flex justify-between items-center mb-2">
          <span class="text-sm font-semibold text-amber-800">Cashier:</span>
          <span class="text-sm text-amber-700">Admin</span>
        </div>
      </div>

      <!-- Items Section -->
      <div class="px-6 py-4">
        <h3 class="text-lg font-bold text-amber-800 mb-4 text-center border-b border-dashed border-amber-200 pb-2">Order Details</h3>
        
        <!-- Items List -->
        <div v-for="(o, orderIndex) in orders" :key="o.id" class="mb-6">
          <div v-if="orders.length > 1" class="text-xs text-amber-600 font-semibold mb-2 bg-amber-50 px-2 py-1 rounded">
            Order {{ orderIndex + 1 }}
          </div>
          
          <div v-for="item in o.items" :key="item.product_id" class="flex justify-between items-center py-2 border-b border-dotted border-amber-100 last:border-0">
            <div class="flex-1">
              <div class="font-medium text-amber-800 text-sm">{{ item.name }}</div>
              <div class="text-xs text-amber-600">{{ item.quantity }} × ฿{{ item.unit_price }}</div>
            </div>
            <div class="text-sm font-semibold text-amber-800 ml-4">
              ฿{{ item.subtotal }}
            </div>
          </div>

          <!-- Order Subtotal -->
          <div v-if="orders.length > 1" class="flex justify-between items-center mt-2 pt-2 border-t border-amber-200 font-semibold text-amber-800">
            <span class="text-sm">Order {{ orderIndex + 1 }} Total:</span>
            <span class="text-sm">฿{{ o.total_price }}</span>
          </div>

          <!-- Remove Order Button (Hidden during print) -->
          <div class="text-right mt-3 print:hidden">
            <button 
              @click="remove(o.id)" 
              class="text-xs text-red-500 hover:text-red-700 hover:bg-red-50 px-2 py-1 rounded transition-colors duration-200"
            >
              Remove Order
            </button>
          </div>
        </div>
      </div>

      <!-- Summary Section -->
      <div class="px-6 py-4 bg-gradient-to-r from-amber-50 to-orange-50 border-t-2 border-dashed border-amber-200">
        <!-- Subtotal -->
        <div class="flex justify-between items-center py-1">
          <span class="text-sm text-amber-700">Subtotal:</span>
          <span class="text-sm text-amber-700">฿{{ grandTotal }}</span>
        </div>
        
        <!-- Discount -->
        <div class="flex justify-between items-center py-1">
          <span class="text-sm text-amber-700">Discount:</span>
          <span class="text-sm text-amber-700">฿0.00</span>
        </div>
        
        <!-- Tax -->
        <div class="flex justify-between items-center py-1 border-b border-dotted border-amber-300 pb-2">
          <span class="text-sm text-amber-700">Tax (7%):</span>
          <span class="text-sm text-amber-700">฿{{ (grandTotal * 0.07).toFixed(2) }}</span>
        </div>
        
        <!-- Grand Total -->
        <div class="flex justify-between items-center py-3 bg-gradient-to-r from-amber-100 to-orange-100 -mx-6 px-6 mt-2 rounded-lg">
          <span class="text-lg font-bold text-amber-800">TOTAL:</span>
          <span class="text-xl font-bold text-amber-800">฿{{ (grandTotal * 1.07).toFixed(2) }}</span>
        </div>
      </div>

      <!-- Payment Info -->
      <div class="px-6 py-4 bg-pink-50 border-t border-pink-100">
        <div class="flex justify-between items-center mb-2">
          <span class="text-sm text-pink-700">Payment Method:</span>
          <span class="text-sm font-medium text-pink-800">Cash</span>
        </div>
        <div class="flex justify-between items-center">
          <span class="text-sm text-pink-700">Change:</span>
          <span class="text-sm font-medium text-pink-800">฿0.00</span>
        </div>
      </div>

      <!-- Footer -->
      <div class="px-6 py-6 bg-gradient-to-r from-orange-100 via-pink-100 to-yellow-100 text-center border-t-2 border-dashed border-amber-200">
        <div class="mb-4">
          <p class="text-lg font-bold text-amber-800 mb-2">🍰 Thank you for your purchase! 🍰</p>
          <p class="text-sm text-amber-600 mb-1">Have a sweet day ahead!</p>
          <p class="text-xs text-amber-500">Visit us again for more delicious treats</p>
        </div>
        
        <!-- Rating prompt -->
        <div class="border-t border-dashed border-amber-200 pt-4">
          <p class="text-xs text-amber-500 mb-2">Rate your experience:</p>
          <div class="flex justify-center gap-1">
            <span v-for="i in 5" :key="i" class="text-yellow-400 text-lg">⭐</span>
          </div>
          <p class="text-xs text-amber-500 mt-1">sweetdreamsbakery.com/feedback</p>
        </div>
      </div>
    </div>

    <!-- Bottom spacing for print -->
    <div class="h-8 print:hidden"></div>
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

const grandTotal = computed(()=> orders.value.reduce((s:number,o:Order)=> s + o.total_price, 0))

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

// Helper function to format date
const formatDate = (date: Date) => {
  const options: Intl.DateTimeFormatOptions = {
    year: 'numeric',
    month: 'short',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit'
  }
  return date.toLocaleDateString('en-US', options)
}
</script>

<style>
/* Print-specific styles */
@media print {
  /* Reset page margins for cleaner print */
  @page {
    margin: 0.5in;
    size: auto;
  }
  
  /* Ensure receipt stays compact on print */
  body {
    background: white !important;
  }
  
  /* Hide elements that shouldn't print */
  .print\\:hidden {
    display: none !important;
  }
  
  /* Adjust receipt container for print */
  .print\\:shadow-none {
    box-shadow: none !important;
  }
  
  .print\\:max-w-none {
    max-width: none !important;
  }
  
  .print\\:mx-0 {
    margin-left: 0 !important;
    margin-right: 0 !important;
  }
  
  /* Ensure all text is black for print */
  * {
    color-adjust: exact !important;
    -webkit-print-color-adjust: exact !important;
  }
  
  /* Prevent page breaks within receipt sections */
  .receipt-section {
    page-break-inside: avoid;
  }
}

/* Custom color classes for cream backgrounds */
.bg-cream-50 {
  background-color: #fefdf8;
}
</style>
