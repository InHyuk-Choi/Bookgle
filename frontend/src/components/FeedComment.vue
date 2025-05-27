<template>
  <div class="px-4 pb-4 space-y-2 text-sm">
    <!-- 💬 댓글 목록 -->
    <div
      v-for="comment in comments"
      :key="comment.id"
      class="flex justify-between items-start bg-gray-50 p-2 rounded"
    >
      <div class="flex gap-2">
        <span class="font-semibold">{{ comment.user.nickname }}</span>
        <span>{{ comment.content }}</span>
      </div>
      <!-- 삭제 버튼 (본인인 경우만 노출) -->
      <button
        v-if="comment.user.id === userId"
        @click="deleteComment(comment.id)"
        class="text-red-400 hover:text-red-500 text-xs underline underline-offset-2"
      >
        삭제
      </button>
    </div>

    <!-- 📝 댓글 입력 -->
    <form @submit.prevent="submitComment" class="flex gap-2 mt-2">
      <input
        v-model="newComment"
        placeholder="댓글 달기..."
        class="flex-1 border rounded-md px-3 py-1 text-sm"
      />
      <button type="submit" class="text-blue-500 font-semibold">게시</button>
    </form>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import axios from 'axios'
import { useAuthStore } from '@/stores/auth'
import Swal from 'sweetalert2'

// props: 댓글 대상 피드 ID
const props = defineProps({
  pheedId: Number
})

const auth = useAuthStore()
const userId = auth.userId
const comments = ref([])
const newComment = ref('')

// 댓글 조회
const fetchComments = async () => {
  try {
    const res = await axios.get(`http://localhost:8000/api/v1/kkubook/pheeds/${props.pheedId}/comments/`, {
      headers: {
        Authorization: `Bearer ${localStorage.getItem('access')}`
      }
    })
    comments.value = res.data
  } catch (err) {
    console.error('댓글 가져오기 실패:', err)
  }
}

// 댓글 작성
const submitComment = async () => {
  if (!newComment.value.trim()) return

  try {
    const res = await axios.post(
      `http://localhost:8000/api/v1/kkubook/pheeds/${props.pheedId}/comments/`,
      { content: newComment.value },
      {
        headers: {
          Authorization: `Bearer ${localStorage.getItem('access')}`
        }
      }
    )
    comments.value.push(res.data)
    newComment.value = ''
  } catch (err) {
    console.error('댓글 작성 실패:', err)
  }
}

// 댓글 삭제
const deleteComment = async (commentId) => {
  const confirmed = await Swal.fire({
    title: '댓글을 삭제할까요?',
    icon: 'warning',
    showCancelButton: true,
    confirmButtonText: '삭제',
    cancelButtonText: '취소',
    customClass: {
      confirmButton: 'bg-red-500 text-white rounded px-3 py-1',
      cancelButton: 'bg-gray-300 text-black rounded px-3 py-1 ml-2',
      popup: 'rounded-xl',
    },
  })

  if (!confirmed.isConfirmed) return

  try {
    await axios.delete(`http://localhost:8000/api/v1/kkubook/comments/${commentId}/`, {
      headers: {
        Authorization: `Bearer ${localStorage.getItem('access')}`
      }
    })
    comments.value = comments.value.filter(comment => comment.id !== commentId)
  } catch (err) {
    console.error('댓글 삭제 실패:', err)
  }
}

// mount
fetchComments()
</script>
