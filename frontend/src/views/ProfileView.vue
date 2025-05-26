<template>
  <div class="bg-[#fffdf8] min-h-screen px-4 pt-36 pb-10">
    <!-- 📌 상단 프로필 -->
    <div class="flex flex-col items-center gap-3 mb-8">
      <input
  id="profile-upload"
  type="file"
  accept="image/*"
  @change="handleProfileChange"
  class="hidden"
/>

<label for="profile-upload">
 <img
  :src="profileImage"
  @error="handleImageError"
  alt="프로필 이미지"
  class="w-28 h-28 rounded-full object-cover border-4 border-yellow-300 cursor-pointer hover:opacity-80 transition"
  title="클릭하여 프로필 사진 변경"
/>

</label>
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
  class="aspect-square bg-gray-100 overflow-hidden rounded-md cursor-pointer hover:opacity-80 transition"
  @click="router.push({ name: 'feed-detail', params: { id: feed.id } })"
>
          <img
            v-if="feed.image"
            :src="feed.image"
            class="w-full h-full object-cover"
          />
         <div v-else class="relative w-full h-full rounded-md overflow-hidden">
  <img src="/placeholder-feed.jpg" class="w-full h-full object-cover opacity-40" />
  <div class="absolute inset-0 flex items-center justify-center text-center text-sm text-gray-800 font-semibold px-3">
    {{ feed.content.slice(0, 20) }}...
  </div>
</div>
        </div>
      </div>
      <p v-else class="text-gray-400 text-sm text-center mt-10">작성한 피드가 아직 없어요!</p>
    </div>
    <button
  @click="router.push({ name: 'feed-write' })"
  class="fixed bottom-20 right-6 bg-yellow-400 text-white w-14 h-14 rounded-full shadow-lg hover:bg-yellow-500 transition text-2xl flex items-center justify-center z-50"
>
  ✍️
</button>
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
const profileImage = computed(() => {
  const img = auth.profileImage
  if (!img || img === '') {
    return '/default-profile.png'
  }
  if (img.startsWith('http')) {
    return img
  }
  return `http://localhost:8000${img}`
})


const myFeeds = ref([])
const scrollObserver = ref(null)
const username = computed(() => auth.username)

const fetchMyFeeds = async () => {
  try {
    const res = await axios.get('http://localhost:8000/api/v1/kkubook/pheeds/me/', {
      headers: {
        Authorization: `Bearer ${localStorage.getItem('access')}`
      }
    })
    myFeeds.value = res.data
  } catch (err) {
    console.error('내 피드 가져오기 실패:', err)
  }
}

const handleProfileChange = async (e) => {
  const file = e.target.files[0]
  if (!file) return

  const formData = new FormData()
  formData.append('profile_image', file)

  try {
    const res = await axios.post('http://localhost:8000/api/v1/accounts/profile/upload/', formData, {
      headers: {
        Authorization: `Bearer ${localStorage.getItem('access')}`,
        'Content-Type': 'multipart/form-data',
      }
    })

    auth.profileImage = res.data.profile_image

    await Swal.fire({
      icon: 'success',
      title: '프로필 사진이 변경되었습니다!',
      customClass: {
        popup: 'bg-white text-gray-900',
        icon: 'text-green-500',
        confirmButton: 'bg-yellow-400 text-white font-bold rounded px-4 py-2 mt-2 hover:bg-yellow-500'
      }
    })
  } catch (err) {
    console.error('프로필 업로드 실패:', err)
    Swal.fire('실패!', '사진 변경 중 오류가 발생했습니다.', 'error')
  }
}

const goToFollowers = () => {
  router.push({
    name: 'followers',
    params: { username: username.value }  // ✅ 진짜 username!
  })
}

const goToFollowing = () => {
  router.push({
    name: 'following',
    params: { username: username.value }  // ✅ 이것도!
  })
}

const logout = () => {
  auth.logout(Swal, router)
}

onMounted(() => {
  fetchMyFeeds()
  console.log('[내 프로필] auth.profileImage:', auth.profileImage)


})
</script>

<style scoped>
.logout-btn {
  @apply bg-red-400 text-white font-bold py-2 px-6 rounded-lg hover:bg-red-500 transition;
}
</style>
