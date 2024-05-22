<template>
  <hr class="text-white">
  <div class="text-white mt-4">
    <p class="fs-3 text-center">평점 순 영화 목록</p>
    
    <swiper :slides-per-view="5" :space-between="5" class="mySwiper" :autoplay="{ delay: 3000, disableOnInteration: false }" loop>
      <swiper-slide @click="movieDetail(movie.movie_id)" v-for="(movie, index) in moviesByRating" :key="'rating' + index">
        <div class="movie-item">
          <img :src="`https://image.tmdb.org/t/p/w500${movie.poster_path}`" class="rounded-2" />
        </div>
        <p class="fs-4">
          {{ movie.title }}
        </p>
        <p class="fs-5">
          평점: {{ movie.vote_avg }}
        </p>
      </swiper-slide>
    </swiper>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { useRecomStore } from '@/stores/recomStore'
import { useRouter } from 'vue-router'
import { Swiper, SwiperSlide } from 'swiper/vue';
import 'swiper/swiper-bundle.css';

const router = useRouter()
const recomStore = useRecomStore()

const movieDetail = (movieId) => {
  router.push({ name: 'movieDetail', params: { id: movieId } })
}
const moviesByRating = computed(() => {
  return [...recomStore.userSetGenre].sort((a, b) => b.rating - a.rating)
})
</script>

<style scoped>
.mySwiper .swiper-slide {
  display: flex;
  flex-direction: column;
  align-items: center;
}

.mySwiper .movie-item {
  width: 100%;
  margin: auto;
}

.mySwiper img {
  width: 100%;
  object-fit: cover;
}

.mySwiper p {
  text-align: center;
}</style>