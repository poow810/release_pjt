<template>
  <div>
    <h1>
      리뷰 작성하기
    </h1>
    <hr>
    <form @submit.prevent="createReview">
      <label for="title">제목</label>
      <input type="text" v-model="title">
      <textarea v-model="content" name="review" id="" cols="150" rows="10">리뷰 작성란</textarea>
      <br>
      <label for="rating">별점 (0.0 ~ 5.0):</label>
      <input type="number" id="rating" v-model.number="rating" step="0.1" min="0" max="5">
      <br>
      <input type="submit">
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