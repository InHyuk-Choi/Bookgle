<template>
<div class="px-4 pt-32 pb-10 max-w-6xl mx-auto bg-[#fffdf8] min-h-screen">

    <!-- 제목 -->
    <h2 class="text-3xl font-extrabold text-center text-yellow-500 tracking-wide mb-8 mt-4 drop-shadow-sm font-[Pretendard]">
      오늘의 추천 도서
    </h2>

    <!-- 로딩 상태 -->
    <div v-if="loading" class="fixed inset-0 bg-white/60 flex items-center justify-center z-50">
      <div class="bg-white rounded-2xl shadow-xl px-8 py-6 flex flex-col items-center gap-3 border border-gray-200">
        <svg class="w-12 h-12 text-green-400 animate-spin" fill="none" viewBox="0 0 24 24">
          <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4" />
          <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z" />
        </svg>
        <h2 class="text-gray-700 font-semibold text-lg">
          책벌레가 도서를 고르는 중이에요 <span class="inline-block animate-bounce">🐛</span>
        </h2>
      </div>
    </div>

    <!-- 데이터 없을 때 -->
    <div v-else-if="books.length === 0" class="text-center text-gray-400 mt-10">
      추천 도서가 없습니다.
    </div>

    <!-- 추천 도서 카드 목록 -->
    <div v-else class="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-5 gap-5">
      <div
        v-for="book in books"
        :key="book.isbn"
        @click="goToDetail(book)"
        class="cursor-pointer bg-white rounded-2xl shadow-md hover:shadow-xl transition hover:scale-[1.02] p-3 border border-gray-100"
      >
        <div class="w-full aspect-[2/3] bg-gray-50 rounded-xl overflow-hidden flex items-center justify-center">
          <img
            :src="book.cover_image || '/default-cover.png'"
            alt="책 표지"
            class="w-full h-full object-contain"
          />
        </div>
        <h3 class="mt-3 font-semibold text-sm text-gray-800 line-clamp-2 leading-snug">{{ book.title }}</h3>
        <p class="text-xs text-gray-500 line-clamp-1">{{ book.author }}</p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'
import { useRouter } from 'vue-router'

const books = ref([])
const loading = ref(true)
const router = useRouter()

const goToDetail = (book) => {
  router.push({
    name: 'BookDetail',
    params: { isbn: book.isbn },
    query: {
      title: book.title,
      author: book.author,
      publisher: book.publisher,
      cover_image: book.cover_image,
      description: book.description,
    },
  })
}

onMounted(async () => {
  try {
    const res = await axios.get('http://localhost:8000/api/v1/kkubook/books/recommend/')
    books.value = res.data.results || []
  } catch (err) {
    console.error('📕 추천 도서 로딩 실패:', err)
    books.value = []
  } finally {
    loading.value = false
  }
})
</script>

<style scoped>
/* line-clamp 지원 */
.line-clamp-2 {
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.line-clamp-1 {
  display: -webkit-box;
  -webkit-line-clamp: 1;
  -webkit-box-orient: vertical;
  overflow: hidden;
}
</style>