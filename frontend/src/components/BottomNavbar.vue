<template>
  <nav class="fixed bottom-0 left-0 w-full bg-white border-t flex justify-around py-2 text-sm">
    <!-- 홈 -->
    <div @click="goTo('home')" class="flex flex-col items-center hover:scale-110 hover:bg-gray-100 transition-all cursor-pointer px-3 py-1 rounded-xl">
      <span><img src="/home.png" alt="" class="w-6 h-6" /></span>
      <span>홈</span>
    </div>

    <!-- 피드 -->
    <div @click="goTo('feed')" class="flex flex-col items-center hover:scale-110 hover:bg-gray-100 transition-all cursor-pointer px-3 py-1 rounded-xl">
      <span><img src="/feed.png" alt="" class="w-6 h-6" /></span>
      <span>피드</span>
    </div>

    <!-- 랭킹 -->
    <div @click="goTo('ranking')" class="flex flex-col items-center hover:scale-110 hover:bg-gray-100 transition-all cursor-pointer px-3 py-1 rounded-xl">
      <span><img src="/ranking.png" alt="" class="w-6 h-6" /></span>
      <span>랭킹</span>
    </div>

    <!-- 프로필 -->
    <div @click="goTo('profile')" class="flex flex-col items-center hover:scale-110 hover:bg-gray-100 transition-all cursor-pointer px-3 py-1 rounded-xl">
      <span><img src="/user.png" alt="" class="w-6 h-6" /></span>
      <span>프로필</span>
    </div>
  </nav>
</template>

<script setup>
import { useRouter } from 'vue-router'

const router = useRouter()
const goTo = (name) => {
  router.push({ name })
}
</script>
