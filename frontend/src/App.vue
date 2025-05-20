<template>
  <div id="app">
    <!-- ✨ 상단 네비게이션 바 -->
    <nav class="sticky top-0 z-50 flex justify-between items-center px-6 py-3 bg-white/80 backdrop-blur border-b shadow-md">
      <!-- 로고 / 메인 링크 -->
      <RouterLink to="/" class="text-xl font-bold text-gray-800 hover:text-yellow-500 transition">
        📚 MyLibrary
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
          <!-- 포인트/유저명 넣고 싶으면 여기에 -->
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
import { computed } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()

const isLoggedIn = computed(() => {
  return !!localStorage.getItem('access')
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
