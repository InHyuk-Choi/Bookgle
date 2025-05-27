<template>
  <div class="min-h-screen flex items-center justify-center bg-[#fffdf8] px-4">
    <div class="bg-white p-12 rounded-2xl shadow-xl w-full max-w-md space-y-8 border">
      <h2 class="text-3xl font-extrabold text-center text-[#444]">로그인</h2>

      <form @submit.prevent="login" class="space-y-5">
        <input v-model="auth.username" placeholder="아이디" class="input" />
        <input v-model="auth.password1" type="password" placeholder="비밀번호" class="input" />
        <button type="submit" class="submit-btn">로그인</button>
      </form>

      <!-- 👇 소셜 로그인 섹션 -->
      <div class="pt-6 space-y-3">
        <p class="text-center text-gray-500 font-medium">소셜 계정으로 로그인</p>

        <!-- 카카오 버튼 -->
        <div class="flex justify-center">
          <img
            src="/kakao-logo.png"
            alt="카카오 로그인"
            @click="kakaoLogin"
            class="h-11 w-auto cursor-pointer hover:scale-105 transition duration-200 shadow"
          />
        </div>

        <!-- 구글 공식 버튼 -->
        <div id="g_id_signin" class="flex justify-center"></div>
      </div>
    </div>
  </div>
</template>


<script setup>
import { useRouter } from 'vue-router'
import Swal from 'sweetalert2'
import { useAuthStore } from '@/stores/auth'
import axios from 'axios'
import { onMounted } from 'vue'

const auth = useAuthStore()
const router = useRouter()
const login = () => auth.login(router, Swal)

onMounted(() => {
  // ✅ 구글 공식 버튼 초기화 및 렌더링
  if (window.google?.accounts?.id) {
    window.google.accounts.id.initialize({
  client_id: '195750984105-9l4lr0mnr53s171bi0gnohvrc7rdjrea.apps.googleusercontent.com',
  callback: handleGoogleLogin,
})

window.google.accounts.id.renderButton(
  document.getElementById('g_id_signin'),
  {
    theme: 'outline',
    size: 'large',
    shape: 'rectangular', // 또는 'pill' 사용 가능
    logo_alignment: 'center'
  }
)
  }
})

const handleGoogleLogin = async (response) => {
  const idToken = response.credential
  try {
    const res = await axios.post('http://localhost:8000/api/v1/accounts/google/login/', {
      access_token: idToken,
    }, { withCredentials: true })

    localStorage.setItem('access', res.data.access)
    axios.defaults.headers.common['Authorization'] = `Bearer ${res.data.access}`

    await auth.fetchUserStatus()
    await auth.fetchBookwormStatus()
    await auth.initAuth()

    Swal.fire({
      icon: 'success',
      title: 'Google 로그인 성공!',
      showConfirmButton: false,
      timer: 1200,
    })

    router.push({ name: 'home' })
  } catch (err) {
    Swal.fire({
      icon: 'error',
      title: 'Google 로그인 실패',
      text: err.response?.data?.error || '서버 에러',
    })
  }
}

// ✅ 카카오 로그인
const kakaoLogin = () => {
  if (typeof window !== 'undefined' && window.Kakao) {
    if (!window.Kakao.isInitialized()) {
      window.Kakao.init('547f004d7a2abd7be2d61a8504d6b439')
    }

    window.Kakao.Auth.login({
      scope: 'profile_nickname,profile_image',
      success: async function (authObj) {
        const accessToken = authObj.access_token
        await auth.kakaoLogin(router, Swal, accessToken)
        await auth.initAuth()
      },
      fail: function (err) {
        Swal.fire({
          icon: 'error',
          title: '카카오 로그인 실패',
          text: JSON.stringify(err),
        })
      }
    })
  }
}
</script>

<style>
.input {
  @apply w-full border rounded-lg p-4 text-base focus:outline-none focus:ring focus:ring-yellow-300;
}
.submit-btn {
  @apply w-full bg-yellow-400 text-white font-bold py-3 rounded-lg hover:bg-yellow-500 transition text-lg;
}
.social-btn {
  @apply w-full flex items-center justify-center gap-2 font-semibold rounded-lg py-3 px-4 shadow border;
}
</style>
