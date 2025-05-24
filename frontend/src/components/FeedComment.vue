<template>
  <div class="px-4 pb-4 space-y-2 text-sm">
    <!-- 💬 댓글 목록 -->
    <div v-for="comment in comments" :key="comment.id" class="flex gap-2 items-start">
      <span class="font-semibold">{{ comment.user.nickname }}</span>
      <span>{{ comment.content }}</span>
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

const props = defineProps({
  pheedId: Number
})

const comments = ref([])
const newComment = ref('')

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

fetchComments()
</script>
