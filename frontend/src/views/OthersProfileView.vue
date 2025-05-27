<template>
  <div class="bg-[#fffdf8] min-h-screen px-4 pt-36 pb-10">
    <!-- 📌 상단 프로필 -->
    <div class="flex flex-col items-center gap-3 mb-8" v-if="user">
      <img
        :src="getProfileImage(user.profile_image)"
        @error="handleImageError"
        alt="프로필 이미지"
        class="w-28 h-28 rounded-full object-cover border-4 border-yellow-300"
      />
      <h2 class="text-2xl font-bold">{{ user.nickname }}</h2>
      <div class="flex gap-4 text-sm text-gray-500">
        <p>팔로잉 <strong>{{ user.following_count }}</strong></p>
        <p>팔로워 <strong>{{ user.followers_count }}</strong></p>
      </div>
      <button @click="toggleFollow" class="mt-4 px-4 py-2 rounded-lg font-bold text-white transition"
        :class="isFollowing ? 'bg-gray-400 hover:bg-gray-500' : 'bg-yellow-400 hover:bg-yellow-500'">
        {{ isFollowing ? '언팔로우' : '팔로우' }}
      </button>
    </div>

    <!-- 📸 피드 목록 -->
    <div>
      <h3 class="text-lg font-semibold mb-4">{{ user?.nickname }}님의 피드</h3>
      <div v-if="feeds.length" class="grid grid-cols-3 gap-2">
        <div
          v-for="feed in feeds"
          :key="feed.id"
          class="aspect-square bg-gray-100 overflow-hidden rounded-md cursor-pointer hover:opacity-80 transition"
          @click="router.push({ name: 'feed-detail', params: { id: feed.id } })"
        >
          <img v-if="feed.image" :src="feed.image" class="w-full h-full object-cover" />
          <div v-else class="relative w-full h-full">
            <img src="/placeholder-feed.jpg" class="w-full h-full object-cover opacity-40" />
            <div
              class="absolute inset-0 flex items-center justify-center text-center text-sm text-gray-800 font-semibold px-3"
            >
              {{ feed.content.slice(0, 20) }}...
            </div>
          </div>
        </div>
      </div>
      <p v-else class="text-gray-400 text-sm text-center mt-10">작성한 피드가 아직 없어요!</p>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import axios from 'axios'

const route = useRoute()
const router = useRouter()
const username = route.params.username || route.query.username
const fetchUrl = `http://localhost:8000/api/v1/accounts/followers/username/${username}/`

const user = ref(null)
const feeds = ref([])
const isFollowing = ref(false)

const fetchUserInfo = async () => {
  try {
    const res = await axios.get(`http://localhost:8000/api/v1/accounts/username/${username}/`)
    user.value = res.data
    isFollowing.value = res.data.is_following
  } catch (err) {
    console.error('유저 정보 불러오기 실패:', err)
  }
}

const fetchFeeds = async () => {
  try {
    const res = await axios.get(`http://localhost:8000/api/v1/kkubook/pheeds/user/${username}/`)
    console.log('🟡 응답 데이터:', res.data)

    feeds.value = res.data

  } catch (err) {
    console.error('피드 불러오기 실패:', err)
  }
}
const toggleFollow = async () => {
  try {
    const res = await axios.post(
      `http://localhost:8000/api/v1/accounts/follow/${user.value.id}/`,
      {},
      {
        headers: {
          Authorization: `Bearer ${localStorage.getItem('access')}`,
        },
      }
    )
    isFollowing.value = !isFollowing.value
    user.value.followers_count += isFollowing.value ? 1 : -1  // ← 이거 추가!
  } catch (err) {
    console.error('팔로우 실패:', err)
  }
}

const getProfileImage = (url) => {
  if (!url || url === '') return '/default-profile.png'
  return url.startsWith('http') ? url : `http://localhost:8000${url}`
}

const handleImageError = (e) => {
  e.target.src = '/default-profile.png'
}

onMounted(() => {
  fetchUserInfo()
  fetchFeeds()
  
})
</script>
