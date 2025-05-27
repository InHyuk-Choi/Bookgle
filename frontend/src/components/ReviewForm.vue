<template>
  <div class="bg-[#fffce8] border border-yellow-300 p-6 rounded-xl shadow">
    <h3 class="text-lg font-semibold text-gray-700 mb-4">✏️ 리뷰 작성하기</h3>

    <textarea
      v-model="content"
      rows="4"
      placeholder="책에 대한 느낌이나 추천 이유를 적어보세요 :)"
      class="w-full border rounded-lg px-4 py-2 text-sm focus:ring-2 focus:ring-yellow-400 focus:outline-none"
    ></textarea>

    <div class="mt-4 flex items-center gap-3">
      <label class="text-sm text-gray-700">⭐ 별점:</label>
      <select
        v-model="rating"
        class="border rounded px-2 py-1 text-sm focus:ring-2 focus:ring-yellow-400 focus:outline-none"
      >
        <option value="">선택</option>
        <option v-for="n in 5" :key="n" :value="n">{{ n }}점</option>
      </select>

      <button
        @click="submitReview"
        class="ml-auto bg-yellow-400 hover:bg-yellow-500 text-white px-4 py-2 rounded-lg shadow text-sm"
      >
        리뷰 작성
      </button>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import Swal from 'sweetalert2'
import axios from 'axios'

const props = defineProps({
  isbn: String,
})
const emit = defineEmits(['refresh'])

const content = ref('')
const rating = ref('')

const submitReview = async () => {
  if (!content.value.trim() || !rating.value) {
    return Swal.fire('입력 오류', '내용과 별점을 모두 입력해주세요', 'warning')
  }

  try {
    await axios.post(`http://localhost:8000/api/v1/kkubook/books/${props.isbn}/reviews/`, {
      content: content.value,
      rating: rating.value,
    })
    Swal.fire({
  icon: 'success',
  title: '작성 완료!',
  text: '리뷰가 등록되었습니다.',
  confirmButtonText: '확인',
  customClass: {
    confirmButton: 'bg-yellow-400 hover:bg-yellow-500 text-white font-bold py-2 px-4 rounded',
  },
  buttonsStyling: false,  // ✅ Tailwind 클래스 적용 시 필수!
})
    content.value = ''
    rating.value = ''
    emit('refresh')  // 부모에게 리뷰 다시 불러오라고 알림
  } catch (err) {
    const msg = err.response?.data?.error || '리뷰 작성 실패'
    Swal.fire({
  icon: 'error',
  title: '오류',
  text: msg,
  confirmButtonText: '확인',
  customClass: {
    confirmButton: 'bg-red-400 hover:bg-red-500 text-white font-bold py-2 px-4 rounded',
  },
  buttonsStyling: false,
})
  }
}
</script>