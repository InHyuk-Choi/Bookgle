<template>
  <div class="mt-10">
    <!-- 제목 -->
    <div class="flex items-center gap-2 mb-6">
      <span class="text-lg font-bold text-yellow-600">📄 사용자 리뷰</span>
    </div>

    <!-- 리뷰가 없을 경우 -->
    <div v-if="!reviews || reviews.length === 0" class="flex flex-col items-center justify-center text-gray-500 py-12">
      <div class="text-6xl mb-4 animate-bounce">🐛</div>
      <p class="text-sm text-center leading-relaxed">
        아직 등록된 리뷰가 없어요.<br />
        가장 먼저 리뷰를 남겨보세요!
      </p>
    </div>

    <!-- 리뷰 리스트 -->
    <div v-else class="space-y-4">
      <div
        v-for="review in reviews"
        :key="review.id"
        class="bg-[#fffcef] border border-yellow-200 rounded-xl p-5 shadow-sm"
      >
        <!-- 상단: 유저 아이콘 + 이름 + 점수 -->
        <div class="flex justify-between items-center mb-1">
          <div class="flex items-center gap-2">
            <div class="w-7 h-7 rounded-full bg-yellow-100 text-yellow-600 font-bold flex items-center justify-center">
              {{ review.username.charAt(0).toUpperCase() }}
            </div>
            <span class="font-semibold text-sm text-gray-700">{{ review.nickname }}</span>
          </div>
          <div class="flex items-center text-yellow-500 text-sm font-medium">
            ⭐ {{ review.rating }}점
          </div>
        </div>

        <!-- 리뷰 내용 -->
        <p class="text-sm text-gray-700 whitespace-pre-line mt-1">
          {{ review.content }}
        </p>
      </div>
    </div>
  </div>
</template>

<script setup>
defineProps({ reviews: Array })
</script>
