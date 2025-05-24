<template>
  <div class="pt-32 pb-20 px-4 bg-[#fffdf8] min-h-screen flex justify-center">
    <div class="bg-white w-full max-w-lg rounded-2xl shadow-xl p-6 space-y-6">

      <h2 class="text-2xl font-bold text-center text-yellow-500">✍️ 피드 작성</h2>

      <!-- 📘 텍스트 입력 -->
      <textarea
        v-model="content"
        placeholder="책 읽고 느낀 점이나, 공유하고 싶은 생각을 적어보세요 :)"
        class="w-full h-40 border border-gray-300 rounded-lg p-4 text-sm focus:outline-none focus:ring-2 focus:ring-yellow-400 resize-none"
        required
      ></textarea>

      <!-- 🖼 이미지 업로드 -->
      <label class="block text-sm font-medium text-gray-600">사진 첨부 (선택)</label>
      <input
        type="file"
        accept="image/*"
        @change="onImageChange"
        class="block w-full text-sm text-gray-500 file:mr-4 file:py-2 file:px-4
               file:rounded-full file:border-0
               file:text-sm file:font-semibold
               file:bg-yellow-50 file:text-yellow-700
               hover:file:bg-yellow-100"
      />

      <!-- 📸 이미지 미리보기 -->
      <div v-if="previewImage" class="mt-2">
        <img :src="previewImage" class="w-full max-h-80 rounded-lg border" />
      </div>

      <!-- 🟡 제출 버튼 -->
      <button
        type="submit"
        @click="submitPheed"
        class="w-full bg-yellow-400 text-white font-bold py-3 rounded-lg hover:bg-yellow-500 transition text-lg"
      >
        작성 완료
      </button>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import axios from 'axios'
import { useRouter } from 'vue-router'
import Swal from 'sweetalert2'

const router = useRouter()
const content = ref('')
const imageFile = ref(null)
const previewImage = ref(null)

const onImageChange = (e) => {
  const file = e.target.files[0]
  if (file) {
    imageFile.value = file
    previewImage.value = URL.createObjectURL(file)
  }
}

const submitPheed = async () => {
  const formData = new FormData()
  formData.append('content', content.value)
  if (imageFile.value) {
    formData.append('image', imageFile.value)
  }

  try {
    await axios.post('http://localhost:8000/api/v1/kkubook/pheeds/', formData, {
      headers: {
        Authorization: `Bearer ${localStorage.getItem('access')}`,
        'Content-Type': 'multipart/form-data',
      }
    })

    await Swal.fire({
      icon: 'success',
      title: '피드 작성 완료!',
      text: '게시글이 정상적으로 등록되었어요 ✨',
      customClass: {
        popup: 'bg-white text-gray-900',
        icon: 'text-green-500',
        confirmButton: 'bg-yellow-400 text-white font-bold rounded px-4 py-2 mt-2 hover:bg-yellow-500'
      }
    })
    router.push({ name: 'feed' })
  } catch (err) {
    console.error('❌ 피드 작성 실패:', err)

    const errorData = err.response?.data
    const errorText = errorData
      ? Object.entries(errorData)
          .map(([field, messages]) => `${field}: ${messages.join(', ')}`)
          .join('\n')
      : '작성 중 오류가 발생했어요 😢'

    await Swal.fire({
      icon: 'error',
      title: '작성 실패',
      text: errorText,
      customClass: {
        popup: 'bg-white text-gray-900',
        icon: 'text-red-500',
        confirmButton: 'bg-red-400 text-white font-bold rounded px-4 py-2 mt-2 hover:bg-red-500'
      }
    })
  }
}

</script>
