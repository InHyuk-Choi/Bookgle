
<template>
  <div class="w-full max-w-md bg-white shadow rounded-lg p-4 mb-4 border">
    <div class="flex justify-between items-center mb-2">
      <p class="font-bold text-lg">{{ feed.nickname }}</p>
      <span class="text-sm text-gray-500">{{ feed.created_at }}</span>
    </div>
    <p class="mb-2">{{ feed.content }}</p>
    <div class="text-sm text-gray-600">❤️ {{ feed.likes }} 좋아요</div>
  </div>
</template>

<script setup>
defineProps({
  feed: Object
})
</script>
