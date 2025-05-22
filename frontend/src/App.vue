<template>
  <div id="app">
<!-- ✨ 상단 네비게이션 바 -->
<nav class="fixed top-0 z-50 w-full flex justify-between items-center px-6 py-2 bg-white/80 backdrop-blur border-b shadow-md">
  <!-- 로고 -->
  <RouterLink to="/" class="hover:opacity-80 transition">
    <img
      src="/favicon.png"
      alt="logo"
      class="w-28 h-20 object-contain"
    />
  </RouterLink>

  <!-- 메뉴 버튼들 -->
  <div class="flex items-center space-x-3">
    <template v-if="!isLoggedIn">
      <RouterLink
        to="/signin"
        class="px-4 py-1.5 text-sm font-medium text-white bg-blue-500 rounded-full shadow hover:bg-blue-600 transition"
      >
        로그인
      </RouterLink>
      <RouterLink
        to="/signup"
        class="px-4 py-1.5 text-sm font-medium text-white bg-green-500 rounded-full shadow hover:bg-green-600 transition"
      >
        회원가입
      </RouterLink>
    </template>

    <template v-else>
      <button
        @click="logout"
        class="px-4 py-1.5 text-sm font-medium text-white bg-red-500 rounded-full shadow hover:bg-red-600 transition"
      >
        로그아웃
      </button>
    </template>
  </div>
</nav>


    <!-- 실제 페이지 -->
    <RouterView />
  </div>
</template>

<script setup>
import { computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'


const router = useRouter()
const auth = useAuthStore()
auth.initAuth()


const isLoggedIn = computed(() => {
  return !!localStorage.getItem('access')
})

// 로그인 상태일 때 유저 상태 불러오기
onMounted(() => {
  if (isLoggedIn.value) {
    auth.initAuth()
    auth.fetchUserStatus()
  }
})

const logout = () => {
  localStorage.removeItem('access')
  localStorage.removeItem('refresh')
  router.push({ name: 'signin' })
}
</script>

<style>
body {
  margin: 0;
  font-family: 'Segoe UI', 'Pretendard', sans-serif;
}
</style>
