<template>
  <div class="min-h-screen flex flex-col items-center justify-center bg-[#fffdf8] px-4">
    <div class="bg-white p-10 rounded-2xl shadow-xl w-full max-w-md space-y-6 border text-center">
      <h2 class="text-3xl font-extrabold text-[#444]">내 프로필</h2>
      <p v-if="nickname" class="text-lg">환영합니다, {{ nickname }}님!</p>
      <p v-else class="text-gray-400">닉네임을 불러오는 중...</p>
      <button @click="logout" class="logout-btn">로그아웃</button>
    </div>
  </div>
</template>

<script setup>
import { useRouter } from 'vue-router'
import Swal from 'sweetalert2'
import { useAuthStore } from '@/stores/auth'  // ✅ authStore import
import { computed } from 'vue'

import axios from 'axios'

const router = useRouter()
const auth = useAuthStore()
const nickname = computed(() => auth.nickname)

const logout = () => {
  auth.logout(Swal, router)
}
</script>


<style scoped>
.logout-btn {
  @apply w-full bg-red-400 text-white font-bold py-3 rounded-lg hover:bg-red-500 transition text-lg;
}

.custom-ok-button-blue {
  background-color: #3b82f6 !important;
  color: white !important;
  font-weight: 600;
  border-radius: 0.375rem;
  padding: 0.5rem 1rem;
  box-shadow: none !important;
}

.custom-ok-button-blue:hover {
  background-color: #2563eb !important;
  transform: scale(1.08);
}
</style>
