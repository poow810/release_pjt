<template>
  <div>
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