<template>
  <div class="review-form-container container mt-5">
    <h1 class="form-title">리뷰 작성하기</h1>
    <hr class="divider">
    <form @submit.prevent="createReview" class="form-group">
      <div class="mb-3">
        <label for="title" class="form-label">제목</label>
        <input type="text" v-model="title" class="form-control" id="title" required>
      </div>
      <div class="mb-3">
        <label for="content" class="form-label">리뷰</label>
        <textarea v-model="content" class="form-control" id="content" rows="5" required></textarea>
      </div>
      <div class="mb-3">
        <label for="rating" class="form-label">별점 (⭐5):</label>
        <input type="number" v-model.number="rating" class="form-control" id="rating" step="0.1" min="0" max="5" required>
      </div>
      <button type="submit" class="btn btn-outline-warning">제출</button>
    </form>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRoute } from 'vue-router'
import { useMovieStore } from '@/stores/movieStore';  

const content = ref('')
const route = useRoute()
const movieStore = useMovieStore()
const rating = ref(0)
const title = ref('')

const movieId = route.params.id
const createReview = () => {
  const reviewData = {
    title: title.value,
    content: content.value,
    rating: rating.value,
  }
  movieStore.createReview(movieId, reviewData)
  title.value = ''
  content.value = ''
  rating.value = 0
}
</script>

<style scoped>
.review-form-container {
  background-color: #2C2C2C;
  color: #FFFFFF;
  padding: 20px;
  border-radius: 10px;
}

.form-title {
  color: #CCB15F;
}

.divider {
  border-top: 1px solid #CCB15F;
}

.form-label {
  color: #FFFFFF;
}

.form-control {
  background-color: #2C2C2C;
  color: #FFFFFF;
  border: 1px solid #CCB15F;
}

.form-control:focus {
  background-color: #2C2C2C;
  color: #FFFFFF;
  border-color: #CCB15F;
  box-shadow: 0 0 0 0.2rem rgba(204, 177, 95, 0.25);
}

.btn-outline-warning {
  color: #CCB15F;
  border-color: #CCB15F;
}

.btn-outline-warning:hover {
  background-color: #CCB15F;
  color: #2C2C2C;
  border-color: #CCB15F;
}
</style>