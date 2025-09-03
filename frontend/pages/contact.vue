<template>
  <div class="min-h-screen bg-gradient-to-br from-amber-50 to-orange-50 py-12">
    <div class="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8">
      <!-- Header Section -->
      <div class="text-center mb-16">
        <h1 class="text-4xl md:text-5xl font-bold text-transparent bg-clip-text bg-gradient-to-r from-amber-600 to-orange-600 mb-4 font-dance">
          🍰 สมาชิกกลุ่ม Sweet Bakery 🍰
        </h1>
        <p class="text-lg text-amber-700 max-w-2xl mx-auto">
          พบกับทีมงานที่ทุ่มเทและมีความเชี่ยวชาญในการสร้างประสบการณ์การสั่งซื้อขนมหวานที่ดีที่สุด
        </p>
      </div>

      <!-- Team Members Grid -->
      <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-8 mb-16">
        <!-- Member 1 -->
        <div class="bg-white/80 backdrop-blur-sm rounded-2xl p-6 shadow-xl hover:shadow-2xl transition-all duration-300 hover:scale-105 border border-amber-200">
          <div class="text-center">
            <div class="w-32 h-32 mx-auto mb-4 rounded-full bg-gradient-to-br from-amber-400 to-orange-400 flex items-center justify-center text-4xl mb-4">
              👨‍💻
            </div>
            <h3 class="text-xl font-bold text-amber-800 mb-2">นายกษิดิ์เดช แพพ่วง</h3>
            <p class="text-amber-600 font-medium mb-3">Tester Developer</p>
            <p class="text-sm text-gray-600 leading-relaxed">
              รับผิดชอบการพัฒนา การเทสตรวจสอบ และการเชื่อมต่อกับ API
            </p>
            <div class="mt-4 flex justify-center space-x-3">
              <span class="px-3 py-1 bg-amber-100 text-amber-700 rounded-full text-xs font-medium">python</span>
              <span class="px-3 py-1 bg-amber-100 text-amber-700 rounded-full text-xs font-medium">unit test</span>
            </div>
          </div>
        </div>

        <!-- Member 2 -->
        <div class="bg-white/80 backdrop-blur-sm rounded-2xl p-6 shadow-xl hover:shadow-2xl transition-all duration-300 hover:scale-105 border border-amber-200">
          <div class="text-center">
            <div class="w-32 h-32 mx-auto mb-4 rounded-full bg-gradient-to-br from-amber-400 to-orange-400 flex items-center justify-center text-4xl mb-4">
              👩‍💻
            </div>
            <h3 class="text-xl font-bold text-amber-800 mb-2">นางสาวธนากร แสงชมภู</h3>
            <p class="text-amber-600 font-medium mb-3">Frontend Developer</p>
            <p class="text-sm text-gray-600 leading-relaxed">
              รับผิดชอบการพัฒนา UI/UX และการเชื่อมต่อกับ API
            </p>
            <div class="mt-4 flex justify-center space-x-3">
              <span class="px-3 py-1 bg-amber-100 text-amber-700 rounded-full text-xs font-medium">Tailwind</span>
              <span class="px-3 py-1 bg-amber-100 text-amber-700 rounded-full text-xs font-medium">Vue.js</span>
            </div>
          </div>
        </div>

        <!-- Member 3 -->
        <div class="bg-white/80 backdrop-blur-sm rounded-2xl p-6 shadow-xl hover:shadow-2xl transition-all duration-300 hover:scale-105 border border-amber-200">
          <div class="text-center">
            <div class="w-32 h-32 mx-auto mb-4 rounded-full bg-gradient-to-br from-amber-400 to-orange-400 flex items-center justify-center text-4xl mb-4">
              👨‍🎨
            </div>
            <h3 class="text-xl font-bold text-amber-800 mb-2">นายปัณณวรรธ ผาบัว</h3>
            <p class="text-amber-600 font-medium mb-3">UI/UX Designer & Full Stack Developer</p>
            <p class="text-sm text-gray-600 leading-relaxed">
              รับผิดชอบการออกแบบและประสบการณ์ผู้ใช้ การพัฒนา Frontend และ Backend
            </p>
            <div class="mt-4 flex justify-center space-x-3">
              <span class="px-3 py-1 bg-amber-100 text-amber-700 rounded-full text-xs font-medium">Figma</span>
              <span class="px-3 py-1 bg-amber-100 text-amber-700 rounded-full text-xs font-medium">Vue.js</span>
              <span class="px-3 py-1 bg-amber-100 text-amber-700 rounded-full text-xs font-medium">Python</span>
            </div>
          </div>
        </div>

        <!-- Member 4 -->
        <div class="bg-white/80 backdrop-blur-sm rounded-2xl p-6 shadow-xl hover:shadow-2xl transition-all duration-300 hover:scale-105 border border-amber-200">
          <div class="text-center">
            <div class="w-32 h-32 mx-auto mb-4 rounded-full bg-gradient-to-br from-amber-400 to-orange-400 flex items-center justify-center text-4xl mb-4">
              👩‍🔬
            </div>
            <h3 class="text-xl font-bold text-amber-800 mb-2">นายพศวีร์ อรุณโน</h3>
            <p class="text-amber-600 font-medium mb-3">Backend Developer & DevOps</p>
            <p class="text-sm text-gray-600 leading-relaxed">
              รับผิดชอบการพัฒนา API และฐานข้อมูล การจัดการเซิร์ฟเวอร์และระบบ
            </p>
            <div class="mt-4 flex justify-center space-x-3">
              <span class="px-3 py-1 bg-amber-100 text-amber-700 rounded-full text-xs font-medium">Python</span>
              <span class="px-3 py-1 bg-amber-100 text-amber-700 rounded-full text-xs font-medium">Docker</span>
              <span class="px-3 py-1 bg-amber-100 text-amber-700 rounded-full text-xs font-medium">Server</span>
            </div>
          </div>
        </div>
      </div>

      <!-- Contact Information -->
      <div class="bg-white/80 backdrop-blur-sm rounded-2xl p-8 shadow-xl border border-amber-200">
        <h2 class="text-3xl font-bold text-center text-amber-800 mb-8 font-dance">
          📞 ข้อมูลติดต่อ
        </h2>
        <div class="text-center">
          <h3 class="text-xl font-semibold text-amber-700 mb-4">📧 อีเมล</h3>
          <div class="space-y-2 max-w-md mx-auto">
            <p class="text-gray-700">
              <span class="font-medium">Kasidet:</span> 67319010016@loeitech.ac.th
            </p>
            <p class="text-gray-700">
              <span class="font-medium">possawee:</span> possawee@gmail.com
            </p>
            <p class="text-gray-700">
              <span class="font-medium">pannawat:</span> pannawatphabua@gmail.com
            </p>
            <p class="text-gray-700">
              <span class="font-medium">Thanagorn:</span> 67319010024@loeitech.ac.th
            </p>
          </div>
        </div>
      </div>

      <!-- Project Description -->
      <div class="mt-12 bg-gradient-to-r from-amber-100 to-orange-100 rounded-2xl p-8 border border-amber-300">
        <h2 class="text-3xl font-bold text-center text-amber-800 mb-6 font-dance">
          🎯 เกี่ยวกับโปรเจค
        </h2>
        <p class="text-lg text-amber-700 text-center leading-relaxed max-w-4xl mx-auto">
          Sweet Bakery เป็นระบบสั่งซื้อขนมหวานออนไลน์ที่พัฒนาด้วยเทคโนโลยีสมัยใหม่ 
          ใช้ Vue.js และ Nuxt.js สำหรับ Frontend และ FastAPI สำหรับ Backend 
          ระบบถูกออกแบบให้ใช้งานง่าย มีความปลอดภัย และรองรับการใช้งานบนอุปกรณ์ทุกขนาด
        </p>
      </div>
    </div>
  </div>
</template>

<script setup>
definePageMeta({
  title: 'Contact - สมาชิกกลุ่ม',
  description: 'พบกับทีมงานที่ทุ่มเทและมีความเชี่ยวชาญในการสร้างประสบการณ์การสั่งซื้อขนมหวานที่ดีที่สุด'
})
</script>

<style scoped>
.animate-bounce-soft {
  animation: bounce-soft 2s infinite;
}

@keyframes bounce-soft {
  0%, 20%, 53%, 80%, 100% {
    transform: translate3d(0, 0, 0);
  }
  40%, 43% {
    transform: translate3d(0, -8px, 0);
  }
  70% {
    transform: translate3d(0, -4px, 0);
  }
  90% {
    transform: translate3d(0, -2px, 0);
  }
}

.font-dance {
  font-family: 'Dancing Script', cursive;
}
</style>
