<template>
  <!-- 장르 옵션 추가 -->
  <div class="container">
    <div class="select-container">
      <select v-model="movieGenre" id="genre-select" class="genre-select">
        <option value=null>선택하세요</option>
        <option value="28">액션</option>
        <option value="12">모험</option>
        <option value="16">애니메이션</option>
        <option value="80">코미디</option>
        <option value="99">범죄</option>
        <option value="18">다큐멘터리</option>
        <option value="10751">드라마</option>
        <option value="14">판타지</option>
        <option value="36">역사</option>
        <option value="27">호러</option>
        <option value="10402">음악</option>
        <option value="9648">미스테리</option>
        <option value="10749">로맨스</option>
        <option value="878">과학픽션</option>
        <option value="10770">티비쇼</option>
        <option value="53">스릴러</option>
        <option value="10752">전쟁</option>
        <option value="37">서부</option>
      </select>
      <button @click="getMovies(value)" class="get-movies-btn">인기 영화 가져오기</button>
    </div>
  </div>

  <div class="text-white mt-4">
    <p class="fs-5">장르별 영화 리스트</p>
    <!-- Swiper -->
    <swiper :slides-per-view="5" :space-between="5" class="mySwiper d-flex">
      <swiper-slide v-for="movie in store.genreMovies" :key="movie.id" class="text-center">
        <div @click="goDetail(movie.id)">
          <img :src="`https://image.tmdb.org/t/p/w500${movie.poster_path}`" class="rounded-2"/>
          <p class="fs-5">{{ movie.title }}</p>
          <p class="fs-6">평점: {{ movie.vote_average.toFixed(1) }}</p>
        </div>
      </swiper-slide>
    </swiper>
  </div>
</template>

<script setup>
import { onMounted, ref } from 'vue';
import { useMovieStore } from '@/stores/movieStore';
import { Swiper, SwiperSlide } from 'swiper/vue';
import 'swiper/swiper-bundle.css';
import { useRouter } from 'vue-router'

const router = useRouter()
const store = useMovieStore();
const movies = ref([]);
const movieGenre = ref(null)

const goDetail = (movie_id) => {
  router.push({name: 'movieDetail', params: {id: movie_id}})
}

const getMovies = async () => {
  store.getPopularMoviesByGenre(movieGenre.value)
}

</script>

<style scoped>
.mySwiper .swiper-slide {
  display: flex;
  flex-direction: column;
  align-items: center;
}

.mySwiper img {
  width: 100%; /* 이미지의 너비를 100%로 설정 */
  height: auto; /* 높이를 자동으로 맞춤 */
  object-fit: cover; /* 이미지가 비율을 유지하면서 컨테이너에 꽉 차도록 합니다. */
}

.mySwiper h3, .mySwiper p {
  text-align: center; /* 텍스트를 가운데 정렬합니다. */
}

.container {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 20px;
}

.select-container {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 10px;
}

.genre-select {
  width: 200px;
  padding: 10px;
  border-radius: 5px;
  border: 1px solid #ccc;
}

.get-movies-btn {
  padding: 10px 20px;
  border: none;
  background-color: #007bff;
  color: white;
  border-radius: 5px;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

.get-movies-btn:hover {
  background-color: #0056b3;
}
</style>
