<template>
  <div class="p-6 max-w-3xl mx-auto">
    <div class="flex justify-between items-center mb-4">
      <h1 class="text-2xl font-bold">ใบเสร็จ โต๊ะ: {{ table }}</h1>
      <button @click="onPrint()" class="btn">พิมพ์</button>
    </div>

    <div class="card p-4">
      <div v-for="o in orders" :key="o.id" class="border-b last:border-0 py-3">
        <ul class="text-sm text-gray-700">
          <li v-for="it in o.items" :key="it.product_id" class="flex justify-between">
            <span>{{ it.name }} x {{ it.quantity }}</span>
            <span>฿{{ it.subtotal }}</span>
          </li>
        </ul>
        <div class="text-right font-semibold mt-2">ยอดบิล: ฿{{ o.total_price }}</div>
        <div class="text-right mt-2">
          <button @click="remove(o.id)" class="text-red-600 text-sm">ลบ</button>
        </div>
      </div>
      <div class="text-right text-lg font-bold mt-4">รวมทั้งหมด: ฿{{ grandTotal }}</div>
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
</script>
