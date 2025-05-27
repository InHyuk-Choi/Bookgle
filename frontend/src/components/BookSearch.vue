<template>
  <div class="max-w-xl mx-auto px-6 py-10 bg-white shadow-xl rounded-2xl mt-12">
    <h2 class="text-2xl font-bold text-center mb-6 text-gray-800">📚 책 검색</h2>

    <!-- 검색창 -->
    <div class="flex items-center gap-2 mb-6">
      <input
        v-model="query"
        @keyup.enter="searchBooks"
        type="text"
        placeholder="책 제목 또는 저자"
        class="flex-1 px-4 py-2 border rounded-lg shadow-sm focus:ring-2 focus:ring-blue-400 focus:outline-none"
      />
      <button
        @click="searchBooks"
        class="bg-blue-500 hover:bg-blue-600 text-white font-semibold px-4 py-2 rounded-lg shadow transition"
      >
        검색
      </button>
    </div>

    <!-- 결과 목록 -->
    <div v-if="results.length" class="space-y-3">
      <div
        v-for="book in results"
        :key="book.isbn"
        class="flex items-center gap-4 p-4 bg-gray-50 border rounded-xl shadow-sm hover:bg-blue-50 cursor-pointer transition"
        @click="registerBook(book)"
      >
        <img
          :src="book.cover_image || '/default-cover.png'"
          alt="책 표지"
          class="w-16 h-24 object-cover rounded border"
        />
        <div>
          <p class="text-lg font-bold text-gray-800">{{ book.title }}</p>
          <p class="text-sm text-gray-500">{{ book.author }}</p>
        </div>
      </div>
    </div>

    <!-- 검색 결과 없음 -->
    <p v-else-if="searched" class="text-center text-gray-400 mt-6">검색 결과가 없습니다.</p>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import axios from 'axios'
import Swal from 'sweetalert2'
import { useAuthStore } from '@/stores/auth'
import { useRouter } from 'vue-router'


const auth = useAuthStore()
const query = ref('')
const results = ref([])
const searched = ref(false)
const router = useRouter()



const searchBooks = async () => {
  if (!query.value.trim()) return
  try {
    const res = await axios.get('http://localhost:8000/api/v1/kkubook/books/search/', {
      params: { q: query.value, type: 'Keyword' }
    })
    console.log(res.data)
    results.value = res.data
    searched.value = true
  } catch (err) {
    console.error(err)
    await Swal.fire({
      title: '오류',
      text: '검색 실패',
      icon: 'error',
      confirmButtonText: '확인',
      customClass: {
        confirmButton: 'bg-red-500 hover:bg-red-600 text-white font-bold py-2 px-4 rounded',
      },
      buttonsStyling: false,
    })
  }
}


const registerBook = async (book) => {
  try {
    const res = await axios.post('http://localhost:8000/api/v1/kkubook/books/register/', book)
    await auth.fetchUserStatus()
    await Swal.fire({
      title: '등록 완료! 🎉',
      text: `"${res.data.title}" 책이 등록되었습니다.`,
      icon: 'success',
      confirmButtonText: '확인',
      customClass: {
        confirmButton: 'bg-blue-500 hover:bg-blue-600 text-white font-bold py-2 px-4 rounded',
      },
      buttonsStyling: false,
    })
    router.push('/')
  } catch (err) {
    const msg = err.response?.data?.error || '등록 실패'
    await Swal.fire({
      title: '오류',
      text: msg,
      icon: 'error',
      confirmButtonText: '확인',
      customClass: {
        confirmButton: 'bg-red-500 hover:bg-red-600 text-white font-bold py-2 px-4 rounded',
      },
      buttonsStyling: false,
    })
  }
}

</script>
