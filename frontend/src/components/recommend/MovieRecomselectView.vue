<template>
  <div>
    <div class="d-flex genre-selection m-5 justify-content-center">
      <div v-for="genre in selectGenres" :key="genre.id" class="genre-item" @click="toggleSelect(genre.id)">
        <img :src="genre.image" :alt="genre.name" class="genre-image rounded-circle" :class="{'selected': select.includes(genre.id)}">
        <p class="text-center">{{ genre.name }}</p>
      </div>
    </div>
    <div class="row">
      <div class="col text-center">
        <button class="btn btn-secondary btn-lg" @click="submitSelect">완료</button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { onMounted, ref } from 'vue'
import { useRecomStore } from '@/stores/recomStore'
import actionImage from '@/assets/genres/action.jpg'
import adventureImage from '@/assets/genres/adventure.jpg'
import animationImage from '@/assets/genres/animation.jpg'
import comedyImage from '@/assets/genres/comedy.jpg'
import crimeImage from '@/assets/genres/crime.jpg'
import documentaryImage from '@/assets/genres/documentary.jpg'
import dramaImage from '@/assets/genres/drama.jpg'
import familyImage from '@/assets/genres/family.jpg'
import fantasyImage from '@/assets/genres/fantasy.jpg'
import historyImage from '@/assets/genres/history.jpg'
import horrorImage from '@/assets/genres/horror.jpg'
import musicImage from '@/assets/genres/music.jpg'
import mysteryImage from '@/assets/genres/mystery.jpg'
import romanceImage from '@/assets/genres/romance.jpg'
import scienceFictionImage from '@/assets/genres/science-fiction.jpg'
import tvMovieImage from '@/assets/genres/tv-movie.jpg'
import thrillerImage from '@/assets/genres/thriller.jpg'
import warImage from '@/assets/genres/war.jpg'
import westernImage from '@/assets/genres/western.jpg'

const store = useRecomStore()

// 선택된 장르들을 관리할 ref
const select = ref([])
const selectGenres = [
  { id: 28, name: "Action", image: actionImage },
  { id: 12, name: "Adventure", image: adventureImage },
  { id: 16, name: "Animation", image: animationImage },
  { id: 35, name: "Comedy", image: comedyImage },
  { id: 80, name: "Crime", image: crimeImage },
  { id: 99, name: "Documentary", image: documentaryImage },
  { id: 18, name: "Drama", image: dramaImage },
  { id: 10751, name: "Family", image: familyImage },
  { id: 14, name: "Fantasy", image: fantasyImage },
  { id: 36, name: "History", image: historyImage },
  { id: 27, name: "Horror", image: horrorImage },
  { id: 10402, name: "Music", image: musicImage },
  { id: 9648, name: "Mystery", image: mysteryImage },
  { id: 10749, name: "Romance", image: romanceImage },
  { id: 878, name: "Science Fiction", image: scienceFictionImage },
  { id: 10770, name: "TV Movie", image: tvMovieImage },
  { id: 53, name: "Thriller", image: thrillerImage },
  { id: 10752, name: "War", image: warImage },
  { id: 37, name: "Western", image: westernImage }
];
const genreSelect = selectGenres.id

// 장르 선택 및 선택 해제 토글
const toggleSelect = (genreId) => {
  const index = select.value.indexOf(genreId);
  if (index > -1) {
    // 이미 선택된 장르 해제
    select.value.splice(index, 1);
  } else {
    // 장르 선택
    select.value.push(genreId);
  }
}

// 선택된 장르 서버로 전송
const submitSelect = () => {
  if (select.value.length >= 2) {
    store.getGenreToServer(select.value)
  } else {
    alert("두 개 이상의 장르를 선택해주세요!")
  }
}


</script>

<style scoped>

.genre-selection {
  display: flex;
  flex-wrap: wrap;
}
.genre-item {
  cursor: pointer;
  margin: 10px;
  color: #ffffff;
}
.genre-image {
  width: 100px; /* 이미지 크기 조절 */
  height: 100px;
  object-fit: cover;
}
.genre-image.selected {
  border: 2px solid orange; /* 선택된 항목 표시 */
}

</style>