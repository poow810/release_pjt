<template>
  <div class="d-flex justify-content-center">
    <div class="flex-column">
      <h1>날씨 기반 추천 영화</h1>
      <p>오늘의 날씨: <span :class="weatherIcon">{{ weather }}</span></p>
      <p v-if="movieRecommend && movieRecommend.genres">추천 장르: <span>{{ movieRecommend.genres.map(genre => genre).join(', ') }}</span></p> 
      <img v-if="movieRecommend && movieRecommend.recommend.poster_path" :src="`https://image.tmdb.org/t/p/original` + movieRecommend.recommend.poster_path" class="card-img-top" alt="...">
      <p v-if="movieRecommend && movieRecommend.recommend.title">{{ movieRecommend.recommend.title }}</p>
      <p v-if="movieRecommend && movieRecommend.recommend.overview">overview</p>
      <p v-if="movieRecommend && movieRecommend.recommend.overview">{{ movieRecommend.recommend.overview }}</p>
    </div>
  </div>
</template>

<script setup>
import axios from 'axios'
import { ref, onMounted } from 'vue'
import { useUserStore } from '@/stores/userStore';

const movieRecommend = ref(null) // 초기 상태를 null로 설정
const api_key = import.meta.env.VITE_OPENWEATHER_API_KEY
const weather = ref('')
const weatherIcon = ref('')
const store = useUserStore()

async function getWeather() {
  navigator.geolocation.getCurrentPosition(async position => {
    const latitude = position.coords.latitude
    const longitude = position.coords.longitude

    try {
      const response = await axios({
        method: 'GET',
        url: `https://api.openweathermap.org/data/2.5/weather?lat=${latitude}&lon=${longitude}&appid=${api_key}&lang=kr&units=metric`
      })

      const weatherData = response.data
      await recommendMovie(weatherData) // 비동기 호출을 기다림
    } catch (error) {
      console.log(error)
    }
  })
}

async function recommendMovie(weatherData) {
  const mainWeather = weatherData.weather[0].main;
  
  let weatherValue
  let weatherIconClass

  switch (mainWeather) {
    case 'Clear':
      weatherValue = '맑음'
      weatherIconClass = 'bi bi-brightness-low-fill'
      break
    case 'Clouds':
      weatherValue = '흐림'
      weatherIconClass = 'bi bi-cloud-fill'
      break
    case 'Rain':
      weatherValue = '비'
      weatherIconClass = 'bi bi-cloud-hail-fill'
      break
    default:
      weatherValue = mainWeather
      weatherIconClass = 'bi bi-cloud-sun-fill'
  }

  weather.value = weatherValue
  weatherIcon.value = weatherIconClass

  try {
    const response = await axios({
      method: 'GET',
      url: `https://pkpk.o-r.kr/movie/recommend/?weather=${weatherValue}`,
      headers: {
        Authorization: `Token ${store.token}`
      }
    })
    console.log(response.data)
    movieRecommend.value = response.data
  } catch (error) {
    console.log(error)
  }
}

onMounted(() => {
  getWeather()
})
</script>

<style scoped>
div.flex-column {
  color: #ffffff
}

img {
  width: 500px;
  height: 700px;
}
</style>
