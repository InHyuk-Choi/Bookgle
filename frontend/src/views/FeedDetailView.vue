<template>
  <div class="pt-32 pb-24 px-4 max-w-md mx-auto bg-[#fffdf8] min-h-screen">
    <div v-if="feed" class="bg-white shadow rounded-xl overflow-hidden">
      <img v-if="feed.image" :src="feed.image" class="w-full object-cover max-h-[400px]" />

      <div class="p-4">
        <p class="text-sm text-gray-500 mb-1">🕒 {{ formatDate(feed.created_at) }}</p>
        <h2 class="text-xl font-bold mb-3">{{ feed.user.nickname }}님의 피드</h2>
        <p class="whitespace-pre-line text-gray-800 mb-4">{{ feed.content }}</p>

        <!-- ❤️ 좋아요 & 💬 댓글 수 -->
        <div class="flex items-center gap-6 text-lg mb-4">
          <span @click="toggleLike" class="cursor-pointer">
            {{ feed.liked ? '❤️' : '🤍' }} {{ feed.like_users_count }}
          </span>
          <span>💬 {{ feed.comments.length }}</span>
        </div>

        <!-- 💬 댓글 리스트 -->
        <div class="space-y-3">
          <div v-for="comment in feed.comments" :key="comment.id" class="bg-gray-50 p-3 rounded-md text-sm">
            <div class="flex justify-between items-start">
              <div>
                <p class="font-semibold text-gray-700">{{ comment.user.nickname }}</p>
                <p class="text-gray-800 mt-1">{{ comment.content }}</p>
              </div>
              <button v-if="comment.user.id === userId" @click="deleteComment(comment.id)" class="text-red-400 text-xs hover:underline">삭제</button>
            </div>
          </div>
        </div>

        <!-- ✍️ 댓글 작성 -->
        <form @submit.prevent="submitComment" class="mt-6 flex items-start gap-2">
          <textarea v-model="newComment" rows="2" placeholder="댓글을 입력하세요..."
                    class="flex-1 border border-gray-300 rounded-md p-2 text-sm focus:outline-none focus:ring focus:ring-yellow-200"></textarea>
          <button type="submit"
                  class="bg-yellow-400 hover:bg-yellow-500 text-white font-bold px-4 py-2 rounded-md transition">작성
          </button>
        </form>

        <!-- 🗑️ 피드 삭제 버튼 -->
        <button v-if="feed.user.id === userId" @click="deleteFeed"
                class="mt-6 w-full bg-red-400 hover:bg-red-500 text-white font-bold py-2 rounded-md transition">
          피드 삭제하기
        </button>

      </div>
    </div>

    <div v-else class="text-center text-gray-400 mt-20">피드를 불러오는 중입니다...</div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import axios from 'axios'
import { useAuthStore } from '@/stores/auth'
import Swal from 'sweetalert2'

const auth = useAuthStore()
const userId = auth.userId

const route = useRoute()
const router = useRouter()
const feed = ref(null)
const newComment = ref('')

const fetchFeed = async () => {
  try {
    const res = await axios.get(`http://localhost:8000/api/v1/kkubook/pheeds/${route.params.id}/`, {
      headers: {
        Authorization: `Bearer ${localStorage.getItem('access')}`
      }
    })
    feed.value = {
      ...res.data,
      liked: res.data.is_liked
    }
  } catch (err) {
    console.error('피드 상세 불러오기 실패:', err)
  }
}

const formatDate = (dateStr) => new Date(dateStr).toLocaleString()

const toggleLike = async () => {
  try {
    const res = await axios.post(
      `http://localhost:8000/api/v1/kkubook/pheeds/${feed.value.id}/like/`,
      {},
      {
        headers: {
          Authorization: `Bearer ${localStorage.getItem('access')}`,
        },
      }
    )
    feed.value.liked = res.data.liked
    feed.value.like_users_count = res.data.like_count
  } catch (err) {
    console.error('좋아요 실패:', err)
  }
}

const submitComment = async () => {
  if (!newComment.value.trim()) return

  try {
    const res = await axios.post(
      `http://localhost:8000/api/v1/kkubook/pheeds/${feed.value.id}/comments/`,
      { content: newComment.value },
      {
        headers: {
          Authorization: `Bearer ${localStorage.getItem('access')}`,
        },
      }
    )
    feed.value.comments.push(res.data)
    newComment.value = ''
  } catch (err) {
    console.error('댓글 작성 실패:', err)
  }
}

const deleteComment = async (commentId) => {
  try {
    await axios.delete(`http://localhost:8000/api/v1/kkubook/comments/${commentId}/`, {
      headers: {
        Authorization: `Bearer ${localStorage.getItem('access')}`
      }
    })
    feed.value.comments = feed.value.comments.filter(c => c.id !== commentId)
  } catch (err) {
    console.error('댓글 삭제 실패:', err)
  }
}

const deleteFeed = async () => {
  const confirmed = await Swal.fire({
  title: '피드를 삭제할까요?',
  icon: 'warning',
  showCancelButton: true,
  confirmButtonText: '삭제',
  cancelButtonText: '취소',
  buttonsStyling: false, // ✅ 기본 스타일 제거
  customClass: {
    confirmButton: 'bg-red-500 hover:bg-red-600 text-white font-bold py-2 px-4 rounded',
    cancelButton: 'bg-gray-400 hover:bg-gray-500 text-white font-bold py-2 px-4 rounded ml-2',
    popup: 'rounded-xl'
  }
})



  if (confirmed.isConfirmed) {
    try {
      await axios.delete(`http://localhost:8000/api/v1/kkubook/pheeds/${feed.value.id}/`, {
        headers: {
          Authorization: `Bearer ${localStorage.getItem('access')}`
        }
      })
      await Swal.fire({
  title: '삭제 완료!',
  icon: 'success',
  confirmButtonText: '확인',
  buttonsStyling: false, // ✅ 필수!
  customClass: {
    confirmButton: 'bg-yellow-400 hover:bg-yellow-500 text-white font-bold py-2 px-4 rounded',
    popup: 'rounded-xl'
  }
})

      router.push({ name: 'profile' })
    } catch (err) {
      console.error('피드 삭제 실패:', err)
    }
  }
}

onMounted(() => {
  fetchFeed()
})
</script>