<template>
  <!-- 장르 옵션 추가 -->
  <select id="genre-select">
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
  <button id="fetch-movies">인기 영화 가져오기</button>

  <div class="text-white mt-4">
    <p class="fs-5">장르별 영화 리스트</p>
    <!-- Swiper -->
    <swiper :slides-per-view="5" :space-between="5" class="mySwiper d-flex">
      <swiper-slide v-for="movie in movies" :key="movie.id" class="text-center">
        <img :src="`https://image.tmdb.org/t/p/w500${movie.poster_path}`" class="rounded-2"/>
        <p class="fs-5">{{ movie.title }}</p>
        <p class="fs-6">평점: {{ movie.vote_average.toFixed(1) }}</p>
      </swiper-slide>
    </swiper>
  </div>
</template>

<script setup>
import { onMounted, ref } from 'vue';
import { useMovieStore } from '@/stores/movieStore';
import { Swiper, SwiperSlide } from 'swiper/vue';
import 'swiper/swiper-bundle.css';

const store = useMovieStore();
const movies = ref([]);

onMounted(async () => {
  await store.getGenreList(); // 장르 목록 먼저 가져오기

  // 예시: 첫 번째 장르의 ID로 인기 영화 가져오기
  if (store.genreMovies.genres && store.genreMovies.genres.length > 0) {
    const genreId = store.genreMovies.genres[0].id;
    await store.getPopularMoviesByGenre(genreId); // 장르별 인기 영화 가져오기
    movies.value = store.genreMovies; // 가져온 영화 목록을 movies에 할당
  }

  // DOM이 완전히 로드된 후에 이벤트 리스너 추가
  document.getElementById('fetch-movies').addEventListener('click', () => {
    const selectedGenre = document.getElementById('genre-select').value;
    getPopularMoviesByGenre(selectedGenre); // 선택된 장르의 ID를 함수에 전달
  });
});

// 인기영화목록 가져오기
async function getPopularMoviesByGenre(genreId) {
  const apiKey = import.meta.env.VITE_TMDB_API_KEY; // 실제 API 키로 대체
  const url = `https://api.themoviedb.org/3/discover/movie?api_key=${apiKey}&with_genres=${genreId}`;

  try {
    const response = await fetch(url);
    const data = await response.json();
    movies.value = data.results; // 가져온 영화 목록을 movies에 할당
  } catch (error) {
    console.error('영화 목록을 가져오는 데 실패했습니다:', error);
  }
}
</script>

<style scoped>
.mySwiper .swiper-slide {
  flex-direction: column;
  align-items: center;
}

.mySwiper img {
  width: 200px; /* 이미지의 너비를 150px로 설정 */
  height: auto; /* 높이를 자동으로 맞춤 */
  object-fit: cover; /* 이미지가 비율을 유지하면서 컨테이너에 꽉 차도록 합니다. */
}

.mySwiper h3, .mySwiper p {
  text-align: center; /* 텍스트를 가운데 정렬합니다. */
}
</style>