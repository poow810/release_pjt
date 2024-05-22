<template>
  <div class="container review-container mt-5">
    <div class="row">
      <div v-for="review in profileStore.reviews" :key="review.movie" class="col-md-4 mb-4">
        <div class="card review h-100" @click="goMovie(review.movie_data.movie_id)">
          <img :src="`https://image.tmdb.org/t/p/original`+review.movie_data.poster_path" alt="영화 포스터" class="card-img-top movie-poster" />
          <div class="card-body movie-info">
            <h3 class="card-title">{{ review.movie_data.title }}</h3>
            <p class="card-text">{{ review.title }}</p>
            <p class="card-text">점수: {{ review.rating }}</p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { useProfileStore } from '@/stores/profileStore';
import { useRouter } from 'vue-router';

const router = useRouter();

const goMovie = (movie_id) => {
  router.push({ name: 'movieDetail', params: { id: movie_id } });
};

const profileStore = useProfileStore();
</script>

<style scoped>
body {
  background-color: #2C2C2C;
  color: #ffffff;
}

.review-container {
  padding: 20px;
}

.review {
  background-color: #2C2C2C;
  border: 1px solid #CCB15F;
  border-radius: 12px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  transition: transform 0.3s ease, box-shadow 0.3s ease;
  cursor: pointer;
}

.review:hover {
  transform: translateY(-10px);
  box-shadow: 0 8px 16px rgba(0, 0, 0, 0.2);
}

.movie-poster {
  width: 100%;
  height: 300px;
  object-fit: cover;
  border-bottom: 1px solid #CCB15F;
}

.movie-info {
  padding: 15px;
}

.movie-info h3 {
  color: #CCB15F;
  font-size: 20px;
  margin-bottom: 5px;
}

.movie-info p {
  color: #ffffff;
  font-size: 16px;
  margin: 0;
}

.card-text {
  color: #CCB15F;
}

@media (max-width: 600px) {
  .review {
    width: 100%;
  }
}
</style>