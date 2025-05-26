<template>
  <div class="pt-32 pb-24 px-4 max-w-md mx-auto bg-[#fffdf8] min-h-screen">
    <div v-if="feed" class="bg-white shadow rounded-2xl overflow-hidden">
      
      <!-- 📸 이미지 -->
      <img v-if="feed.image" :src="feed.image" class="w-full object-cover max-h-[400px] rounded-t-2xl" />

      <div class="relative p-5">
        <!-- ⋮ 수정/삭제 메뉴 버튼 (본문 우상단으로 이동됨) -->
        <button
          v-if="feed.user.id === userId"
          @click="showMenu = !showMenu"
          class="absolute top-2 right-4 text-gray-500 hover:text-black text-2xl z-10"
        >
          ⋮
        </button>

        <!-- 드롭다운 메뉴 -->
        <div
          v-if="showMenu"
          class="absolute top-8 right-0 bg-white border rounded shadow z-20 w-28 text-sm"
        >
          <button @click="goToEdit" class="block w-full px-4 py-2 hover:bg-gray-100 text-left">✏️ 수정</button>
          <button @click="deleteFeed" class="block w-full px-4 py-2 hover:bg-gray-100 text-left text-red-500">🗑️ 삭제</button>
        </div>

        <p class="text-xs text-gray-400 mb-1">🕒 {{ formatDate(feed.created_at) }}</p>
        <h2 class="text-lg font-bold text-gray-800 mb-2">{{ feed.user.nickname }}님의 피드</h2>
        <p class="whitespace-pre-line text-gray-700 text-sm mb-4">{{ feed.content }}</p>

        <!-- ❤️ 좋아요 & 💬 댓글 수 -->
        <div class="flex items-center gap-6 text-base mb-4 select-none">
          <span @click="toggleLike" class="cursor-pointer hover:scale-105 transition">
            {{ feed.liked ? '❤️' : '🤍' }} {{ feed.like_users_count }}
          </span>
          <span>💬 {{ feed.comments.length }}</span>
        </div>

        <!-- 💬 댓글 리스트 -->
        <div class="space-y-3 mb-6">
          <div v-for="comment in feed.comments" :key="comment.id" class="bg-gray-50 p-3 rounded-xl text-sm shadow-sm">
            <div class="flex justify-between items-start">
              <div>
                <p class="font-semibold text-gray-800">{{ comment.user.nickname }}</p>
                <p class="text-gray-700 mt-1">{{ comment.content }}</p>
              </div>
              <button
                v-if="comment.user.id === userId"
                @click="deleteComment(comment.id)"
                class="text-red-400 hover:text-red-500 text-xs underline underline-offset-2 transition"
              >삭제</button>
            </div>
          </div>
        </div>

        <!-- ✍️ 댓글 작성 -->
        <form @submit.prevent="submitComment" class="flex items-start gap-2">
          <textarea
            v-model="newComment"
            rows="2"
            placeholder="댓글을 입력하세요..."
            class="flex-1 border border-gray-300 rounded-xl p-2 text-sm focus:outline-none focus:ring-2 focus:ring-yellow-200 resize-none shadow-inner"
          ></textarea>
          <button
            type="submit"
            class="bg-yellow-400 hover:bg-yellow-500 text-white font-semibold px-4 py-2 rounded-full shadow transition"
          >
            작성
          </button>
        </form>
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
const showMenu = ref(false)

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
  showMenu.value = false
  const confirmed = await Swal.fire({
    title: '피드를 삭제할까요?',
    icon: 'warning',
    showCancelButton: true,
    confirmButtonText: '삭제',
    cancelButtonText: '취소',
    buttonsStyling: false,
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
        buttonsStyling: false,
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

const goToEdit = () => {
  showMenu.value = false
  router.push({
    name: 'feed-edit',
    params: { id: feed.value.id },
    query: {
      content: feed.value.content,
      image: feed.value.image
    }
  })
}

onMounted(() => {
  fetchFeed()
})
</script>
