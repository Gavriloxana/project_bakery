<template>
  <div class="p-6 max-w-6xl mx-auto" :class="{ 'opacity-50 pointer-events-none': loading }">
    <div class="flex justify-between items-center mb-6">
      <h1 class="text-2xl font-bold">POS Dashboard</h1>
      <div class="flex items-center gap-2">
        <button @click="logout" class="px-3 py-2 bg-gray-200 rounded">Logout</button>
      </div>
    </div>

    <div class="grid grid-cols-1 lg:grid-cols-3 gap-6">
      <section class="bg-white rounded shadow p-4 col-span-1 lg:col-span-1">
        <h2 class="font-semibold mb-3">สินค้า</h2>
        <div class="flex gap-2 mb-3">
          <input v-model="productForm.name" placeholder="ชื่อสินค้า" class="border p-2 flex-1 rounded" />
          <input v-model.number="productForm.price" placeholder="ราคา" type="number" class="border p-2 w-28 rounded" />
          <input v-model.number="productForm.stock" placeholder="สต๊อก" type="number" class="border p-2 w-24 rounded" />
          <button @click="saveProduct" class="bg-green-600 text-white px-3 rounded">บันทึก</button>
        </div>
        <div class="border-t pt-3 space-y-2 max-h-72 overflow-auto">
          <div v-for="p in products" :key="p.id" class="flex items-center justify-between">
            <div>
              <div class="font-medium">{{ p.name }}</div>
              <div class="text-xs text-gray-500">฿{{ p.price }} | คงเหลือ {{ p.stock }}</div>
            </div>
            <div class="flex gap-2">
              <button @click="editProduct(p)" class="px-2 py-1 text-sm bg-blue-600 text-white rounded">แก้ไข</button>
              <button @click="removeProduct(p.id)" class="px-2 py-1 text-sm bg-red-600 text-white rounded">ลบ</button>
            </div>
          </div>
        </div>
      </section>

      <section class="bg-white rounded shadow p-4 col-span-1 lg:col-span-1">
        <h2 class="font-semibold mb-3">ขายสินค้า</h2>
        <div class="flex gap-2 mb-3">
          <select v-model.number="saleForm.product_id" class="border p-2 rounded flex-1">
            <option disabled value="">เลือกสินค้า</option>
            <option v-for="p in products" :key="p.id" :value="p.id">
              {{ p.name }} (฿{{ p.price }})
            </option>
          </select>
          <input v-model.number="saleForm.quantity" type="number" min="1" placeholder="จำนวน" class="border p-2 w-28 rounded" />
          <button @click="createSale" class="bg-indigo-600 text-white px-3 rounded">ขาย</button>
        </div>
        <p v-if="saleMessage" class="text-green-600 text-sm">{{ saleMessage }}</p>
        <p v-if="saleError" class="text-red-600 text-sm">{{ saleError }}</p>
      </section>

      <section class="bg-white rounded shadow p-4 col-span-1 lg:col-span-1">
        <h2 class="font-semibold mb-3">สรุปรายงาน</h2>
        <div class="grid grid-cols-2 gap-3">
          <div class="bg-gray-50 rounded p-3">
            <div class="text-xs text-gray-500">ยอดขายรวม</div>
            <div class="text-xl font-bold">฿{{ reports.total_sales }}</div>
          </div>
          <div class="bg-gray-50 rounded p-3">
            <div class="text-xs text-gray-500">จำนวนบิล</div>
            <div class="text-xl font-bold">{{ reports.total_transactions }}</div>
          </div>
        </div>
        <div class="mt-4 border-t pt-3 max-h-52 overflow-auto">
          <div v-for="s in stocks" :key="s.name" class="flex justify-between text-sm">
            <span>{{ s.name }}</span>
            <span>คงเหลือ {{ s.stock }}</span>
          </div>
        </div>
      </section>
    </div>
  </div>
  
  <div v-if="loading" class="fixed inset-0 flex items-center justify-center bg-white/60">กำลังโหลด...</div>
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

// sale
const saleForm = ref({ product_id: '', quantity: 1 })
const saleMessage = ref('')
const saleError = ref('')

// reports
const reports = ref({ total_sales: 0, total_transactions: 0 })
const stocks = ref([])

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
    } else {
      const { name, price, stock } = productForm.value
      await $fetch('/products/', { baseURL: API, method: 'POST', body: { name, price, stock } })
    }
    productForm.value = { id: null, name: '', price: 0, stock: 0 }
    await fetchProducts()
  } catch (e) {
    // ignore
  } finally {
    loading.value = false
  }
}

const editProduct = (p) => {
  productForm.value = { id: p.id, name: p.name, price: p.price, stock: p.stock }
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
    const res = await $fetch('/pos/', { baseURL: API, method: 'POST', body: { product_id, quantity } })
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

const logout = () => {
  localStorage.removeItem('is_admin')
  navigateTo('/login')
}

onMounted(async () => {
  await Promise.all([fetchProducts(), fetchReports()])
})
</script>
