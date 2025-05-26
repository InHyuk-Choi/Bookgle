<template>
  <div class="max-w-3xl mx-auto px-4 sm:px-6 mt-[100px] pb-20">

    <!-- 책 정보 카드 -->
    <div class="bg-white rounded-2xl shadow-md border border-gray-100 p-6 mb-10">
    <div class="flex gap-6 justify-between">
        <!-- 표지 이미지 -->
        <img
        :src="book.cover_image || '/default-cover.png'"
        alt="cover"
        class="w-28 h-auto rounded-xl border object-contain"
        />

        <!-- 제목, 설명, 별점 포함 -->
        <div class="flex flex-col justify-between flex-1">
        <!-- 책 정보 -->
        <div>
            <h2 class="text-xl sm:text-2xl font-bold text-gray-800 mb-1 leading-snug">
            {{ book.title }}
            </h2>
            <p class="text-sm text-gray-500 mb-4">
            {{ book.author }} · {{ book.publisher }}
            </p>
            <p class="text-gray-700 text-sm leading-relaxed whitespace-pre-line">
            {{ book.description }}
            </p>
        </div>

        <!-- 평균 별점 -->
        <div
            v-if="averageRating !== null"
            class="self-end mt-4 text-sm text-gray-700 flex items-center gap-1"
        >
            <svg class="w-4 h-4 text-yellow-400 fill-current" viewBox="0 0 20 20">
            <path
                d="M10 15l-5.878 3.09 1.122-6.545L.488 6.91l6.562-.955L10 0l2.95 5.955 
                6.562.955-4.756 4.635 1.122 6.545z"
            />
            </svg>
            평균 {{ averageRating.toFixed(1) }}점
        </div>
        </div>
    </div>

    <!-- 평균 별점 -->
    <div
    v-if="averageRating !== null"
    class="absolute -bottom-3 right-6 mt-2 text-sm text-gray-700 flex items-center gap-1"
    >
    <svg class="w-4 h-4 text-yellow-400 fill-current" viewBox="0 0 20 20">
        <path
        d="M10 15l-5.878 3.09 1.122-6.545L.488 6.91l6.562-.955L10 0l2.95 5.955 
        6.562.955-4.756 4.635 1.122 6.545z"
        />
    </svg>
    평균 {{ averageRating.toFixed(1) }}점
    </div>
    </div>


    <!-- 리뷰 작성 폼 (테스트용) -->
    <div class="mt-10">
      <ReviewForm :isbn="isbn" @refresh="fetchBookDetail" />
    </div>

    <!-- 사용자 리뷰 -->
    <div class="border-t border-gray-200 pt-10 mt-14">
      <ReviewList :reviews="reviews" />
    </div>
  </div>
</template>

<script setup>
import { onMounted, ref, computed } from 'vue'
import axios from 'axios'
import { useRoute } from 'vue-router'

import ReviewForm from '@/components/ReviewForm.vue'
import ReviewList from '@/components/ReviewList.vue'

const route = useRoute()
const isbn = route.params.isbn

const book = ref({})
const reviews = ref([])

const averageRating = computed(() => {
  if (reviews.value.length === 0) return null
  const total = reviews.value.reduce((sum, review) => sum + review.rating, 0)
  return total / reviews.value.length
})

const fetchBookDetail = async () => {
  try {
    const res = await axios.get(`http://localhost:8000/api/v1/kkubook/books/${isbn}/`, {
      params: {
        title: route.query.title,
        author: route.query.author,
        publisher: route.query.publisher,
        cover_image: route.query.cover_image,
        description: route.query.description,
      },
    })
    book.value = res.data.book
    reviews.value = res.data.reviews
  } catch (err) {
    console.error(err)
  }
}

onMounted(fetchBookDetail)
</script>