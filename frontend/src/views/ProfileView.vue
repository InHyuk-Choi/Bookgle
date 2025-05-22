<template>
  <div class="min-h-screen flex flex-col items-center justify-center bg-[#fffdf8] px-4">
    <div class="bg-white p-10 rounded-2xl shadow-xl w-full max-w-md space-y-6 border text-center">
      <h2 class="text-3xl font-extrabold text-[#444]">내 프로필</h2>
      <p class="text-lg">환영합니다, {{ username }}님!</p>
      <button @click="logout" class="logout-btn">로그아웃</button>
    </div>
  </div>
</template>

<script setup>

import { useRouter } from 'vue-router'
import Swal from 'sweetalert2'
import { ref } from 'vue'
import axios from 'axios'  // ✅ 이거 추가 중요!

const router = useRouter()
const username = localStorage.getItem('username') || '유저'

const logout = () => {
  localStorage.removeItem('access')
  localStorage.removeItem('refresh')
  localStorage.removeItem('username')
  delete axios.defaults.headers.common['Authorization']

  Swal.fire({
    icon: 'success',
    title: '로그아웃 완료!',
    text: '다음에 또 만나요 😊',
    confirmButtonText: '확인',
    customClass: {
      confirmButton: 'custom-ok-button-blue',
    }
  }).then(() => {
    // ✅ 강제 새로고침으로 상태 완전 초기화
    window.location.href = '/signin'
  })
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
