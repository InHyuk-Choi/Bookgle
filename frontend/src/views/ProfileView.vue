<template>
  <div class="bg-[#fffdf8] min-h-screen px-4 pt-36 pb-10">
    <!-- 📌 상단 프로필 -->
    <div class="flex flex-col items-center gap-3 mb-8">
      <img
        :src="profileImage"
        alt="프로필 이미지"
        class="w-28 h-28 rounded-full object-cover border-4 border-yellow-300"
      />
      <h2 class="text-2xl font-bold">{{ nickname }}</h2>
      <div class="flex gap-6 text-sm text-gray-700">
        <p><strong>{{ totalPoints }}</strong> 포인트</p>
        <p><strong>{{ readPages }}</strong> 페이지</p>
      </div>
<div class="flex gap-4 text-sm text-gray-500">
  <p class="cursor-pointer hover:underline" @click="goToFollowing">
    팔로잉 <strong>{{ followingCount }}</strong>
  </p>
  <p class="cursor-pointer hover:underline" @click="goToFollowers">
    팔로워 <strong>{{ followersCount }}</strong>
  </p>
</div>
      <button @click="logout" class="logout-btn mt-4">로그아웃</button>
    </div>

    <!-- 📸 내 피드 목록 -->
    <div>
      <h3 class="text-lg font-semibold mb-4">📷 내가 쓴 피드</h3>
      <div v-if="myFeeds.length" class="grid grid-cols-3 gap-2">
        <div
          v-for="feed in myFeeds"
          :key="feed.id"
          class="aspect-square bg-gray-100 overflow-hidden rounded-md"
        >
          <img
            v-if="feed.image"
            :src="feed.image"
            class="w-full h-full object-cover"
          />
          <div v-else class="flex items-center justify-center h-full text-sm text-gray-500 px-2 text-center">
            {{ feed.content.slice(0, 20) }}...
          </div>
        </div>
      </div>
      <p v-else class="text-gray-400 text-sm text-center mt-10">작성한 피드가 아직 없어요!</p>
    </div>

    <!-- 🔁 무한 스크롤 감지용 -->
    <div ref="scrollObserver" class="h-4"></div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import Swal from 'sweetalert2'
import axios from 'axios'
import { useAuthStore } from '@/stores/auth'

const auth = useAuthStore()
const router = useRouter()

const nickname = computed(() => auth.nickname)
const totalPoints = computed(() => auth.totalPoints)
const readPages = computed(() => auth.readPages)
const followingCount = computed(() => auth.followingCount)
const followersCount = computed(() => auth.followersCount)
const profileImage = computed(() =>
  auth.profileImage ? `http://localhost:8000${auth.profileImage}` : '/default-profile.png'
)

const myFeeds = ref([])
const scrollObserver = ref(null)

const fetchMyFeeds = async () => {
  try {
    const res = await axios.get('http://localhost:8000/api/v1/feeds/me/')
    myFeeds.value = res.data
  } catch (err) {
    console.error('내 피드 가져오기 실패:', err)
  }
}

const goToFollowing = () => {
  router.push({ name: 'following-list', params: { userId: auth.userId } })
}
const goToFollowers = () => {
  router.push({ name: 'follower-list', params: { userId: auth.userId } })
}

const logout = () => {
  auth.logout(Swal, router)
}

onMounted(() => {
  fetchMyFeeds()
})
</script>

<style scoped>
.logout-btn {
  @apply bg-red-400 text-white font-bold py-2 px-6 rounded-lg hover:bg-red-500 transition;
}
</style>
