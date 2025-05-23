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
          :src="user.profile_image ? `http://localhost:8000${user.profile_image}` : '/default-profile.png'"
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

const route = useRoute()
const users = ref([])
const title = route.meta.title || '팔로우 목록'
const fetchUrl = route.meta.apiUrl

onMounted(async () => {
  try {
    const res = await axios.get(fetchUrl)
    users.value = res.data
  } catch (err) {
    console.error('유저 목록 가져오기 실패:', err)
  }
})
</script>

<style scoped>
</style>
