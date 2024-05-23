<template>
    <div class="container mt-5">
        <div v-if="!movieStore.searchMovies.length" class="p-5 text-center text-warning">
            <h3 class="fs-1 text-center text-danger">검색된 데이터가 없습니다.</h3>
        </div>
        <p class="fs-3 text-center" style="color: white; font-weight: 700;">Search Movie✔</p>
        <div v-if="type=='영화'">
            <swiper
                :slides-per-view="1"
                :space-between="30"
                class="mb-5"
            >
                <swiper-slide v-for="searchMovie in movieStore.searchMovies" :key="searchMovie.id">
                    <MovieSearchList :searchMovie="searchMovie" class="card-custom" />
                </swiper-slide>
            </swiper>
            <hr class="border-warning">
            <br>
            <p class="fs-3 text-center" style="color: white; font-weight: 700;">이런 영화는 어떠신가요?</p>
            <swiper
                :slides-per-view="3"
                :space-between="30"
                pagination
                loop
            >
                <swiper-slide v-for="searchMovie in movieStore.searchMovies" :key="searchMovie.id">
                    <MovieSearchList :searchMovie="searchMovie" class="card-custom" />
                </swiper-slide>
            </swiper>
        </div>
        <div v-else>
            <swiper
                :slides-per-view="1"
                :space-between="30"
                class="mb-5"
            >
                <swiper-slide v-for="searchMovie in movieStore.searchMovies" :key="searchMovie.id">
                    <MovieSearchActor :searchMovie="searchMovie" :actor_id="searchMovie.id" class="card-custom" />
                </swiper-slide>
            </swiper>
            <hr class="border-warning">
            <br>
            <p class="fs-3 text-center" style="color: white; font-weight: 700;">이런 영화는 어떠신가요?</p>
            <swiper
                :slides-per-view="3"
                :space-between="30"
                pagination
                loop
            >
                <swiper-slide v-for="searchMovie in movieStore.searchMovies" :key="searchMovie.id">
                    <MovieSearchActor :searchMovie="searchMovie" :actor_id="searchMovie.id" class="card-custom" />
                </swiper-slide>
            </swiper>
        </div>
    </div>
</template>

<script setup>
import { onMounted } from 'vue'
import { useMovieStore } from '@/stores/movieStore';
import MovieSearchList from '@/components/movie/MovieSearchList.vue';
import MovieSearchActor from '@/components/movie/MovieSearchActor.vue';
import { Swiper, SwiperSlide } from 'swiper/vue';
import 'swiper/swiper-bundle.css';

const movieStore = useMovieStore();

onMounted(() => {
    console.log(movieStore.searchMovies)
})
</script>
<style scoped>
/* 원하는 추가 스타일을 여기에 추가할 수 있습니다 */
.swiper {
    width: 100%;
    height: 100%;
}
.swiper-slide {
    display: flex;
    justify-content: center;
    align-items: center;
}

.card-custom {
    width: 1000px; /* 카드의 너비를 일정하게 설정 */
    background-color: #1b1b1b;
    border: 2px solid #CCB15F;
    padding: 20px;
    border-radius: 10px;
    color: wheat;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    align-items: center;
}

.text-warning {
    color: #CCB15F !important;
}

.border-warning {
    border-color: #CCB15F !important;
}
</style>