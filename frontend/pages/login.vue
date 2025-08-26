<template>
  <div class="min-h-screen bg-bakery-gradient flex justify-center items-center p-4">
    <div class="bg-white rounded-2xl shadow-lg border border-amber-200 transition-all duration-300 hover:shadow-xl hover:scale-105 p-8 w-full max-w-md text-center transform transition-all duration-300 hover:scale-105">
      <!-- Header -->
      <div class="mb-8">
        <div class="text-6xl mb-4 animate-float">🍰</div>
        <h1 class="text-3xl font-bold text-transparent bg-clip-text bg-gradient-to-r from-amber-600 to-orange-600 mb-2">
          Sweet Bakery
        </h1>
        <p class="text-amber-700">ระบบจัดการร้านเบเกอรี่</p>
      </div>

      <!-- Login Form -->
      <div class="space-y-6">
        <div>
          <label class="block text-left text-sm font-medium text-amber-700 mb-2">
            รหัสผ่านแอดมิน
          </label>
          <input
            v-model="adminPassword"
            type="password"
            placeholder="กรอกรหัสผ่าน"
            class="w-full px-4 py-3 border border-amber-200 rounded-xl focus:outline-none focus:ring-2 focus:ring-amber-300 focus:border-transparent transition-all duration-200 bg-white/80 backdrop-blur-sm"
            @keyup.enter="loginAdmin"
          />
        </div>

        <button
          @click="loginAdmin"
          class="w-full inline-flex items-center gap-2 px-6 py-3 rounded-full font-medium transition-all duration-300 transform hover:scale-105 hover:shadow-lg bg-gradient-to-r from-amber-400 to-orange-400 text-white shadow-md hover:from-amber-500 hover:to-orange-500 text-lg py-4"
        >
          <span>เข้าสู่ระบบ</span>
          <svg xmlns="http://www.w3.org/2000/svg" class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 16l-4-4m0 0l4-4m-4 4h14m-5 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h7a3 3 0 013 3v1" />
          </svg>
        </button>

        <p v-if="errorMsg" class="text-red-500 text-sm bg-red-50 p-3 rounded-lg border border-red-200">
          {{ errorMsg }}
        </p>
      </div>

      <!-- Decorative elements -->
      <div class="mt-8 flex justify-center gap-2">
        <div class="w-2 h-2 bg-amber-400 rounded-full animate-bounce-soft"></div>
        <div class="w-2 h-2 bg-orange-400 rounded-full animate-bounce-soft" style="animation-delay: 0.2s"></div>
        <div class="w-2 h-2 bg-pink-300 rounded-full animate-bounce-soft" style="animation-delay: 0.4s"></div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()
const adminPassword = ref('')
const errorMsg = ref('')

const EXPECTED_PASSWORD = import.meta.env.VITE_ADMIN_PASSWORD || 'admin123'

onMounted(() => {
  const isAdmin = localStorage.getItem('is_admin') === '1'
  if (isAdmin) router.push('/dashboard')
})

const loginAdmin = () => {
  errorMsg.value = ''
  if (adminPassword.value === EXPECTED_PASSWORD) {
    localStorage.setItem('is_admin', '1')
    router.push('/dashboard')
  } else {
    errorMsg.value = 'รหัสผ่านไม่ถูกต้อง กรุณาลองใหม่'
  }
}
</script>
