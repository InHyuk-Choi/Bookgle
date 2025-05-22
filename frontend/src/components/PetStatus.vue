<template>
<div class="relative w-full max-w-[320px] sm:max-w-[360px] md:max-w-[400px] aspect-square flex items-center justify-center">
  <img
    src="/char6.gif"
    alt="캐릭터"
    class="w-full h-full object-contain cursor-pointer"
    @click="toggleBubble"
  />



<!-- 말풍선 내부 -->
<!-- 말풍선 -->
<div
  v-if="showBubble"
  class="absolute top-[-40px] left-[96%] -translate-x-1/2
         w-[320px] bg-[#fffce8] border border-yellow-300 rounded-2xl
         px-6 py-5 shadow-lg text-base text-gray-800 animate-fade-in cursor-default
         transition-transform hover:scale-[1.02]
         before:content-[''] before:absolute before:bottom-[-10px] before:left-6
         before:border-l-[10px] before:border-l-transparent
         before:border-r-[10px] before:border-r-transparent
         before:border-t-[10px] before:border-t-[#fffce8]"
>
  <!-- 기본 메시지 -->
  <template v-if="!inputMode">
    <p class="font-bold text-lg mb-2">📖 지금까지 {{ auth.readPages }}페이지 읽었어!</p>
    <p>오늘은 몇 페이지까지 읽을 거야?</p>
    <button
      @click="inputMode = true"
      class="mt-4 text-sm text-yellow-500 font-medium hover:underline"
    >입력하기</button>
  </template>

  <!-- 입력 모드 -->
  <template v-else>
    <input
      v-model="todayPages"
      type="number"
      placeholder="예: 120"
      class="w-full bg-yellow-50 border border-yellow-300 rounded-full
             px-4 py-2 mt-3 text-center text-lg focus:outline-none focus:ring-2
             focus:ring-yellow-400 transition shadow-inner"
    />
    <div class="flex justify-end mt-3 gap-2">
      <button
  @click="submitPages"
  class="bg-yellow-400 hover:bg-yellow-500 p-3 rounded-full shadow-md"
>
  <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" class="w-6 h-6" stroke="white">
  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
        d="M11 5h6m-3-3v6m7 14H6a2 2 0 01-2-2V6m16 0v12a2 2 0 01-2 2z"/>
</svg>
</button>
      <button
        @click="inputMode = false"
        class="text-sm text-gray-500 hover:underline"
      >
        취소
      </button>
    </div>
  </template>
</div>

</div>

</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useAuthStore } from '@/stores/auth'
import axios from 'axios'
import Swal from 'sweetalert2'

const auth = useAuthStore()
const showBubble = ref(false)
const showModal = ref(false)
const todayPages = ref('')
const inputMode = ref(false)

const toggleBubble = () => {
  showBubble.value = !showBubble.value
}

const submitPages = async () => {
  const pageNum = parseInt(todayPages.value)
  if (isNaN(pageNum) || pageNum < 0) {
    Swal.fire('잘못된 입력', '0 이상의 숫자를 입력해주세요!', 'error')
    return
  }

  try {
    await axios.post('http://localhost:8000/api/v1/accounts/pages/set/', {
      pages: pageNum
    })
    Swal.fire('기록 완료!', `${pageNum}페이지까지 읽었어요!.`, 'success')
    showModal.value = false
    auth.fetchUserStatus() // 갱신
  } catch (err) {
    console.error(err)
    Swal.fire('오류 발생', '페이지 기록 중 문제가 생겼어요.', 'error')
  }
}


onMounted(() => {
  auth.fetchUserStatus()
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
