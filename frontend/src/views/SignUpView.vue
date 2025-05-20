<template>
  <div class="min-h-screen flex items-center justify-center bg-[#fffdf8] px-4">
    <div class="bg-white shadow-lg p-12 rounded-2xl w-full max-w-lg space-y-8 border">
      <h2 class="text-3xl font-extrabold text-center text-[#444]">회원가입</h2>

      <form @submit.prevent="signup" class="space-y-5">
        <input v-model="username" placeholder="아이디" class="input" />
        <input v-model="nickname" placeholder="닉네임" class="input" />
        <input v-model="password" type="password" placeholder="비밀번호" class="input" />
        <input v-model="password2" type="password" placeholder="비밀번호 확인" class="input" />
        <button type="submit" class="submit-btn">회원가입</button>
      </form>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import axios from 'axios'
import { useRouter } from 'vue-router'
import Swal from 'sweetalert2'

const username = ref('')
const password = ref('')
const password2 = ref('')
const nickname = ref('')
const router = useRouter()

const signup = async () => {
  if (!nickname.value.trim()) {
    return Swal.fire({
      icon: 'error',
      title: '닉네임 필수!',
      text: '닉네임을 입력해주세요.',
      confirmButtonText: '확인',
      customClass: {
        confirmButton: 'custom-ok-button-red',
      }
    })
  }

  if (password.value !== password2.value) {
    return Swal.fire({
      icon: 'error',
      title: '비밀번호 불일치!',
      text: '비밀번호가 서로 다릅니다.',
      confirmButtonText: '확인',
      customClass: {
        confirmButton: 'custom-ok-button-red',
      }
    })
  }

  try {
    await axios.post('http://localhost:8000/api/v1/accounts/register/', {
      username: username.value,
      email: `${username.value}@kkubook.com`,
      password: password.value,
      password2: password2.value,
      nickname: nickname.value,
    })

    const res = await axios.post('http://localhost:8000/api/v1/accounts/token/', {
      username: username.value,
      password: password.value,
    })

    localStorage.setItem('access', res.data.access)
    localStorage.setItem('refresh', res.data.refresh)
    axios.defaults.headers.common['Authorization'] = `Bearer ${res.data.access}`

    Swal.fire({
      icon: 'success',
      title: '회원가입 성공!',
      text: '환영합니다!',
      confirmButtonText: '확인',
      customClass: {
        confirmButton: 'custom-ok-button-blue'
      }
    }).then(() => router.push({ name: 'home' }))

  } catch (err) {
    Swal.fire({
      icon: 'error',
      title: '에러!',
      text: err.response?.data?.nickname?.[0] ||
            err.response?.data?.username?.[0] ||
            err.response?.data?.non_field_errors?.[0] ||
            '회원가입에 실패했습니다.',
      confirmButtonText: '확인',
      customClass: {
        confirmButton: 'custom-ok-button-red'
      }
    })
  }
}
</script>

<style>
body {
  margin: 0;
  font-family: 'Arial', sans-serif;
}

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
