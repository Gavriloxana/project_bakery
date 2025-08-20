<template>
  <div class="p-4 sm:p-6 lg:p-8 max-w-7xl mx-auto font-sans">
    <div class="flex flex-col sm:flex-row justify-between items-start sm:items-center mb-6 gap-4">
      <h1 class="text-3xl font-extrabold text-gray-900 tracking-tight">POS Dashboard</h1>
      <div class="flex items-center gap-3">
        <button @click="logout" class="px-4 py-2 bg-gray-700 text-white rounded-lg hover:bg-gray-800 transition-colors duration-200 text-sm font-medium">Logout</button>
      </div>
    </div>

    <div class="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-4 sm:gap-6">
      <section class="bg-white rounded-xl shadow-sm p-4 sm:p-6 col-span-1 md:col-span-2 xl:col-span-2">
  <h2 class="font-semibold text-lg text-gray-800 mb-4">สินค้า</h2>
  <div class="flex flex-col lg:flex-row flex-wrap gap-3 mb-6 items-start lg:items-center">
    <input v-model="productForm.name" placeholder="ชื่อสินค้า" class="border border-gray-300 p-2 flex-1 rounded-lg focus:outline-none focus:ring-2 focus:ring-indigo-500 transition-colors" />
    <input v-model.number="productForm.price" placeholder="ราคา" type="number" class="border border-gray-300 p-2 w-full sm:w-28 rounded-lg focus:outline-none focus:ring-2 focus:ring-indigo-500 transition-colors" />
    <input v-model.number="productForm.stock" placeholder="สต๊อก" type="number" class="border border-gray-300 p-2 w-full sm:w-24 rounded-lg focus:outline-none focus:ring-2 focus:ring-indigo-500 transition-colors" />
    <input type="file" accept="image/*" @change="onFileChange" class="border border-gray-300 p-2 rounded-lg file:mr-4 file:py-2 file:px-4 file:rounded-lg file:border-0 file:text-sm file:font-medium file:bg-indigo-50 file:text-indigo-700 hover:file:bg-indigo-100" />
    <button @click="saveProduct" class="border border-gray-300 p-2 rounded-lg bg-indigo-600 text-white hover:bg-indigo-700 transition-colors duration-200 font-medium self-stretch lg:self-auto">บันทึก</button>
  </div>
  <div class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-4 max-h-[70vh] overflow-auto">
    <div v-for="p in products" :key="p.id" class="bg-white rounded-lg shadow-md p-3 hover:shadow-lg transition-shadow duration-200">
      <img v-if="p.image_url" :src="API + p.image_url" alt="" class="w-full h-32 object-cover rounded-lg mb-2" />
      <div class="font-medium text-gray-800 text-center">{{ p.name }}</div>
      <div class="text-sm text-gray-500 text-center">฿{{ p.price }} | คงเหลือ {{ p.stock }}</div>
      <div class="flex justify-center gap-2 mt-2">
        <button @click="editProduct(p)" class="px-3 py-1 text-sm bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors">แก้ไข</button>
        <button @click="removeProduct(p.id)" class="px-3 py-1 text-sm bg-red-600 text-white rounded-lg hover:bg-red-700 transition-colors">ลบ</button>
      </div>
    </div>
  </div>
</section>

      <section class="bg-white rounded-xl shadow-sm p-4 sm:p-6 col-span-1 lg:col-span-1">
        <h2 class="font-semibold text-lg text-gray-800 mb-4">ขายสินค้า</h2>
        <div class="flex flex-col sm:flex-row gap-3 mb-4">
          <select v-model="saleForm.product_id" class="border border-gray-300 p-2 rounded-lg flex-1 focus:outline-none focus:ring-2 focus:ring-indigo-500 transition-colors">
            <option disabled value="">เลือกสินค้า</option>
            <option v-for="p in products" :key="p.id" :value="p.id">
              {{ p.name }} (฿{{ p.price }})
            </option>
          </select>
          <input v-model.number="saleForm.quantity" type="number" min="1" placeholder="จำนวน" class="border border-gray-300 p-2 w-full sm:w-28 rounded-lg focus:outline-none focus:ring-2 focus:ring-indigo-500 transition-colors" />
          <button @click="createSale" class="bg-indigo-600 text-white px-4 py-2 rounded-lg hover:bg-indigo-700 transition-colors font-medium">ขาย</button>
        </div>
        <p v-if="saleMessage" class="text-green-600 text-sm">{{ saleMessage }}</p>
        <p v-if="saleError" class="text-red-600 text-sm">{{ saleError }}</p>
        <div class="mt-4">
          <NuxtLink to="/cart" class="text-indigo-600 text-sm hover:text-indigo-800 font-medium">เปิดตะกร้าลูกค้า</NuxtLink>
        </div>
      </section>

      <section class="bg-white rounded-xl shadow-sm p-4 sm:p-6 col-span-1 lg:col-span-1">
        <h2 class="font-semibold text-lg text-gray-800 mb-4">สรุปรายงาน</h2>
        <div class="grid grid-cols-1 sm:grid-cols-2 gap-3">
          <div class="bg-gray-50 rounded-lg p-4">
            <div class="text-sm text-gray-500">ยอดขายรวม</div>
            <div class="text-xl font-bold text-gray-800">฿{{ reports.total_sales }}</div>
          </div>
          <div class="bg-gray-50 rounded-lg p-4">
            <div class="text-sm text-gray-500">จำนวนบิล</div>
            <div class="text-xl font-bold text-gray-800">{{ reports.total_transactions }}</div>
          </div>
        </div>
        <div class="mt-4 border-t border-gray-200 pt-4 max-h-52 overflow-auto">
          <div v-for="s in stocks" :key="s.name" class="flex justify-between text-sm text-gray-600 py-1">
            <span>{{ s.name }}</span>
            <span>คงเหลือ {{ s.stock }}</span>
          </div>
        </div>
      </section>

      <section class="bg-white rounded-xl shadow-sm p-4 sm:p-6 col-span-1 lg:col-span-1">
        <h2 class="font-semibold text-lg text-gray-800 mb-4">ออเดอร์ตามโต๊ะ</h2>
        <div class="space-y-4 max-h-80 overflow-auto">
          <div v-for="(list, table) in grouped" :key="table" class="border border-gray-200 rounded-lg">
            <div class="px-4 py-3 flex justify-between items-center bg-gray-50 rounded-t-lg">
              <div class="font-medium text-gray-800">โต๊ะ: {{ table || '-' }}</div>
              <div class="text-sm text-gray-600 flex items-center gap-3">
                <span>รวม ฿{{ list.reduce((s,o)=>s+o.total_price,0) }}</span>
                <NuxtLink :to="`/receipt?table=${encodeURIComponent(table)}`" class="text-indigo-600 hover:text-indigo-800">พิมพ์ใบเสร็จ</NuxtLink>
                <button @click="deleteTableOrders(table)" class="px-2 py-1 rounded bg-red-600 text-white hover:bg-red-700">ลบทั้งหมด</button>
              </div>
            </div>
            <div class="p-4 space-y-3">
              <div v-for="o in list" :key="o.id" class="border border-gray-200 rounded-lg p-3 bg-gray-50">
                <ul class="text-sm text-gray-600 list-disc pl-5">
                  <li v-for="it in o.items" :key="it.product_id">{{ it.name }} x {{ it.quantity }} = ฿{{ it.subtotal }}</li>
                </ul>
                <div class="text-right text-sm font-medium text-gray-800">ยอดบิล: ฿{{ o.total_price }}</div>
              </div>
            </div>
          </div>
        </div>
      </section>
    </div>
  </div>
  
  <div v-if="loading" class="fixed inset-0 flex items-center justify-center bg-white/80">
    <div class="text-lg font-medium text-gray-700 animate-pulse">กำลังโหลด...</div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
definePageMeta({ middleware: ['auth'] })

const config = useRuntimeConfig()
const API = config.public.apiBase

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

const fetchProducts = async () => {
  const res = await $fetch('/products', { baseURL: API })
  products.value = res
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
    // ignore
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