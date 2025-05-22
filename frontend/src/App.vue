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
import axios from 'axios'
import Swal from 'sweetalert2'



const router = useRouter()
const auth = useAuthStore()

// ✅ 반응형 로그인 상태
const isLoggedIn = computed(() => auth.isAuthenticated)

onMounted(() => {
  auth.initAuth()
  auth.fetchUserStatus()
})

// ✅ auth의 logout 사용
const logout = () => {
  auth.logout(Swal, router)
}
</script>

<style>
body {
  margin: 0;
  font-family: 'Segoe UI', 'Pretendard', sans-serif;
}
</style>
