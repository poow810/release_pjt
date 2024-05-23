<template>
  <div class="review-page d-flex justify-content-center align-items-center">
    <div class="review-container">
      <div>
        <p class="fs-3 text-white text-center m-3">리뷰 상세페이지</p>
      </div>
      <div class="d-flex align-items-center mb-3">
        <img :src="images[movieStore.detailReviews?.user_image || 0]" alt="User Image" class="user-image me-3">
        <p class="user-nickname mb-0">{{ movieStore.detailReviews?.user.nickname }}</p>
      </div>
      <div class="mb-3">
        <p class="review-title">제목</p>
        <p class="review-title-content p-2">{{ movieStore.detailReviews?.title }}</p>
      </div>
      <div class="mb-3">
        <p class="review-content-title">내용</p>
        <p class="review-content p-2 ptt">{{ movieStore.detailReviews?.content }}</p>
      </div>
      <p class="review-rating">평점❤: {{ movieStore.detailReviews?.rating }}</p>
    </div>
  </div>
</template>

<style scoped>
.review-page {
  padding: 20px;
  min-height: 100vh;
  background-color: #1b1b1b;
}

.review-container {
  background-color: #2c2c2c;
  padding: 20px;
  border-radius: 8px;
  border: 1px solid #CCB15F;
  width: 100%;
  max-width: 600px;
}

.user-image {
  width: 50px;
  height: 50px;
  border-radius: 50%;
  object-fit: cover;
}

.user-nickname, .review-title, .review-content-title, .review-rating {
  color: white;
}

.review-title, .review-rating {
  color: white;
}

.review-title-content, .review-content {
  border: solid 1px #CCB15F;
  border-radius: 10px;
  
  padding: 10px;
  color: white;
  transition: background-color 0.3s, color 0.3s;
}

.ptt {
  min-height: 120px;
}
.review-title-content:hover, .review-content:hover {
  background-color: white;
  color: #1b1b1b;
}
</style>

<script setup>
import { useRoute } from 'vue-router'
import { ref, onMounted } from 'vue'
import axios from 'axios';
import noimage from '@/assets/static/noimage.png'
import image1 from '@/assets/static/cinnamoroll.png'
import image2 from '@/assets/static/kitty.png'
import image3 from '@/assets/static/kuromi.png'
import image4 from '@/assets/static/mymelody.png'
import image5 from '@/assets/static/pompompurin.png'
import { useMovieStore } from '@/stores/movieStore';

const images = [noimage, image1, image2, image3, image4, image5]
const route = useRoute()
const review_id = ref(route.params.review_id)
const movieStore = useMovieStore()

onMounted(() => {
  movieStore.getDetailReview(review_id.value)
})
</script>
