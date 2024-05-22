<template>
  <div class="review-container">
    <div v-for="review in profileStore.reviews" :key="review.movie" class="review" @click="goMovie(review.movie_data.movie_id)">
      <img :src="`https://image.tmdb.org/t/p/original`+review.movie_data.poster_path" alt="영화 포스터" class="movie-poster" />
      <div class="movie-info">
        <h3>{{ review.movie_data.title }}</h3>
        <p>{{ review.title }}</p>
        <p>점수: {{ review.rating }}</p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { useProfileStore } from '@/stores/profileStore';
import { useRouter } from 'vue-router'

const router = useRouter()

const goMovie = (movie_id) => {
  router.push({name: 'movieDetail', params: {id: movie_id}})
}


const profileStore = useProfileStore()
</script>

<style scoped>
.review-container {
  display: flex;
  flex-wrap: wrap;
  gap: 20px;
}

.review {
  display: flex;
  align-items: center;
  gap: 15px;
}

.movie-poster {
  width: 100px;
  height: 150px;
  object-fit: cover;
}

.movie-info h3,
.movie-info p {
  margin: 0;
}

.movie-info h3 {
  font-size: 20px;
  margin-bottom: 5px;
}

.movie-info p {
  font-size: 16px;
  color: #666;
}
</style>
