<template>
  <div class="flex justify-center items-center min-h-screen bg-gray-100">
    <div class="bg-white p-6 rounded shadow w-full max-w-xl">
      <h1 class="text-xl font-bold mb-4 text-center">ตั้งค่าเริ่มต้นผู้ใช้งาน (Admin)</h1>

      <div class="grid grid-cols-1 md:grid-cols-2 gap-3">
        <input v-model="username" placeholder="Username" class="p-2 border rounded" />
        <input v-model="password" type="password" placeholder="Password" class="p-2 border rounded" />
        <select v-model="role" class="p-2 border rounded">
          <option value="admin">admin</option>
          <option value="staff">staff</option>
        </select>
      </div>

      <button @click="createUser" class="bg-green-600 text-white p-2 rounded mt-4 w-full hover:bg-green-700">สร้างผู้ใช้</button>

      <p v-if="message" class="text-green-600 text-center mt-3">{{ message }}</p>
      <p v-if="error" class="text-red-600 text-center mt-3">{{ error }}</p>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'

const config = useRuntimeConfig()
const API = config.public.apiBase

const username = ref('')
const password = ref('')
const role = ref('admin')
const message = ref('')
const error = ref('')

const createUser = async () => {
  message.value = ''
  error.value = ''
  try {
    const res = await $fetch(`/users/`, {
      baseURL: API,
      method: 'POST',
      body: { username: username.value, password: password.value, role: role.value }
    })
    message.value = `สร้างผู้ใช้ ${res.username} เรียบร้อย`
  } catch (e) {
    error.value = e?.data?.detail || 'ไม่สามารถสร้างผู้ใช้ได้'
  }
}
</script>