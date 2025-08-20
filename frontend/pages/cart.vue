<template>
  <div class="p-4 max-w-3xl mx-auto">
    <h1 class="text-2xl font-bold mb-4">ตะกร้าสินค้า</h1>

    <div v-if="items.length===0" class="bg-white rounded shadow p-6 text-center text-gray-600">
      ยังไม่มีสินค้าในตะกร้า
      <div class="mt-3">
        <NuxtLink to="/menu" class="text-indigo-600">เลือกสินค้า</NuxtLink>
      </div>
    </div>

    <div v-else class="bg-white rounded shadow p-4">
      <div class="overflow-x-auto">
        <table class="w-full text-left">
          <thead>
            <tr class="text-gray-600 text-sm">
              <th class="py-2">สินค้า</th>
              <th class="py-2">ราคา</th>
              <th class="py-2">จำนวน</th>
              <th class="py-2">รวม</th>
              <th></th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="it in items" :key="it.id" class="border-t">
              <td class="py-2 flex items-center gap-3">
                <img v-if="it.image_url" :src="API + it.image_url" class="w-12 h-12 rounded object-cover" />
                <span class="font-medium">{{ it.name }}</span>
              </td>
              <td>฿{{ it.price }}</td>
              <td>
                <input type="number" min="1" v-model.number="it.quantity" class="w-20 border rounded px-2 py-1" />
              </td>
              <td>฿{{ (it.price * it.quantity).toFixed(2) }}</td>
              <td><button class="text-red-600" @click="remove(it.id)">ลบ</button></td>
            </tr>
          </tbody>
        </table>
      </div>

      <div class="mt-4 flex flex-col sm:flex-row gap-3 sm:items-center sm:justify-between">
        <div class="flex items-center gap-2">
          <label class="text-sm text-gray-600">โต๊ะ/ชื่อลูกค้า</label>
          <input v-model="table" placeholder="เช่น โต๊ะ 5" class="border rounded px-2 py-1" />
        </div>
        <div class="text-lg font-bold">รวม: ฿{{ total.toFixed(2) }}</div>
      </div>

      <div class="mt-3 flex justify-end">
        <button @click="checkout" class="bg-green-600 text-white px-4 py-2 rounded">สั่งซื้อ</button>
      </div>
    </div>

    <div v-if="successOpen" class="fixed inset-0 bg-black/40 flex items-center justify-center p-4">
      <div class="bg-white rounded shadow p-6 w-full max-w-sm text-center">
        <div class="text-2xl mb-2">✅</div>
        <div class="font-semibold mb-1">สั่งรายการสำเร็จ</div>
        <div class="text-sm text-gray-600 mb-4">ยอดรวม ฿{{ lastTotal.toFixed(2) }}</div>
        <button @click="successOpen=false" class="bg-indigo-600 text-white px-4 py-2 rounded w-full">ปิด</button>
      </div>
    </div>

    <div v-if="errorOpen" class="fixed inset-0 bg-black/40 flex items-center justify-center p-4">
      <div class="bg-white rounded shadow p-6 w-full max-w-sm text-center">
        <div class="text-2xl mb-2">⚠️</div>
        <div class="font-semibold mb-1">สั่งซื้อไม่สำเร็จ</div>
        <div class="text-sm text-gray-600 mb-4">{{ errorMsg }}</div>
        <button @click="errorOpen=false" class="bg-red-600 text-white px-4 py-2 rounded w-full">ปิด</button>
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
