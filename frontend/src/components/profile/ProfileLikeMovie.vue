<template>
  <div class="movie-container container mt-5">
    <div class="row">
      <div v-for="movie in profileStore.likeMovies" :key="movie.movie_id" class="col-md-3 mb-4">
        <div class="card movie-card h-100" @click="goMovie(movie.movie_id)">
          <img :src="`https://image.tmdb.org/t/p/original`+movie.poster_path" alt="movie poster" class="card-img-top movie-poster">
          <div class="card-body p-2">
            <h5 class="card-title movie-title text-center">{{ movie.title }}</h5>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { useProfileStore } from '@/stores/profileStore'
import { useRouter } from 'vue-router'

const profileStore = useProfileStore()
const router = useRouter()

const goMovie = (movie_id) => {
  router.push({name: "movieDetail", params: {id : movie_id}})
}
</script>

<style scoped>
body {
  background-color: #2C2C2C;
  color: #ffffff;
}

.movie-container {
  padding: 20px;
  max-width: 1200px;
  margin: 0 auto;
}

.movie-card {
  background-color: #2C2C2C;
  border: 1px solid #CCB15F;
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
  color: #CCB15F;
  padding: 10px;
  font-size: 16px;
  text-align: center;
}
</style>