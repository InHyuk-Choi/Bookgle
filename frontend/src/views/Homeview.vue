<template>
  <div class="relative h-screen overflow-hidden bg-[#fffdf8]">

    <!-- 🧷 상단 고정된 아이콘 바 -->
    <div class="fixed top-0 w-full flex justify-between items-center px-6 py-2 z-50 bg-[#fffdf8]">
      <img src="/bookcase.png" class="w-10 h-10 object-contain hover:scale-110 transition-transform mt-[-4px]" />
      <img src="/favicon.png" alt="logo" class="w-28 h-20 object-contain" />
      <div class="flex gap-6 items-center">
          <div>
    <!-- 📦 보관함 버튼 -->
    <img
      src="/box.png"
      alt="보관함"
      class="w-10 h-10 object-contain cursor-pointer hover:scale-110 transition-transform"
      @click="openInventory"
    />

    <!-- 📦 보관함 사이드바 -->
    <InventorySidebar
  :isOpen="showInventory"
  :foodBasic="foodBasic"
  :foodPremium="foodPremium"
  @close="showInventory = false"
/>
  </div>
        <img src="/cart.png" alt="상점" class="w-10 h-10 object-contain hover:scale-110 transition-transform cursor-pointer" @click="router.push({ name: 'store' })" />
      </div>
    </div>

    <!-- 📦 본문 콘텐츠: 수직 중앙 배치 -->
<main
      class="absolute top-[88px] bottom-[64px] left-0 right-0 flex justify-center items-center overflow-y-auto">
          <div class="flex flex-col items-center gap-4 transform scale-[0.85] sm:scale-[0.9] md:scale-100 origin-center">
      <PetStatus />
      <LevelInfo />
      </div>
    </main>

    <!-- 🔒 하단 고정 바텀 네브바 -->
    <BottomNavbar />
  </div>
</template>

<script setup>
import PetStatus from '@/components/PetStatus.vue'
import LevelInfo from '@/components/LevelInfo.vue'
import BottomNavbar from '@/components/BottomNavbar.vue'
import { useRouter } from 'vue-router'
import { ref } from 'vue'
import InventorySidebar from '@/components/InventorySidebar.vue'

const showInventory = ref(false)
const openInventory = () => {
  showInventory.value = true
}

// ✅ 테스트용 보유 먹이 수
const foodBasic = ref(3)
const foodPremium = ref(1)
const router = useRouter()

</script>