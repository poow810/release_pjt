<template>
  <div>
    <h2>평점 순 영화 목록</h2>
    <ul>
      <li @click="movieDetail(movie.movie_id)" v-for="(movie, index) in moviesByRating" :key="'rating' + index">
        {{ movie.title }} - 평점: {{ movie.vote_avg }}
      </li>
    </ul>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { useRecomStore } from '@/stores/recomStore'
import { useRouter } from 'vue-router'

const router = useRouter()
const recomStore = useRecomStore()

const movieDetail = (movieId) => {
  router.push({ name: 'movieDetail', params: { id: movieId } })
}
const moviesByRating = computed(() => {
  return [...recomStore.userSetGenre].sort((a, b) => b.rating - a.rating)
})
</script>