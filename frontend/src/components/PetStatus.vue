<template>  
  <div class="relative w-full max-w-[320px] sm:max-w-[360px] md:max-w-[400px] aspect-square flex items-center justify-center">
          <video
            src="/brokenegg.mp4"
            autoplay
            loop
            muted
            playsinline
            class="w-full h-full object-contain cursor-pointer"
            @click="toggleBubble"
          ></video>

          <div
  v-if="showBubble"
  class="
    absolute top-[-40px] left-[96%] -translate-x-1/2
    bg-yellow-100 border border-yellow-300 shadow-md
    px-8 py-6 rounded-xl text-lg text-black text-center w-[320px]
    hover:scale-105 transition-transform cursor-default
    before:content-[''] before:absolute before:bottom-[-10px] before:left-6
    before:border-l-[10px] before:border-l-transparent
    before:border-r-[10px] before:border-r-transparent
    before:border-t-[10px] before:border-t-yellow-100
  "
>
  <p class="font-bold">어제까지 {{ auth.readPages }} 페이지 읽었어!</p>
  <p>오늘은 몇 페이지까지 읽을거야?</p>
</div>
</div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useAuthStore } from '@/stores/auth'

const auth = useAuthStore()
const showBubble = ref(false)

const toggleBubble = () => {
  showBubble.value = !showBubble.value
}

onMounted(() => {
  auth.fetchUserStatus()
})
</script>
