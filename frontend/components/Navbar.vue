<template>
  <nav class="bg-white/90 backdrop-blur-md border-b border-amber-200 shadow-lg sticky top-0 z-40 transition-all duration-300">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      <div class="flex justify-between h-16">
        <div class="flex items-center gap-3">
          <button 
            class="sm:hidden p-2 rounded-full hover:bg-amber-100 transition-colors duration-200" 
            @click="open = !open" 
            aria-label="menu"
          >
            <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor" class="w-6 h-6 text-amber-700">
              <path fill-rule="evenodd" d="M3.75 5.25a.75.75 0 01.75-.75h15a.75.75 0 010 1.5h-15a.75.75 0 01-.75-.75zm0 6a.75.75 0 01.75-.75h15a.75.75 0 010 1.5h-15a.75.75 0 01-.75-.75zm0 6a.75.75 0 01.75-.75h15a.75.75 0 010 1.5h-15a.75.75 0 01-.75-.75z" clip-rule="evenodd" />
            </svg>
          </button>
          <NuxtLink 
            to="/menu" 
            class="font-bold text-xl text-transparent bg-clip-text bg-gradient-to-r from-amber-600 to-orange-600 hover:from-amber-700 hover:to-orange-700 transition-all duration-300 flex items-center gap-2"
          >
            <span class="text-2xl">🍰</span>
            <span class="font-dance">Sweet Bakery</span>
          </NuxtLink>
        </div>

        <div class="hidden sm:flex items-center gap-6">
          <NuxtLink 
            to="/menu" 
            class="text-amber-800 hover:text-amber-600 font-medium px-4 py-2 rounded-full hover:bg-amber-50 transition-all duration-300 hover:scale-105"
          >
            เมนู
          </NuxtLink>
          <NuxtLink 
            to="/contact" 
            class="text-amber-800 hover:text-amber-600 font-medium px-4 py-2 rounded-full hover:bg-amber-50 transition-all duration-300 hover:scale-105"
          >
            ติดต่อ
          </NuxtLink>
          <NuxtLink 
            to="/cart" 
            class="relative text-amber-800 hover:text-amber-600 font-medium px-4 py-2 rounded-full hover:bg-amber-50 transition-all duration-300 hover:scale-105"
          >
            <span>ตะกร้า</span>
            <span 
              v-if="count > 0" 
              class="absolute -top-2 -right-3 bg-gradient-to-r from-amber-500 to-orange-500 text-white text-xs rounded-full px-2 py-1 font-bold shadow-lg animate-bounce-soft"
            >
              {{ count }}
            </span>
          </NuxtLink>
        </div>

        <NuxtLink 
          to="/cart" 
          class="sm:hidden relative flex items-center p-2 rounded-full hover:bg-amber-100 transition-colors duration-200" 
          aria-label="cart"
        >
          <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-6 h-6 text-amber-700">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M2.25 3h1.386c.51 0 .955.343 1.087.835l.383 1.437M7.5 14.25h9.75m-9.75 0L6.75 6.75m.75 7.5l-1.5-7.5m0 0h13.5m0 0l1.258 6.286a1.125 1.125 0 01-1.102 1.339H7.5" />
          </svg>
          <span 
            v-if="count > 0" 
            class="absolute -top-1 -right-2 bg-gradient-to-r from-amber-500 to-orange-500 text-white text-xs rounded-full px-1.5 py-0.5 font-bold shadow-lg animate-bounce-soft"
          >
            {{ count }}
          </span>
        </NuxtLink>
      </div>
    </div>

    <div 
      v-if="open" 
      class="sm:hidden border-t border-amber-200 bg-white/95 backdrop-blur-md transition-all duration-300"
    >
      <div class="px-4 py-3 space-y-2">
        <NuxtLink 
          @click="open=false" 
          to="/menu" 
          class="block py-2 px-3 rounded-lg hover:bg-amber-50 hover:text-amber-600 transition-colors duration-200"
        >
          เมนู
        </NuxtLink>
        <NuxtLink 
          @click="open=false" 
          to="/contact" 
          class="block py-2 px-3 rounded-lg hover:bg-amber-50 hover:text-amber-600 transition-colors duration-200"
        >
          ติดต่อ
        </NuxtLink>
        <NuxtLink 
          @click="open=false" 
          to="/cart" 
          class="block py-2 px-3 rounded-lg hover:bg-amber-50 hover:text-amber-600 transition-colors duration-200"
        >
          ตะกร้า ({{ count }})
        </NuxtLink>
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
