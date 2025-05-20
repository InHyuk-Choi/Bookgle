<template>
  <main class="pt-[100px] pb-20 flex flex-col items-center bg-[#fffdf8] min-h-screen relative">

    <!-- 🧷 상단 고정된 아이콘 바 -->
    <div class="fixed top-0 w-full flex justify-between items-center px-6 py-2 z-50 bg-[#fffdf8]">
      
      <!-- 왼쪽: 책 아이콘 -->
      <img
        src="/bookcase.png"
        class="w-10 h-10 object-contain hover:scale-110 transition-transform mt-[-4px]"
      />

      <!-- 가운데: 로고 -->
      <img
        src="/favicon.png"
        alt="logo"
        class="w-28 h-20 object-contain"
      />

      <!-- 오른쪽: 상점 & 보관함 -->
      <div class="flex gap-6 items-center">
                <img
          src="/box.png"
          alt="보관함"
          class="w-10 h-10 object-contain hover:scale-110 transition-transform cursor-pointer"
        />
        <img
          src="/cart.png"
          alt="상점"
          class="w-10 h-10 object-contain hover:scale-110 transition-transform cursor-pointer"
        />

      </div>
    </div>

    <!-- 본문 콘텐츠 -->
    <PetStatus />
    <LevelInfo />
    <BottomNavbar />
  </main>
</template>



  <script setup>
  import PetStatus from '@/components/PetStatus.vue'
  import LevelInfo from '@/components/LevelInfo.vue'
  import BottomNavbar from '@/components/BottomNavbar.vue'
  </script>
  