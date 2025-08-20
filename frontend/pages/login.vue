<template>
  <div class="flex justify-center items-center min-h-screen bg-gray-100">
    <div class="bg-white p-6 rounded shadow w-80">
      <h1 class="text-xl font-bold mb-4 text-center">POS Admin Login</h1>

      <p class="text-sm text-gray-500 text-center mb-2">กรอกรหัสผ่านเพื่อเข้าสู่หน้าแอดมิน</p>

      <input
        v-model="adminPassword"
        type="password"
        placeholder="Admin Password"
        class="mb-4 p-2 border w-full rounded"
      />

      <button
        @click="loginAdmin"
        class="bg-blue-600 text-white p-2 w-full rounded hover:bg-blue-700"
      >
        เข้าสู่ระบบ
      </button>

      <p v-if="errorMsg" class="text-red-500 text-sm mt-3 text-center">
        {{ errorMsg }}
      </p>
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
    errorMsg.value = 'รหัสผ่านไม่ถูกต้อง'
  }
}
</script>
