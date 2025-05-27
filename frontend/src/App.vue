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
    <template v-if="!auth.isLoading && !auth.isLoggedIn">
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

    <template v-else-if="!auth.isLoading && auth.isLoggedIn">
<button
  @click="logout"
  class="flex items-center gap-2 px-3 py-1.5 text-sm font-medium text-red-600 border border-red-300 bg-red-50 rounded-full shadow-sm hover:bg-red-100 hover:text-red-700 transition"
>
  <svg xmlns="http://www.w3.org/2000/svg" class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a2 2 0 01-2 2H7a2 2 0 01-2-2V7a2 2 0 012-2h4a2 2 0 012 2v1" />
  </svg>
  로그아웃
</button>

    </template>
  </div> 
</nav>


    <!-- 실제 페이지 -->
    <RouterView />
    
  </div>
        <BottomNavbar />
</template>

<script setup>
import { onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import Swal from 'sweetalert2'

const router = useRouter()
const auth = useAuthStore()

onMounted(() => {
  auth.initAuth()  // ✅ 앱 시작 시 모든 상태 세팅
})

// ✅ 반응형 로그인 상태
const isLoggedIn = auth.isLoggedIn

// ✅ 로그아웃 함수
const logout = () => {
  auth.logout(Swal, router)
}
import BottomNavbar from '@/components/BottomNavbar.vue'
import { watchEffect } from 'vue'

watchEffect(() => {
  const _ = auth.isLoggedIn  // 반응성 트리거용
})
</script>


<style>
body {
  margin: 0;
  font-family: 'Segoe UI', 'Pretendard', sans-serif;
}
</style>
