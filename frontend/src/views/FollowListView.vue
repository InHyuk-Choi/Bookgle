<template>
  <div class="bg-[#fffdf8] min-h-screen px-4 pt-36 pb-10">
    <h2 class="text-2xl font-bold text-center mb-6">{{ title }}</h2>

    <div v-if="users.length" class="space-y-4 max-w-md mx-auto">
      <div
        v-for="user in users"
        :key="user.id"
        class="flex items-center gap-4 p-4 bg-white shadow rounded-xl border"
      >
        <img
  :src="getProfileImage(user)"
  @error="e => e.target.src = '/default-profile.png'"
  alt="프로필 이미지"
  class="w-12 h-12 rounded-full object-cover border"
/>
        <p class="font-semibold text-gray-800">{{ user.nickname }}</p>
      </div>
    </div>
    <p v-else class="text-center text-gray-400 mt-10">아직 표시할 유저가 없어요.</p>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import axios from 'axios'

const users = ref([])
const route = useRoute()

const username = route.params.username
const type = route.meta.type  // 'followers' or 'following'
const title = route.meta.title

const getProfileImage = (user) => {
  const img = user.profile_image
  console.log('🔥 유저 이미지:', user.profile_image)
  if (!img || img === '') {
    return '/default-profile.png'
  }
  return img.startsWith('http') ? img : `http://localhost:8000${img}`
}
const handleImageError = (e) => {
  e.target.src = '/default-profile.png'
}
onMounted(async () => {
  try {
    const res = await axios.get(
      `http://localhost:8000/api/v1/accounts/${type}/username/${username}/`
    )
    users.value = res.data
  } catch (err) {
    console.error('유저 목록 가져오기 실패:', err)
  }
})
</script>
