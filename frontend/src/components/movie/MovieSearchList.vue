<template>
    <div @click="goDetail(searchMovie.id)" class="card-content">
        <img :src="posterUrl" alt="poster" class="poster-image">
        <p class="fs-2 mt-2">{{ searchMovie.title }}</p>
        <p class="text-white">{{ searchMovie.overview }}</p>
    </div>
</template>

<script setup>
import { ref } from 'vue';
import { useRouter } from 'vue-router'

const router = useRouter()
const props = defineProps({
    searchMovie: Object
});

const goDetail = (movie_id) => {
    router.push({name: 'movieDetail', params: {id: movie_id}})
}

const posterUrl = ref(`https://image.tmdb.org/t/p/w500${props.searchMovie.poster_path}`);
</script>

<style scoped>
.poster-image {
    width: 100%;
    height: auto;
    border-radius: 10px;
    margin-bottom: 15px;
}

.card-content {
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    align-items: center;
    text-align: center;
}
</style>