<template>
  <div class="pt-40 p-6 max-w-md mx-auto bg-white rounded-xl shadow-md text-center space-y-4">
    <h2 class="text-xl font-bold">프로필 사진 업로드</h2>

    <img
      v-if="auth.profileImage"
      :src="`http://localhost:8000${auth.profileImage}`"
      alt="현재 프로필"
      class="w-32 h-32 rounded-full object-cover mx-auto border"
    />

    <input type="file" @change="handleFileChange" accept="image/*" />

    <button @click="uploadImage" class="upload-btn" :disabled="!selectedFile">
      업로드
    </button>
  </div>
</template>


<script setup>
import { ref } from 'vue'
import axios from 'axios'
import { useAuthStore } from '@/stores/auth'
import Swal from 'sweetalert2'

const auth = useAuthStore()
const selectedFile = ref(null)

const handleFileChange = (e) => {
  selectedFile.value = e.target.files[0]
}

const uploadImage = async () => {
  if (!selectedFile.value) return

  const formData = new FormData()
  formData.append('profile_image', selectedFile.value)

  try {
    const res = await axios.post('http://localhost:8000/api/v1/accounts/profile/upload/', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    })

    auth.profileImage = res.data.profile_image

    await Swal.fire('성공!', '프로필 사진이 업로드되었습니다.', 'success')
  } catch (err) {
    console.error('업로드 실패:', err)
    Swal.fire('실패!', '업로드 중 오류가 발생했습니다.', 'error')
  }
}
</script>

<style scoped>
.upload-btn {
  @apply bg-blue-500 text-white px-4 py-2 rounded hover:bg-blue-600 transition;
}
</style>
