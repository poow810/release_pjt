<template>
    <div>
        <div v-if="!movieStore.searchMovies.length">
            <h3>검색된 데이터가 없습니다.</h3>
        </div>
        <div v-else>
            <MovieSearchList 
            v-for="searchMovie in movieStore.searchMovies"
            :key="searchMovie.id"
            :searchMovie="searchMovie"
            />
        </div>

    </div>
</template>

<script setup>
import { useMovieStore } from '@/stores/movieStore'
import MovieSearchList from '@/components/movie/MovieSearchList.vue'


const movieStore = useMovieStore()

</script>