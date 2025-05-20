<template>
  <div class="relative w-[400px] h-[400px] flex items-center justify-center mt-[260px]">
    <!-- 캐릭터 비디오 -->
    <video
      src="/brokenegg.mp4"
      autoplay
      loop
      muted
      playsinline
      class="w-full h-full object-contain cursor-pointer"
      @click="toggleBubble"
    ></video>

    <!-- 말풍선 (클릭 시 나타남) -->
    <div
      v-if="showBubble"
      class="absolute top-[8px] left-[80%] -translate-x-1/2 bg-yellow-100 border border-yellow-300 shadow-md px-4 py-2 rounded-xl text-sm text-black text-center w-[240px]
              hover:scale-105 transition-transform cursor-default
              before:content-[''] before:absolute before:bottom-[-10px] before:left-6 
              before:border-l-[10px] before:border-l-transparent 
              before:border-r-[10px] before:border-r-transparent 
              before:border-t-[10px] before:border-t-yellow-100"
    >
      <p class="font-bold">어제까지 52페이지 읽었어!</p>
      <p>오늘은 몇 페이지까지 읽을거야?</p>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'

const showBubble = ref(false)

const toggleBubble = () => {
  showBubble.value = !showBubble.value
}
</script>
