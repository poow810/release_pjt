<template>
  <div class="container-fluid p-0">
    <div class="ratio ratio-16x9">
      <iframe class="embed-responsive-item" 
        :src="`https://www.youtube.com/embed/${videoId}?autoplay=1&mute=1&fit=cover`" frameborder="0"
        allowfullscreen>
      </iframe>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { useMovieStore } from '@/stores/movieStore'
import axios from 'axios';

const movieStore = useMovieStore()
const videoId = ref(null);
const latestMovieTitle = ref('');

onMounted(async () => {
  const apiKey = movieStore.API_KEY;
  try {
    // 최신 영화 정보 가져오기
    let response = await axios.get(`https://api.themoviedb.org/3/movie/now_playing?api_key=${apiKey}&language=en-US&page=1`);
    if (response.data.results.length > 0) {
      const movieTitle = response.data.results[0].title;
      latestMovieTitle.value = movieTitle; // 최신 영화 제목 설정
      const movieId = response.data.results[0].id;      
      // 영화의 비디오 정보 가져오기
      response = await axios.get(`https://api.themoviedb.org/3/movie/${movieId}/videos?api_key=${apiKey}&language=en-US`);
      const trailers = response.data.results.filter(v => v.site === "YouTube" && v.type === "Trailer");
      if (trailers.length > 0) {
        videoId.value = trailers[0].key; // YouTube 트레일러 ID 설정
      }
    }
  } catch (error) {
    console.error("Error fetching movie trailer:", error);
  }
});
</script>

<style scoped>
</style>
