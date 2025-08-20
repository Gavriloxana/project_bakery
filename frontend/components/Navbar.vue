<template>
  <nav class="bg-white border-b shadow-sm sticky top-0 z-40">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      <div class="flex justify-between h-14">
        <div class="flex items-center gap-3">
          <button class="sm:hidden p-2 rounded hover:bg-gray-100" @click="open = !open" aria-label="menu">
            <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor" class="w-6 h-6">
              <path fill-rule="evenodd" d="M3.75 5.25a.75.75 0 01.75-.75h15a.75.75 0 010 1.5h-15a.75.75 0 01-.75-.75zm0 6a.75.75 0 01.75-.75h15a.75.75 0 010 1.5h-15a.75.75 0 01-.75-.75zm0 6a.75.75 0 01.75-.75h15a.75.75 0 010 1.5h-15a.75.75 0 01-.75-.75z" clip-rule="evenodd" />
            </svg>
          </button>
          <NuxtLink to="/menu" class="font-bold text-lg">🍞 Bakery POS</NuxtLink>
        </div>

        <div class="hidden sm:flex items-center gap-6">
          <NuxtLink to="/menu" class="hover:text-indigo-600">เมนู</NuxtLink>
          <NuxtLink to="/dashboard" class="hover:text-indigo-600">แอดมิน</NuxtLink>
          <NuxtLink to="/cart" class="relative hover:text-indigo-600">
            <span>ตะกร้า</span>
            <span v-if="count>0" class="absolute -top-2 -right-3 bg-indigo-600 text-white text-xs rounded-full px-1.5">{{ count }}</span>
          </NuxtLink>
        </div>

        <NuxtLink to="/cart" class="sm:hidden relative flex items-center" aria-label="cart">
          <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-6 h-6">
            <path stroke-linecap="round" stroke-linejoin="round" d="M2.25 3h1.386c.51 0 .955.343 1.087.835l.383 1.437M7.5 14.25h9.75m-9.75 0L6.75 6.75m.75 7.5l-1.5-7.5m0 0h13.5m0 0l1.258 6.286a1.125 1.125 0 01-1.102 1.339H7.5" />
          </svg>
          <span v-if="count>0" class="absolute -top-1 -right-2 bg-indigo-600 text-white text-xs rounded-full px-1">{{ count }}</span>
        </NuxtLink>
      </div>
    </div>

    <div v-if="open" class="sm:hidden border-t bg-white">
      <div class="px-4 py-2 space-y-1">
        <NuxtLink @click="open=false" to="/menu" class="block py-2">เมนู</NuxtLink>
        <NuxtLink @click="open=false" to="/dashboard" class="block py-2">แอดมิน</NuxtLink>
        <NuxtLink @click="open=false" to="/cart" class="block py-2">ตะกร้า ({{ count }})</NuxtLink>
      </div>
    </div>
  </nav>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useCart } from '~/composables/useCart'

const open = ref(false)
const { items } = useCart()
const count = computed(() => items.value.reduce((n,i)=>n+i.quantity,0))
</script>
