<template>
  <div class="min-h-screen flex items-center justify-center bg-[#fffdf8] px-4">
    <div class="bg-white p-12 rounded-2xl shadow-xl w-full max-w-lg space-y-8 border">
      <h2 class="text-3xl font-extrabold text-center text-[#444]">로그인</h2>

      <form @submit.prevent="login" class="space-y-6">
        <input v-model="username" placeholder="아이디" class="input" />
        <input v-model="password" type="password" placeholder="비밀번호" class="input" />
        <button type="submit" class="submit-btn">로그인</button>
      </form>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import axios from 'axios'
import Swal from 'sweetalert2'

const username = ref('')
const password = ref('')
const router = useRouter()

const login = async () => {
  try {
    const res = await axios.post('http://localhost:8000/api/v1/accounts/token/', {
      username: username.value,
      password: password.value,
    })

    localStorage.setItem('access', res.data.access)
    localStorage.setItem('refresh', res.data.refresh)
    axios.defaults.headers.common['Authorization'] = `Bearer ${res.data.access}`

    Swal.fire({
      icon: 'success',
      title: '로그인 성공!',
      text: '환영합니다!',
      confirmButtonText: '확인',
      customClass: {
        confirmButton: 'custom-ok-button-blue'
      }
    }).then(() => router.push({ name: 'home' }))
  } catch (err) {
    Swal.fire({
      icon: 'error',
      title: '로그인 실패!',
      text: '아이디 또는 비밀번호를 확인해주세요.',
      confirmButtonText: '확인',
      customClass: {
        confirmButton: 'custom-ok-button-red'
      }
    })
  }
}
</script>

<style>
.custom-ok-button-blue {
  opacity: 1 !important;
  background-color: #3b82f6 !important;
  color: white !important;
  font-weight: 600;
  border-radius: 0.375rem;
  padding: 0.5rem 1rem;
  transition: all 0.2s ease-in-out;
  box-shadow: none !important;
}

.custom-ok-button-blue:hover {
  transform: scale(1.08);
  background-color: #2563eb !important;
}

.custom-ok-button-red {
  opacity: 1 !important;
  background-color: #ef4444 !important;
  color: white !important;
  font-weight: 600;
  border-radius: 0.375rem;
  padding: 0.5rem 1rem;
  transition: all 0.2s ease-in-out;
  box-shadow: none !important;
}

.custom-ok-button-red:hover {
  transform: scale(1.08);
  background-color: #dc2626 !important;
}

.input {
  @apply w-full border rounded-lg p-4 text-base focus:outline-none focus:ring focus:ring-yellow-300;
}

.submit-btn {
  @apply w-full bg-yellow-400 text-white font-bold py-3 rounded-lg hover:bg-yellow-500 transition text-lg;
}
</style>
