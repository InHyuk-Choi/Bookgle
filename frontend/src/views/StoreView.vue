<template>
  <div class="min-h-screen bg-[#fffdf8] px-6 pt-60 pb-12">
    <h2 class="text-3xl font-bold text-center mb-8">상점</h2>

    <div class="grid grid-cols-1 sm:grid-cols-2 gap-6 max-w-xl mx-auto">
      <!-- 일반먹이 -->
      <div class="bg-white p-6 rounded-xl shadow-md flex flex-col items-center space-y-4 border">
        <img src="/food-basic.png" alt="일반먹이" class="w-20 h-20 object-contain" />
        <h3 class="text-xl font-semibold">일반먹이</h3>
        <p class="text-gray-600">가격: 10 포인트</p>
        <button @click="buy('일반먹이')" class="buy-btn">구매하기</button>
      </div>

      <!-- 고급먹이 -->
      <div class="bg-white p-6 rounded-xl shadow-md flex flex-col items-center space-y-4 border">
        <img src="/food-premium.png" alt="고급먹이" class="w-20 h-20 object-contain" />
        <h3 class="text-xl font-semibold">고급먹이</h3>
        <p class="text-gray-600">가격: 30 포인트</p>
        <button @click="buy('고급먹이')" class="buy-btn">구매하기</button>
      </div>
    </div>
  </div>
</template>

<script setup>
import Swal from 'sweetalert2'

const buy = (itemName) => {
  Swal.fire({
    icon: 'success',
    title: `${itemName} 구매 완료!`,
    text: '펫에게 먹이를 줄 수 있어요!',
    confirmButtonText: '확인',
    customClass: {
      confirmButton: 'custom-ok-button-blue',
    }
  })
}
</script>

<style scoped>
.buy-btn {
  @apply bg-yellow-400 text-white font-bold py-2 px-4 rounded-lg hover:bg-yellow-500 transition;
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
