<template>
  <div class="movie-container">
    <div class="movies-grid">
      <div v-for="movie in profileStore.likeMovies" :key="movie.movie_id" class="movie-card" @click="goMovie(movie.movie_id)">
        <img :src="`https://image.tmdb.org/t/p/original`+movie.poster_path" alt="movie poster" class="movie-poster" />
        <h2 class="movie-title">{{ movie.title }}</h2>
      </div>
    </div>
  </div>
</template>

<script setup>
import { useProfileStore } from '@/stores/profileStore'
import { computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'

const profileStore = useProfileStore()
const router = useRouter()

const goMovie = (movie_id) => {
  router.push({name: "movieDetail", params: {id : movie_id}})
}

</script>

<style scoped>
.movie-container {
  padding: 20px;
  max-width: 1200px;
  margin: 0 auto;
}

.movies-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
  gap: 20px;
}

.movie-card {
  background-color: #fff;
  border-radius: 10px;
  overflow: hidden;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  transition: transform 0.3s ease;
}

.movie-card:hover {
  transform: scale(1.05);
}

.movie-poster {
  width: 100%;
  height: auto;
}

.movie-title {
  padding: 10px;
  font-size: 16px;
  text-align: center;
}
</style>
