<template>
  <div class="relative w-full max-w-[320px] sm:max-w-[360px] md:max-w-[400px] aspect-square flex items-center justify-center">
    <img
      :src="characterImage"
      alt="캐릭터"
      class="w-full h-full object-contain cursor-pointer"
      @click="toggleBubble"
    />

    <!-- 💬 말풍선 -->
    <div
  v-if="showBubble"
  class="absolute -top-28 left-56 mr-4
         w-[320px] bg-[#fffce8] border border-yellow-300 rounded-2xl
         px-6 py-5 shadow-lg text-base text-gray-800 animate-fade-in
         transition-all z-10
         before:content-[''] before:absolute before:bottom-[-10px] before:left-6
         before:border-l-[10px] before:border-l-transparent
         before:border-r-[10px] before:border-r-transparent
         before:border-t-[10px] before:border-t-[#fffce8]"
>
      <!-- 📚 책 있을 때 -->
      <template v-if="!inputMode">
        <template v-if="auth.currentBookTitle">
          <p class="font-bold text-lg mb-2">
            📖 지금까지
            <span class="text-blue-600 font-semibold">{{ auth.currentBookTitle }}</span>의
            <span class="text-yellow-600 font-semibold">{{ auth.readPages }}페이지</span>까지 읽었어!
          </p>
          <p>오늘은 몇 페이지까지 읽을 거야?</p>
          <div class="mt-4 space-x-4">
            <button @click="handleInputClick" class="text-sm text-yellow-500 font-medium hover:underline">입력하기</button>
            <button @click="goToBookSearch" class="text-sm text-blue-500 font-medium hover:underline">책 고르기</button>
          </div>
        </template>

        <!-- ❌ 책 없을 때 -->
        <template v-else>
          <p class="font-bold text-lg mb-2">📖 아직 읽고 있는 책이 없어요!</p>
          <p>새 책을 등록해 볼까요?</p>
          <button @click="goToBookSearch" class="mt-4 text-sm text-blue-500 font-medium hover:underline">책 고르기</button>
        </template>
      </template>

      <!-- 📝 입력 모드 -->
      <template v-else>
        <input
          v-model.number="todayPages"
          type="number"
          placeholder="예: 120"
          class="w-full bg-yellow-50 border border-yellow-300 rounded-full px-4 py-2 mt-3 text-center text-lg focus:outline-none focus:ring-2 focus:ring-yellow-400 transition shadow-inner"
        />
        <div class="flex justify-end mt-3 gap-2">
          <button @click="submitPages(todayPages)" class="bg-yellow-400 hover:bg-yellow-500 p-3 rounded-full shadow-md">
            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" class="w-6 h-6" stroke="white">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 5h6m-3-3v6m7 14H6a2 2 0 01-2-2V6m16 0v12a2 2 0 01-2 2z" />
            </svg>
          </button>
          <button @click="inputMode = false" class="text-sm text-gray-500 hover:underline">취소</button>
        </div>
      </template>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { useAuthStore } from '@/stores/auth'
import axios from 'axios'
import Swal from 'sweetalert2'
import { useRouter } from 'vue-router'

const auth = useAuthStore()
const router = useRouter()
const showBubble = ref(false)
const inputMode = ref(false)
const todayPages = ref('')

const toggleBubble = () => {
  showBubble.value = !showBubble.value
}

const goToBookSearch = () => {
  router.push({ name: 'book-search' })
}

const handleInputClick = async () => {
  const result = await Swal.fire({
    title: '📘 완독했나요?',
    text: '이 책을 다 읽었나요?',
    icon: 'question',
    showCancelButton: true,
    confirmButtonText: '예',
    cancelButtonText: '아니오',
    reverseButtons: false,
    customClass: {
      popup: 'bg-white text-gray-900',
      confirmButton: 'bg-green-500 text-white px-4 py-2 rounded hover:bg-green-600',
      cancelButton: 'bg-gray-300 text-black px-4 py-2 rounded hover:bg-gray-400',
    },
  })

  if (result.isConfirmed) {
    try {
      const title = auth.currentBookTitle
      await axios.post('http://localhost:8000/api/v1/kkubook/books/finish/', {
        book_title: title,
      })
      router.push({
  name: 'quiz',
  query: {
    title: auth.currentBook.title,
    author: auth.currentBook.author,
    publisher: auth.currentBook.publisher,
    cover_image: auth.currentBook.cover_image,
    description: auth.currentBook.description,
    isbn: auth.currentBook.isbn  // ✅ 누락 없이!
  }
})


    } catch (err) {
      Swal.fire({
        icon: 'error',
        title: '완독 처리 실패',
        text: err.response?.data?.error || '완독 처리 중 문제가 발생했어요!',
      })
    }
  } else {
    inputMode.value = true
  }
}

const submitPages = async (pageNum) => {
  try {
    const res = await axios.post('http://localhost:8000/api/v1/kkubook/pages/set/', {
      pages: pageNum,
    })

    if (res.data.already_recorded) {
      Swal.fire({
  icon: 'info',
  title: '오늘은 이미 기록했어요!',
  text: '내일 다시 기록해 주세요 🙂',
  confirmButtonText: '확인',
  customClass: {
    confirmButton: 'bg-blue-400 hover:bg-blue-500 text-white font-bold px-4 py-2 rounded mt-2'
  }
})
      return
    }

      Swal.fire({
    icon: 'success',
    title: '기록 완료!',
    text: `${pageNum}페이지까지 읽었어요! (+15포인트 지급)`,
    confirmButtonText: '확인',
    customClass: {
      confirmButton: 'bg-yellow-400 hover:bg-yellow-500 text-white font-bold px-4 py-2 rounded mt-2'
    }
  })

    auth.fetchUserStatus()
    inputMode.value = false
  } catch (err) {
    Swal.fire({
  icon: 'error',
  title: '기록 실패',
  text: err.response?.data?.error || '문제가 발생했어요!',
  confirmButtonText: '확인',
  customClass: {
    confirmButton: 'bg-red-400 hover:bg-red-500 text-white font-bold px-4 py-2 rounded mt-2'
  }
})

  }
}

const characterImage = computed(() => {
  const level = auth.bookworm.level
  if (level >= 60) return '/char7.gif'
  if (level >= 50) return '/char6.gif'
  if (level >= 40) return '/char5.gif'
  if (level >= 30) return '/char4.gif'
  if (level >= 20) return '/char3.gif'
  if (level >= 10) return '/char2.gif'
  return '/char1.gif'
})

onMounted(() => {
  auth.fetchUserStatus()
  auth.fetchBookwormStatus()
})
</script>

<style>
@keyframes fade-in {
  0% {
    opacity: 0;
    transform: scale(0.95);
  }
  100% {
    opacity: 1;
    transform: scale(1);
  }
}
.animate-fade-in {
  animation: fade-in 0.2s ease-out;
}
</style>