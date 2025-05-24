<template>
  <div class="min-h-screen bg-[#fffdf8] px-6 pt-60 pb-12">
    <h2 class="text-3xl font-bold text-center mb-2">상점</h2>
    <p class="text-center text-gray-700 mb-6">
      보유 포인트: <span class="font-bold">{{ auth.totalPoints }}</span>점
    </p>
    <!-- 🔥 테스트용 포인트 지급 버튼 -->
    <div class="flex justify-center mb-6">
      <button @click="giveTestPoints" class="test-btn">
        포인트 3점 지급 (테스트용)
      </button>
    </div>
    <div class="grid grid-cols-1 sm:grid-cols-2 gap-6 max-w-xl mx-auto">
      <!-- 일반먹이 -->
      <div class="bg-white p-6 rounded-xl shadow-md flex flex-col items-center space-y-4 border">
        <img src="/food-basic.png" alt="일반먹이" class="w-20 h-20 object-contain" />
        <h3 class="text-xl font-semibold">일반먹이</h3>
        <p class="text-gray-600">가격: 10 포인트</p>
        <button @click="buy('basic', 10)" class="buy-btn">구매하기</button>
      </div>

      <!-- 고급먹이 -->
      <div class="bg-white p-6 rounded-xl shadow-md flex flex-col items-center space-y-4 border">
        <img src="/food-premium.png" alt="고급먹이" class="w-20 h-20 object-contain" />
        <h3 class="text-xl font-semibold">고급먹이</h3>
        <p class="text-gray-600">가격: 30 포인트</p>
        <button @click="buy('premium', 30)" class="buy-btn">구매하기</button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { onMounted } from 'vue'
import { useAuthStore } from '@/stores/auth'
import Swal from 'sweetalert2'
import axios from 'axios'

const auth = useAuthStore()

onMounted(() => {
  auth.fetchUserStatus()  // 포인트 포함한 유저 정보
})
const giveTestPoints = async () => {
  try {
    const res = await axios.post('http://localhost:8000/api/v1/accounts/points/add/', {
      amount: 100
    })

    auth.totalPoints = res.data.total_points

    await Swal.fire({
      icon: 'success',
      title: '포인트 +3 지급 완료!',
      text: `현재 포인트: ${res.data.total_points}`,
    })
  } catch (err) {
    console.error('포인트 지급 실패:', err)
  }
}



// 구매 함수
const buy = async (type, price) => {
  if (auth.totalPoints < price) {
    await Swal.fire({
  icon: 'error',
  title: '포인트 부족!',
  text: '포인트가 부족해요!',
  customClass: {
    popup: 'bg-white text-gray-900',
    icon: 'text-red-500',
    confirmButton: 'custom-ok-button-red',
  }
})

    return
  }

  try {
    await auth.purchaseFood({ type, quantity: 1, cost: price })
    await Swal.fire({
      icon: 'success',
      title: `${type === 'basic' ? '일반먹이' : '고급먹이'} 구매 완료!`,
      text: '펫에게 먹이를 줄 수 있어요!',
      confirmButtonText: '확인',
      customClass: {
        confirmButton: 'custom-ok-button-blue',
      }
    })
  } catch (err) {
    console.error('먹이 구매 실패:', err)
  }
}
</script>

<style scoped>
.buy-btn {
  @apply bg-yellow-400 text-white font-bold py-2 px-4 rounded-lg hover:bg-yellow-500 transition;
}

.test-btn {
  @apply bg-blue-500 text-white font-semibold py-2 px-4 rounded-lg hover:bg-blue-600 transition;
}

.custom-ok-button-blue {
  background-color: #3b82f6 !important;
  color: white !important;
  font-weight: 600;
  border-radius: 0.375rem;
  padding: 0.5rem 1rem;
  box-shadow: none !important;
}

.custom-ok-button-blue:hover {
  background-color: #2563eb !important;
  transform: scale(1.08);
}
</style>
