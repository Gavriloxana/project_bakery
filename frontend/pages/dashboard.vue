<template>
  <div class="min-h-screen bg-bakery-gradient p-4 sm:p-6 lg:p-8">
    <div class="max-w-7xl mx-auto font-sans">
      <!-- Header -->
      <div class="flex flex-col sm:flex-row justify-between items-start sm:items-center mb-8 gap-4">
        <div>
          <h1 class="text-4xl font-bold text-transparent bg-clip-text bg-gradient-to-r from-amber-600 to-orange-600 mb-2">
            🍰 POS Dashboard
          </h1>
          <p class="text-amber-700">จัดการร้านเบเกอรี่ของคุณ</p>
        </div>
        <div class="flex items-center gap-3">
          <button 
            @click="logout" 
            class="inline-flex items-center gap-2 px-6 py-3 rounded-full font-medium transition-all duration-300 transform hover:scale-105 hover:shadow-lg bg-gradient-to-r from-pink-400 to-rose-400 text-white shadow-md hover:from-pink-500 hover:to-rose-500 text-sm"
          >
            <span>ออกจากระบบ</span>
            <svg xmlns="http://www.w3.org/2000/svg" class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1" />
            </svg>
          </button>
        </div>
      </div>

      <div class="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-6">
        <!-- Products Section -->
        <section class="bg-white rounded-2xl shadow-lg border border-amber-200 transition-all duration-300 hover:shadow-xl hover:scale-105 p-6 col-span-1 md:col-span-2 xl:col-span-2">
          <h2 class="font-bold text-xl text-amber-800 mb-6 flex items-center gap-2">
            <span class="text-2xl">📦</span>
            จัดการสินค้า
          </h2>
          
          <div class="flex flex-col lg:flex-row flex-wrap gap-4 mb-6 items-start lg:items-center">
            <input 
              v-model="productForm.name" 
              placeholder="ชื่อสินค้า" 
              class="border border-amber-200 p-3 flex-1 rounded-xl focus:outline-none focus:ring-2 focus:ring-amber-300 focus:border-transparent transition-all duration-200 bg-white/80 backdrop-blur-sm" 
            />
            <input 
              v-model.number="productForm.price" 
              placeholder="ราคา" 
              type="number" 
              class="border border-amber-200 p-3 w-full sm:w-32 rounded-xl focus:outline-none focus:ring-2 focus:ring-amber-300 focus:border-transparent transition-all duration-200 bg-white/80 backdrop-blur-sm" 
            />
            <input 
              v-model.number="productForm.stock" 
              placeholder="สต๊อก" 
              type="number" 
              class="border border-amber-200 p-3 w-full sm:w-28 rounded-xl focus:outline-none focus:ring-2 focus:ring-amber-300 focus:border-transparent transition-all duration-200 bg-white/80 backdrop-blur-sm" 
            />
            <input 
              type="file" 
              accept="image/*" 
              @change="onFileChange" 
              class="border border-amber-200 p-3 rounded-xl file:mr-4 file:py-2 file:px-4 file:rounded-lg file:border-0 file:text-sm file:font-medium file:bg-amber-50 file:text-amber-700 hover:file:bg-amber-100 transition-all duration-200" 
            />
            <button 
              @click="saveProduct" 
              class="inline-flex items-center gap-2 px-6 py-3 rounded-full font-medium transition-all duration-300 transform hover:scale-105 hover:shadow-lg bg-gradient-to-r from-amber-400 to-orange-400 text-white shadow-md hover:from-amber-500 hover:to-orange-500 self-stretch lg:self-auto"
            >
              <span>บันทึก</span>
              <svg xmlns="http://www.w3.org/2000/svg" class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" />
              </svg>
            </button>
          </div>
          
          <div class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-4 max-h-[70vh] overflow-auto">
            <div 
              v-for="p in products" 
              :key="p.id" 
              class="bg-white rounded-2xl shadow-lg border border-amber-200 transition-all duration-300 hover:shadow-xl hover:scale-105 p-4 hover:scale-105 transition-all duration-300"
            >
              <div class="relative overflow-hidden rounded-xl mb-3">
                <img 
                  v-if="p.image_url" 
                  :src="API + p.image_url" 
                  :alt="p.name" 
                  class="w-full h-32 object-cover" 
                />
                <div v-else class="w-full h-32 bg-gradient-to-br from-amber-100 to-orange-100 flex items-center justify-center">
                  <span class="text-3xl">🍰</span>
                </div>
              </div>
              <div class="font-semibold text-amber-800 text-center mb-2">{{ p.name }}</div>
              <div class="text-sm text-amber-700 text-center mb-3">฿{{ p.price }} | คงเหลือ {{ p.stock }}</div>
              <div class="flex justify-center gap-2">
                <button 
                  @click="editProduct(p)" 
                  class="px-3 py-2 text-sm bg-blue-500 text-white rounded-lg hover:bg-blue-600 transition-all duration-200 hover:scale-105"
                >
                  แก้ไข
                </button>
                <button 
                  @click="removeProduct(p.id)" 
                  class="px-3 py-2 text-sm bg-red-500 text-white rounded-lg hover:bg-red-600 transition-all duration-200 hover:scale-105"
                >
                  ลบ
                </button>
              </div>
            </div>
          </div>
        </section>

        <!-- Sales Section -->
        <section class="bg-white rounded-2xl shadow-lg border border-amber-200 transition-all duration-300 hover:shadow-xl hover:scale-105 p-6 col-span-1 lg:col-span-1">
          <h2 class="font-bold text-xl text-amber-800 mb-6 flex items-center gap-2">
            <span class="text-2xl">💰</span>
            ขายสินค้า
          </h2>
          
          <div class="space-y-4">
            <select 
              v-model="saleForm.product_id" 
              class="w-full border border-amber-200 p-3 rounded-xl focus:outline-none focus:ring-2 focus:ring-amber-300 focus:border-transparent transition-all duration-200 bg-white/80 backdrop-blur-sm"
            >
              <option disabled value="">เลือกสินค้า</option>
              <option v-for="p in products" :key="p.id" :value="p.id">
                {{ p.name }} (฿{{ p.price }})
              </option>
            </select>
            
            <input 
              v-model.number="saleForm.quantity" 
              type="number" 
              min="1" 
              placeholder="จำนวน" 
              class="w-full border border-amber-200 p-3 rounded-xl focus:outline-none focus:ring-2 focus:ring-amber-300 focus:border-transparent transition-all duration-200 bg-white/80 backdrop-blur-sm" 
            />
            
            <button 
              @click="createSale" 
              class="w-full inline-flex items-center gap-2 px-6 py-3 rounded-full font-medium transition-all duration-300 transform hover:scale-105 hover:shadow-lg bg-gradient-to-r from-emerald-400 to-teal-400 text-white shadow-md hover:from-emerald-500 hover:to-teal-500"
            >
              <span>ขายสินค้า</span>
              <svg xmlns="http://www.w3.org/2000/svg" class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6v6m0 0v6m0-6h6m-6 0H6" />
              </svg>
            </button>
            
            <p v-if="saleMessage" class="text-green-600 text-sm bg-green-50 p-3 rounded-lg border border-green-200">
              {{ saleMessage }}
            </p>
            <p v-if="saleError" class="text-red-600 text-sm bg-red-50 p-3 rounded-lg border border-red-200">
              {{ saleError }}
            </p>
            
            <div class="mt-4">
              <NuxtLink 
                to="/cart" 
                class="text-amber-600 text-sm hover:text-amber-800 font-medium hover:underline transition-all duration-200"
              >
                เปิดตะกร้าลูกค้า →
              </NuxtLink>
            </div>
          </div>
        </section>

        <!-- Reports Section -->
        <section class="bg-white rounded-2xl shadow-lg border border-amber-200 transition-all duration-300 hover:shadow-xl hover:scale-105 p-6 col-span-1 lg:col-span-1">
          <h2 class="font-bold text-xl text-amber-800 mb-6 flex items-center gap-2">
            <span class="text-2xl">📊</span>
            สรุปรายงาน
          </h2>
          
          <div class="grid grid-cols-1 sm:grid-cols-2 gap-4 mb-6">
            <div class="bg-gradient-to-br from-amber-50 to-orange-50 rounded-xl p-4 border border-amber-200">
              <div class="text-sm text-amber-700 mb-1">ยอดขายรวม</div>
              <div class="text-2xl font-bold text-amber-600">฿{{ reports.total_sales }}</div>
            </div>
            <div class="bg-gradient-to-br from-pink-50 to-rose-50 rounded-xl p-4 border border-pink-200">
              <div class="text-sm text-pink-700 mb-1">จำนวนบิล</div>
              <div class="text-2xl font-bold text-pink-600">{{ reports.total_transactions }}</div>
            </div>
          </div>
          
          <div class="border-t border-amber-200 pt-4 max-h-52 overflow-auto">
            <h4 class="font-semibold text-amber-700 mb-3">สต๊อกสินค้า</h4>
            <div v-for="s in stocks" :key="s.name" class="flex justify-between text-sm text-amber-700 py-2 hover:bg-amber-50 rounded-lg px-2 transition-colors duration-200">
              <span>{{ s.name }}</span>
              <span class="font-medium">คงเหลือ {{ s.stock }}</span>
            </div>
          </div>
        </section>

        <!-- Table Orders Section -->
        <section class="bg-white rounded-2xl shadow-lg border border-amber-200 transition-all duration-300 hover:shadow-xl hover:scale-105 p-6 col-span-1 lg:col-span-1">
          <h2 class="font-bold text-xl text-amber-800 mb-6 flex items-center gap-2">
            <span class="text-2xl">🪑</span>
            ออเดอร์ตามโต๊ะ
          </h2>
          
          <div class="space-y-4 max-h-80 overflow-auto">
            <div 
              v-for="(list, table) in grouped" 
              :key="table" 
              class="border border-amber-200 rounded-xl overflow-hidden hover:shadow-lg transition-all duration-300"
            >
              <div class="px-4 py-3 flex justify-between items-center bg-gradient-to-r from-amber-50 to-orange-50">
                <div class="font-semibold text-amber-800">โต๊ะ: {{ table || '-' }}</div>
                <div class="text-sm text-amber-700 flex items-center gap-3">
                  <span class="font-medium">รวม ฿{{ list.reduce((s,o)=>s+o.total_price,0) }}</span>
                  <NuxtLink 
                    :to="`/receipt?table=${encodeURIComponent(table)}`" 
                    class="text-amber-600 hover:text-amber-800 hover:underline transition-all duration-200"
                  >
                    พิมพ์ใบเสร็จ
                  </NuxtLink>
                  <button 
                    @click="deleteTableOrders(table)" 
                    class="px-3 py-1 rounded-lg bg-red-500 text-white hover:bg-red-600 transition-all duration-200 hover:scale-105 text-sm"
                  >
                    ลบทั้งหมด
                  </button>
                </div>
              </div>
              
              <div class="p-4 space-y-3">
                <div 
                  v-for="o in list" 
                  :key="o.id" 
                  class="border border-amber-200 rounded-lg p-3 bg-gradient-to-br from-amber-50/50 to-orange-50/50"
                >
                  <ul class="text-sm text-amber-700 list-disc pl-5 mb-2">
                    <li v-for="it in o.items" :key="it.product_id">
                      {{ it.name }} x {{ it.quantity }} = ฿{{ it.subtotal }}
                    </li>
                  </ul>
                  <div class="text-right text-sm font-semibold text-amber-800">ยอดบิล: ฿{{ o.total_price }}</div>
                </div>
              </div>
            </div>
          </div>
        </section>
      </div>
    </div>
    
    <!-- Loading Overlay -->
    <div 
      v-if="loading" 
      class="fixed inset-0 flex items-center justify-center bg-white/80 backdrop-blur-sm z-50"
    >
      <div class="text-center">
        <div class="text-4xl mb-4 animate-bounce-soft">🍰</div>
        <div class="text-lg font-medium text-amber-700">กำลังโหลด...</div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
definePageMeta({ middleware: ['auth'] })

// ใช้ https เท่านั้น
const API = "https://lab.loeitech.org/"

const loading = ref(false)

// products
const products = ref([])
const productForm = ref({ id: null, name: '', price: 0, stock: 0 })
const fileRef = ref(null)

// sale
const saleForm = ref({ product_id: '', quantity: 1 })
const saleMessage = ref('')
const saleError = ref('')

// reports
const reports = ref({ total_sales: 0, total_transactions: 0 })
const stocks = ref([])
const orders = ref([])
const grouped = computed(() => {
  const map = {}
  for (const o of orders.value) {
    const key = o.table || '-'
    if (!map[key]) map[key] = []
    map[key].push(o)
  }
  return map
})

// ดึงสินค้าทั้งหมด
const fetchProducts = async () => {
  const res = await $fetch('/products', { baseURL: API })
  // บังคับให้ image_url เป็น https เสมอ
  products.value = res.map(p => ({
    ...p,
    image_url: p.image_url ? p.image_url.replace(/^http:\/\//i, 'https://') : null
  }))
}

const saveProduct = async () => {
  loading.value = true
  try {
    if (productForm.value.id) {
      const id = productForm.value.id
      const { name, price, stock } = productForm.value
      await $fetch(`/products/${id}`, { baseURL: API, method: 'PUT', body: { name, price, stock } })
      if (fileRef.value) {
        const form = new FormData()
        form.append('file', fileRef.value)
        await $fetch(`/products/${id}/image`, { baseURL: API, method: 'POST', body: form })
      }
    } else {
      const { name, price, stock } = productForm.value
      const created = await $fetch('/products/', { baseURL: API, method: 'POST', body: { name, price, stock } })
      if (fileRef.value) {
        const form = new FormData()
        form.append('file', fileRef.value)
        await $fetch(`/products/${created.id}/image`, { baseURL: API, method: 'POST', body: form })
      }
    }
    productForm.value = { id: null, name: '', price: 0, stock: 0 }
    fileRef.value = null
    await fetchProducts()
  } catch (e) {
    console.error('Save product error:', e)
  } finally {
    loading.value = false
  }
}

const editProduct = (p) => {
  productForm.value = { id: p.id, name: p.name, price: p.price, stock: p.stock }
  fileRef.value = null
}

const removeProduct = async (id) => {
  loading.value = true
  try {
    await $fetch(`/products/${id}`, { baseURL: API, method: 'DELETE' })
    await fetchProducts()
  } finally {
    loading.value = false
  }
}

const createSale = async () => {
  saleMessage.value = ''
  saleError.value = ''
  try {
    const { product_id, quantity } = saleForm.value
    const res = await $fetch('/pos/sale', { baseURL: API, method: 'POST', body: { product_id, quantity } })
    saleMessage.value = `ขายสำเร็จ ยอดรวม ฿${res.total_price}`
    saleForm.value = { product_id: '', quantity: 1 }
    await fetchProducts()
    await fetchReports()
  } catch (e) {
    saleError.value = e?.data?.detail || 'ขายไม่สำเร็จ'
  }
}

const fetchReports = async () => {
  const summary = await $fetch('/reports/sales', { baseURL: API })
  reports.value = summary
  const st = await $fetch('/reports/stock', { baseURL: API })
  stocks.value = st
}

const fetchOrders = async () => {
  orders.value = await $fetch('/pos/orders', { baseURL: API })
}

const deleteTableOrders = async (table) => {
  const key = (!table || table === '-' ? '' : table)
  await $fetch(`/pos/orders/by-table/${encodeURIComponent(key)}`, { baseURL: API, method: 'DELETE' })
  await fetchOrders()
}

const logout = () => {
  localStorage.removeItem('is_admin')
  navigateTo('/login')
}

onMounted(async () => {
  await Promise.all([fetchProducts(), fetchReports(), fetchOrders()])
  setInterval(fetchOrders, 5000)
})

function onFileChange(e) {
  const f = e.target.files?.[0]
  if (f) fileRef.value = f
}
</script>

