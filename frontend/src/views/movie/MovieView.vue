<template>
  <div>
    <h3>영화 상세 페이지</h3>
    <MovieDetails 
    :movieId="movieId"
    />
  </div>
</template>

<script setup>
import MovieDetails from "@/components/movie/detail/MovieDetails.vue"
import { useRoute } from "vue-router"

const route = useRoute()
const movieId = route.params.id

</script>