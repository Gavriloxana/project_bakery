<!-- pages/index.vue -->
<template>
  <div class="min-h-screen bg-bakery-gradient flex items-center justify-center">
    <div class="text-center">
      <div class="text-6xl mb-6 animate-bounce-soft">🍰</div>
      <div class="text-2xl font-bold text-transparent bg-clip-text bg-gradient-to-r from-pink-600 to-rose-600 mb-4">
        Sweet Bakery
      </div>
      <div class="text-gray-600 mb-8">กำลังพาไปหน้า เมนู...</div>
      <div class="flex justify-center gap-2">
        <div class="w-2 h-2 bg-pink-400 rounded-full animate-bounce-soft"></div>
        <div class="w-2 h-2 bg-rose-400 rounded-full animate-bounce-soft" style="animation-delay: 0.2s"></div>
        <div class="w-2 h-2 bg-purple-400 rounded-full animate-bounce-soft" style="animation-delay: 0.4s"></div>
      </div>
    </div>
  </div>
</template>

<script setup>
navigateTo('/menu')
</script>
 