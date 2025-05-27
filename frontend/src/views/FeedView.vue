<!-- src/views/FeedView.vue -->
<template>
  <div class="pt-36 pb-20 bg-[#fffdf8] min-h-screen">
    <div v-if="isLoading" class="text-center text-gray-400 py-6">불러오는 중...</div>

    <div class="max-w-lg mx-auto px-4">
    
      <!-- 📋 피드 카드 리스트 -->
      <div v-for="feed in feeds" :key="feed.id" class="bg-white rounded-xl shadow mb-6 overflow-hidden">
        <!-- 🧑 유저 정보 -->

<div class="flex items-center p-4 border-b">
  <RouterLink
    :to="{ name: 'UserProfile', params: { username: feed.user.username } }"
    class="flex items-center hover:bg-gray-50 transition"
  >
    <img
      :src="getProfileImage(feed.user)"
      class="w-10 h-10 rounded-full mr-3 object-cover"
    />
    <div>
      <p class="font-semibold text-sm">{{ feed.user.nickname }}</p>
      <p class="text-xs text-gray-400">{{ formatDate(feed.created_at) }}</p>
    </div>
  </RouterLink>

        </div>
        <!-- ✨ 이미지 or 내용 -->
        <div v-if="feed.image" class="w-full">
          <img :src="feed.image" class="w-full max-h-[300px] object-cover" />
        </div>
        <div class="p-4 text-sm whitespace-pre-line">{{ feed.content }}</div>
 
        <!-- ❤️ 액션바 -->      
        <!-- ❤️ 액션바 -->
<div class="px-4 pb-2 flex items-center gap-4 text-lg">
  <span @click="toggleLike(feed)" class="cursor-pointer">
    {{ feed.liked ? '❤️' : '🤍' }} {{ feed.like_users_count }}
  </span>
  <span @click="toggleComments(feed.id)" class="cursor-pointer">
    💬 {{ feed.comments_count }}
  </span>
</div>

<!-- 💬 댓글 컴포넌트 표시 -->
<FeedComment v-if="openComments[feed.id]" :pheedId="feed.id" />


      </div>
        <div v-if="feeds.length === 0" class="text-center text-gray-500 mt-12">
        아직 피드가 없어요 😢
        </div>
        <!-- ✍️ 피드 작성 플로팅 버튼 -->
<button
  @click="router.push({ name: 'feed-write' })"
  class="fixed bottom-20 right-6 bg-yellow-400 text-white w-14 h-14 rounded-full shadow-lg hover:bg-yellow-500 transition text-2xl flex items-center justify-center z-50"
>
  ✍️
</button>

    </div>
  </div>
</template>



<script setup>
import { ref, onMounted, onBeforeUnmount } from 'vue'
import axios from 'axios'
import { useAuthStore } from '@/stores/auth'
import { useRouter } from 'vue-router'
import FeedComment from '@/components/FeedComment.vue'
const openComments = ref({})
const router = useRouter()
const auth = useAuthStore()
const feeds = ref([])
const page = ref(1)
const hasNext = ref(true)
const isLoading = ref(false)


const toggleComments = (pheedId) => {
  openComments.value[pheedId] = !openComments.value[pheedId]
}
const toggleLike = async (feed) => {
  try {
    const res = await axios.post(
      `http://localhost:8000/api/v1/kkubook/pheeds/${feed.id}/like/`,
      {},
      {
        headers: {
          Authorization: `Bearer ${localStorage.getItem('access')}`,
        },
      }
    )

    // 좋아요 상태/수 반영
    feed.liked = res.data.liked
    feed.like_users_count = res.data.like_count
  } catch (err) {
    console.error('좋아요 토글 실패:', err)
  }
}

const fetchFeeds = async () => {
  if (isLoading.value || !hasNext.value) return
  isLoading.value = true
  try {
    const res = await axios.get(`http://localhost:8000/api/v1/kkubook/pheeds/?page=${page.value}`, {
      headers: {
        Authorization: `Bearer ${localStorage.getItem('access')}`,
      },
    })

    const results = res.data.results || res.data  // paginator 지원 시
    feeds.value.push(...results.map(feed => ({
      ...feed,
      liked: feed.is_liked,
    })))

    if (res.data.next) {
      page.value++
    } else {
      hasNext.value = false
    }
  } catch (err) {
    console.error('피드 가져오기 실패:', err)
  } finally {
    isLoading.value = false
  }
}


const getProfileImage = (user) => {
  const img = user.profile_image
  if (!img || img === '') {
    return '/default-profile.png'
  }
  return img.startsWith('http') ? img : `http://localhost:8000${img}`
}

const handleScroll = () => {
  const scrollBottom = window.innerHeight + window.scrollY
  const docHeight = document.body.offsetHeight
  if (scrollBottom >= docHeight - 300) {
    fetchFeeds()
  }
}

onMounted(() => {
  fetchFeeds()
  window.addEventListener('scroll', handleScroll)
})

onBeforeUnmount(() => {
  window.removeEventListener('scroll', handleScroll)
})

const formatDate = (dateStr) => {
  return new Date(dateStr).toLocaleString()
}



onMounted(() => {
  fetchFeeds()
})
</script>

