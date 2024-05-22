<template>
  <div v-if="movieStore.detailMovies">
    <h1>{{ movieStore.detailMovies.title }}</h1>
    <div v-if="movieStore.isLiked"><button @click="movieLike">좋아요 취소</button></div>
    <div v-else><button @click="movieLike">좋아요</button></div>
    <p>좋아요 개수: {{ movieStore.likeCount }}</p>
    <img :src="`https://image.tmdb.org/t/p/original`+movieStore.detailMovies.poster_path" alt="Movie Poster">
    <p>{{ movieStore.detailMovies.overview }}</p>
    <p>Release Date: {{ movieStore.detailMovies.release_date }}</p>
    <p>Popularity: {{ movieStore.detailMovies.popularity }}</p>
    <p>Average Vote: {{ movieStore.detailMovies.vote_avg }}</p>
    <h3>리뷰</h3>
    <MovieReview 
    :movieId="movieId"
    />
    <hr>
    <h3>리뷰 작성하기</h3>
    <router-link :to="{name:'review', params: {id: movieId}}">작성 하기</router-link>
    <router-view />
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'
import { useRecomStore } from '@/stores/recomStore.js'
import { useMovieStore } from '@/stores/movieStore'
import { useUserStore } from '@/stores/userStore'
import MovieReview from '@/components/movie/detail/MovieReview.vue'

const { movieId } = defineProps({
  movieId: String,
})

const useStore = useUserStore()
const recomStore = useRecomStore()
const movieStore = useMovieStore()
const movie = ref(null)

const movieLike = () => {
  movieStore.movieLike(movieId)
}

onMounted(() => {
  movieStore.movieDetail(movieId)
})
</script>
