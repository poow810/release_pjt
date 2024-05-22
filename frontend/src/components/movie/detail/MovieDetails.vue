<template>
  <div v-if="Object.keys(movieStore.detailMovies).length" class="movie-detail-container container mt-5">
    <div class="text-center">
      <h1 class="movie-title">{{ movieStore.detailMovies.title }}</h1>
      <div v-if="isLiked">
        <button @click="toggleLike" class="btn btn-outline-warning my-2 text">좋아요 취소</button>
      </div>
      <div v-else>
        <button @click="toggleLike" class="btn btn-outline-warning my-2">좋아요❤️</button>
      </div>
      <p class="liked-count fs-2">좋아요 개수: {{ movieStore.detailMovies.liked_count }}</p>
    </div>
    <img :src="`https://image.tmdb.org/t/p/original` + movieStore.detailMovies.poster_path" alt="Movie Poster" class="movie-poster img-fluid my-3">
    <p class="movie-overview">{{ movieStore.detailMovies.overview }}</p>

    <!-- 개봉일자, 인기도, 평점 -->
    <div class="d-flex justify-content-around">
      <p class="movie-detail text-secondary">Release Date</p>
      <p class="movie-detail text-secondary">Popularity</p>
      <p class="movie-detail text-secondary">Average Vote</p>
    </div>
    <div class="d-flex justify-content-around fs-2">
      <p class="movie-detail">{{ movieStore.detailMovies.release_date }}</p>
      <p class="movie-detail">{{ movieStore.detailMovies.popularity }}</p>
      <p class="movie-detail">{{ movieStore.detailMovies.vote_avg }}</p>
    </div>
    <hr>
    <!-- 리뷰 -->
    <h3 class="reviews-title">리뷰</h3>
    <MovieReview :movieId="movieId" />
    <hr class="divider">
    <router-link :to="{ name: 'review', params: { id: movieId } }" class="btn btn-outline-warning my-2">리뷰작성 하러가기</router-link>
    <router-view />
  </div>
  <div v-else>
    <p class="loading-text">로딩 중...</p>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { useMovieStore } from '@/stores/movieStore';
import { useUserStore } from '@/stores/userStore';
import MovieReview from '@/components/movie/detail/MovieReview.vue';

const { movieId } = defineProps({
  movieId: String,
});

const movieStore = useMovieStore();
const userStore = useUserStore();
const isLiked = ref(false);

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
});
</script>

<style scoped>
.movie-detail-container {
  background-color: #2C2C2C;
  border: solid #CCB15F 1px;
  color: #FFFFFF;
  padding: 20px;
  border-radius: 10px;
  padding: 30px;
}

.movie-title {
  color: #CCB15F;
}

.movie-poster {
  border-radius: 10px;
}

.movie-overview, .movie-detail, .liked-count {
  color: #FFFFFF;
  font-weight: bold;
}
.loading-text {
  color: #FFFFFF;
  text-align: center;
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

.divider {
  border-top: 1px solid #CCB15F;
}

.movie-detail {
  color: #CCB15F;
  font-weight: bold;
  width: 200px;
  text-align: center
}

</style>