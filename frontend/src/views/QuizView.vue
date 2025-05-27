<template>
  <div class="pt-32 pb-20 px-4 max-w-xl mx-auto bg-[#fffdf8] min-h-screen text-gray-800">
    <div v-if="quiz.length" class="bg-white rounded-2xl shadow-xl p-6 space-y-8 animate-fade-in">
      
      <!-- 📊 Progress Bar -->
      <div class="w-full h-3 rounded-full overflow-hidden bg-gray-200">
        <div
          class="h-full transition-all duration-500"
          :style="{ width: `${progressPercentage}%`, backgroundColor: progressColor }"
        ></div>
      </div>

      <!-- 문제 헤더 -->
      <div class="text-center">
        <p class="text-sm text-gray-500 mb-1">📘 문제 {{ currentIndex + 1 }} / {{ quiz.length }}</p>
        <h2 class="text-xl font-bold text-gray-800 leading-relaxed">
          {{ currentQuestion.question }}
        </h2>
      </div>

      <!-- 선택지 -->
      <div class="space-y-4">
        <button
          v-for="(option, index) in currentQuestion.options"
          :key="index"
          :class="[ 
            'w-full text-left px-5 py-3 rounded-xl border transition font-semibold text-base',
            selectedAnswer === option
              ? (option === currentQuestion.answer
                ? 'bg-green-100 border-green-400 text-green-800'
                : 'bg-red-100 border-red-400 text-red-800')
              : 'bg-gray-50 hover:bg-yellow-100 border-gray-200 text-gray-800'
          ]"
          @click="selectAnswer(option)"
          :disabled="!!selectedAnswer"
        >
          <span class="mr-2">🔹</span>{{ option }}
        </button>
      </div>

      <!-- 다음 버튼 -->
      <button
        v-if="selectedAnswer"
        @click="goToNext"
        class="w-full bg-yellow-400 hover:bg-yellow-500 text-white font-bold py-3 rounded-xl transition mt-4 shadow-md"
      >
        {{ currentIndex === quiz.length - 1 ? '✅ 결과 보기' : '➡ 다음 문제' }}
      </button>
    </div>

    <!-- 로딩 -->
    <div v-else class="flex flex-col items-center justify-center mt-24 text-gray-400 animate-pulse">
      <span class="text-3xl mb-2">⏳</span>
      <p>퀴즈를 불러오는 중입니다...</p>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import axios from 'axios'
import Swal from 'sweetalert2'

const route = useRoute()
const router = useRouter()

const quiz = ref([])
const currentIndex = ref(0)
const selectedAnswer = ref(null)
const wrongAttempts = ref(0)

const currentQuestion = computed(() => quiz.value[currentIndex.value])

const progressPercentage = computed(() => {
  return ((currentIndex.value + 1) / quiz.value.length) * 100
})

const progressColor = computed(() => {
  const percent = progressPercentage.value
  if (percent < 40) return '#facc15'      // 노랑
  if (percent < 80) return '#38bdf8'      // 파랑
  return '#4ade80'                        // 초록
})

const fetchQuiz = async () => {
  try {
    const res = await axios.post('http://localhost:8000/api/v1/kkubook/questions/generate/', {
      title: route.query.title,
    })
    quiz.value = res.data.quiz
  } catch (err) {
    console.error('퀴즈 가져오기 실패:', err)
  }
}

const selectAnswer = async (option) => {
  const isCorrect = option === currentQuestion.value.answer

  if (isCorrect) {
    await Swal.fire({
      title: '정답입니다! 🎉',
      icon: 'success',
      timer: 1000,
      showConfirmButton: false,
    })
    goToNext()
  } else {
    wrongAttempts.value++

    if (wrongAttempts.value >= 3) {
      await Swal.fire({
        title: '퀴즈 실패 😢',
        html: `총 <b>3번</b> 틀렸어요.<br><br>다시 도전하고 싶다면<br>책을 다시 선택하고 완독 처리를 해주세요!`,
        icon: 'error',
        confirmButtonText: '홈으로',
        customClass: {
          confirmButton: 'bg-yellow-400 hover:bg-yellow-500 text-white font-bold py-2 px-4 rounded',
        },
        buttonsStyling: false,
      })
      router.push({ name: 'home' })
    } else {
      await Swal.fire({
        title: '틀렸어요 😢',
        text: `총 ${wrongAttempts.value}번 틀렸어요!`,
        icon: 'error',
        timer: 1500,
        showConfirmButton: false,
      })
    }
  }
}

const goToNext = async () => {
  if (currentIndex.value === quiz.value.length - 1) {
    let success = false
    try {
      await axios.post('http://localhost:8000/api/v1/kkubook/questions/quiz-complete/', {
        title: route.query.title,
      })
      success = true
    } catch (err) {
      if (err.response?.status === 409) {
        await Swal.fire({
          title: '퀴즈 완료됨 ✅',
          text: '이미 퀴즈를 완료한 책입니다.',
          icon: 'info',
          confirmButtonText: '홈으로',
          customClass: {
            confirmButton: 'bg-yellow-400 hover:bg-yellow-500 text-white font-bold py-2 px-4 rounded',
          },
          buttonsStyling: false,
        })
        router.push({ name: 'home' })
        return
      }
    }

if (success) {
  await Swal.fire({
  title: '퀴즈 완료 🎉',
  html: `모든 문제를 성공적으로 풀었어요!<br/>+50 포인트 지급!<br/><br/>📚 <b>책에 대한 리뷰도 작성해주세요!</b>`,
  icon: 'success',
  confirmButtonText: '리뷰 쓰러 가기',
  customClass: {
    confirmButton: 'bg-yellow-400 hover:bg-yellow-500 text-white font-bold py-2 px-4 rounded',
  },
  buttonsStyling: false,
})
if (!route.query.isbn) {
  console.error('❌ isbn이 누락되었습니다.')
  return
}
router.push({
  name: 'BookDetail',
  params: { isbn: route.query.isbn },
  query: {
    title: route.query.title,
    author: route.query.author,
    publisher: route.query.publisher,
    cover_image: route.query.cover_image,
    description: route.query.description,
  }
})

 // ✅ 성공 시 이동
} else {
  await Swal.fire({
    title: '퀴즈는 완료했지만... ❗',
    text: '포인트 지급에 실패했어요. 나중에 다시 시도해주세요.',
    icon: 'warning',
    confirmButtonText: '홈으로',
    customClass: {
      confirmButton: 'bg-gray-400 hover:bg-gray-500 text-white font-bold py-2 px-4 rounded',
    },
    buttonsStyling: false,
  })
  router.push({ name: 'home' })  // ❌ 이건 실패일 때만
}

  } else {
    currentIndex.value++
    selectedAnswer.value = null
  }
}

onMounted(() => {
  fetchQuiz()
})
</script>

<style>
.animate-fade-in {
  animation: fade-in 0.5s ease-in;
}
@keyframes fade-in {
  from { opacity: 0; transform: translateY(10px); }
  to { opacity: 1; transform: translateY(0); }
}
</style>
