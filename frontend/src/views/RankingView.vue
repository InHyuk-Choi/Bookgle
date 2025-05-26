<template>
  <div class="bg-[#fffdf8] min-h-screen px-4 pt-36 pb-10">
    <h2 class="text-3xl font-bold text-center text-yellow-500 mb-6">🏆 랭킹</h2>

    <div v-if="rankings.length" class="space-y-4 max-w-xl mx-auto">
      <div
        v-for="(user, idx) in rankings"
        :key="idx"
        class="flex items-center gap-4 p-4 bg-white shadow rounded-xl border"
        :class="{
          'border-yellow-400 bg-yellow-50': user.rank === 1,
          'border-gray-300 bg-gray-50': user.rank === 2,
          'border-yellow-200 bg-yellow-100': user.rank === 3
        }"
      >
        <!-- 랭크 번호 / 이모지 -->
        <div class="text-2xl font-bold w-8 text-center">
          <span v-if="user.rank === 1">🥇</span>
          <span v-else-if="user.rank === 2">🥈</span>
          <span v-else-if="user.rank === 3">🥉</span>
          <span v-else>{{ user.rank }}</span>
        </div>

        <!-- 프로필 이미지 -->
        <img
  :src="user.profile_image.startsWith('http') ? user.profile_image : `http://localhost:8000${user.profile_image}`"
  alt="프로필"
  class="w-12 h-12 rounded-full object-cover border"
/>

        <!-- 닉네임 + 레벨 + 경험치 -->
        <div class="flex flex-col">
          <p class="font-semibold text-lg">{{ user.nickname }}</p>
          <p class="text-sm text-gray-500">Lv. {{ user.level }} / Exp. {{ user.experience }}</p>
        </div>
      </div>
    </div>

    <p v-else class="text-center text-gray-400">랭킹 정보를 불러오는 중입니다...</p>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'

const rankings = ref([])

onMounted(async () => {
  try {
    const res = await axios.get('http://localhost:8000/api/v1/accounts/ranking/')
    rankings.value = res.data
  } catch (err) {
    console.error('📛 랭킹 불러오기 실패:', err)
  }
})
</script>
