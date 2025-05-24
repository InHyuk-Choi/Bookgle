
<template>
  <transition name="slide">
    <div v-if="isOpen" class="fixed inset-0 z-50 flex justify-end" @click.self="close">
      <div class="w-72 bg-white h-full shadow-lg p-6 flex flex-col">
        <div class="flex justify-between items-center mb-4">
          <h2 class="text-xl font-bold">📦 보관함</h2>
          <button @click="close" class="text-gray-500 hover:text-black text-xl">✕</button>
        </div>

        <!-- 먹이 카드 1: 헌책 -->
        <div class="flex flex-col items-center mb-6">
          <img src="/food-basic.png" alt="헌책" class="w-20 h-20 object-contain mb-2" />
          <p class="text-lg font-semibold">헌책</p>
          <p class="text-sm text-gray-600 mb-2">보유 수량: {{ auth.basicFood }}개</p>
          <button
            class="bg-yellow-400 hover:bg-yellow-500 text-white font-bold py-2 px-4 rounded transition"
            @click="feedPet('basic')"
            :disabled="auth.basicFood <= 0"
          >
            먹이 주기
          </button>
        </div>

        <!-- 먹이 카드 2: 새책 -->
        <div class="flex flex-col items-center">
          <img src="/food-premium.png" alt="새책" class="w-20 h-20 object-contain mb-2" />
          <p class="text-lg font-semibold">새책</p>
          <p class="text-sm text-gray-600 mb-2">보유 수량: {{ auth.premiumFood }}개</p>
          <button
            class="bg-yellow-400 hover:bg-yellow-500 text-white font-bold py-2 px-4 rounded transition"
            @click="feedPet('premium')"
            :disabled="auth.premiumFood <= 0"
          >
            먹이 주기
          </button>
        </div>
      </div>
    </div>
  </transition>
</template>

<script setup>
import Swal from 'sweetalert2'
import { useAuthStore } from '@/stores/auth'

const auth = useAuthStore()
console.log(auth.basicFood)
const props = defineProps({
  isOpen: Boolean,
})

const emit = defineEmits(['close'])

const close = () => emit('close')

// 먹이 주기 버튼 눌렀을 때
const feedPet = async (type) => {
  try {
    console.log(auth.basicFood)
    await auth.feedBookworm(type)  // ✅ 실제 먹이 주기 API 호출

    await Swal.fire({
      icon: 'success',
      title: `${type === 'basic' ? '헌책' : '새책'}을(를) 먹였어요!`,
      text: '펫이 좋아하고 있어요 🐾',
      confirmButtonText: '확인',
      customClass: {
        confirmButton: 'custom-ok-button-blue',
      }
    })
  } catch (err) {
    console.error('먹이 주기 실패:', err)
  }
}
</script>

<style scoped>
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
