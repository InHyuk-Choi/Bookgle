<script setup>
import { useAuthStore } from '@/stores/auth'
const auth = useAuthStore()
</script>

<template>
  <div class="text-center mt-2">
    <p class="text-sm text-gray-600">
      현재 단계: <strong>책벌레</strong> <!-- 추후 캐릭터명도 바꾸면 됨 -->
    </p>

    <p class="text-lg font-semibold">Level {{ auth.bookworm.level }}</p>

    <!-- 경험치 바 -->
    <div class="bg-[#e6e6e6] h-2 rounded-full w-40 mx-auto mt-1">
      <div
        class="bg-blue-400 h-2 rounded-full transition-all duration-300"
        :style="{ width: (auth.bookworm.progress * 100).toFixed(1) + '%' }"
      ></div>
    </div>

    <p class="text-sm text-gray-500 mt-1">
      다음 진화까지 {{ auth.bookworm.exp_to_next - auth.bookworm.experience }}xp 남음
    </p>
  </div>
</template>
