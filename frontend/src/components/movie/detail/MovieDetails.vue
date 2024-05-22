<template>
  <div v-if="Object.keys(movieStore.detailMovies).length">
    <h1>{{ movieStore.detailMovies.title }}</h1>
    <div v-if="isLiked"><button @click="toggleLike">좋아요 취소</button></div>
    <div v-else><button @click="toggleLike">좋아요</button></div>
    <p>좋아요 개수: {{ movieStore.detailMovies.liked_count }}</p>
    <img :src="`https://image.tmdb.org/t/p/original`+movieStore.detailMovies.poster_path" alt="Movie Poster">
    <p>{{ movieStore.detailMovies.overview }}</p>
    <p>Release Date: {{ movieStore.detailMovies.release_date }}</p>
    <p>Popularity: {{ movieStore.detailMovies.popularity }}</p>
    <p>Average Vote: {{ movieStore.detailMovies.vote_avg }}</p>
    <h3>리뷰</h3>
    <MovieReview :movieId="movieId" />
    <hr>
    <h3>리뷰 작성하기</h3>
    <router-link :to="{name:'review', params: {id: movieId}}">작성 하기</router-link>
    <router-view />
  </div>
  <div v-else>
    <p>로딩 중...</p>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useMovieStore } from '@/stores/movieStore'
import { useUserStore } from '@/stores/userStore'
import MovieReview from '@/components/movie/detail/MovieReview.vue'

const { movieId } = defineProps({
  movieId: String,
})

const movieStore = useMovieStore()
const userStore = useUserStore()
const isLiked = ref(false)

const toggleLike = async () => {
  const likeData = await movieStore.movieLike(movieId); // movieLike 함수의 반환값을 받습니다.
  if (likeData) { // 정상적으로 데이터를 받았을 경우
    isLiked.value = likeData.is_liked; // 좋아요 상태 업데이트
    movieStore.detailMovies.liked_count = likeData.like_count; // 좋아요 개수 업데이트
  }
}

onMounted(async () => {
  console.log('영화 상세 정보 로드 시작');
  await movieStore.movieDetail(movieId);
  console.log('영화 상세 정보 로드 완료');
  isLiked.value = movieStore.detailMovies.is_liked;
})
</script>
