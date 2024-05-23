<script setup>
import noimage from '@/assets/static/noimage.png'
import image1 from '@/assets/static/cinnamoroll.png'
import image2 from '@/assets/static/kitty.png'
import image3 from '@/assets/static/kuromi.png'
import image4 from '@/assets/static/mymelody.png'
import image5 from '@/assets/static/pompompurin.png'
const images = [noimage, image1, image2, image3, image4, image5]

import { computed, ref, onMounted, watch } from 'vue'
import { RouterLink, RouterView } from 'vue-router'
import { useUserStore } from '@/stores/userStore'
import { useMovieStore } from '@/stores/movieStore'
import { useProfileStore } from '@/stores/profileStore'

const profileStore = useProfileStore()
const userStore = useUserStore()
const movieStore = useMovieStore()

const searchText = ref('')
const selectType = ref('')

const id = computed(() => userStore.userInfo)

const searchMovie = () => {
  movieStore.searchMovie(selectType.value, searchText.value)
  searchText.value = ''
}

const logOut = () => {
  userStore.logOut()
}

onMounted(async () => {
  if (userStore.isLogIn) {
    await profileStore.getProfile(userStore.userInfo.id)
  }
  console.log(userStore.isLogIn)
})

watch(() => userStore.userInfo, async (newId) => {
  if (newId && userStore.isLogIn) {
    await profileStore.getProfile(newId)
  }
}, {deep:true})
</script>

<template>
  <nav class="navbar navbar-expand-lg" style="background-color: #1b1b1b;">
    <div class="container-fluid">
      <RouterLink class="navbar-brand text-white fs-1" style="font-weight: 700;" to="/">PK=PK</RouterLink>
      <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarSupportedContent" aria-controls="navbarSupportedContent" aria-expanded="false" aria-label="Toggle navigation">
        <span class="navbar-toggler-icon"></span>
      </button>
      <div class="collapse navbar-collapse" id="navbarSupportedContent">
        <ul class="navbar-nav me-auto mb-2 mb-lg-0">
          <li class="nav-item">
            <RouterLink class="nav-link text-white" :to="{ name: 'community' }">커뮤니티</RouterLink>
          </li>
          <li class="nav-item dropdown">
            <a class="nav-link dropdown-toggle text-white" href="#" id="navbarDropdown" role="button" data-bs-toggle="dropdown" aria-expanded="false">
              추천 알고리즘
            </a>
            <ul class="dropdown-menu" aria-labelledby="navbarDropdown">
              <li><RouterLink class="dropdown-item text-white" :to="{ name: 'recommend' }">영화추천</RouterLink></li>
              <li><RouterLink class="dropdown-item text-white" :to="{ name: 'weather' }">날씨추천</RouterLink></li>
              <li><hr class="dropdown-divider text-white"></li>
              <li><RouterLink class="dropdown-item text-white" href="#">Something else here</RouterLink></li>
            </ul>
          </li>
          <li class="nav-item"></li>
        </ul>
        <ul class="navbar-nav ms-auto mb-2 mb-lg-0">
          <div class="d-flex">
            <select class="form-select me-2" v-model="selectType">
              <option disabled value="">선택하세요</option>
              <option value="영화">영화</option>
              <option value="이름">이름</option>
            </select>
            <input type="text" class="form-control me-2 other" placeholder="영화를 입력해주세요 :)" aria-label="Input group example" aria-describedby="basic-addon1" v-model="searchText" @keypress.enter="searchMovie">
            <button class="btn btn-outline-success other text-white" id="basic-addon1" @click="searchMovie">Search</button>
          </div>
          <li class="nav-item">
            <RouterLink v-if="!userStore.userInfo" class="nav-link text-white" :to="{ name: 'signup' }">회원가입</RouterLink>
          </li>
          <li class="nav-item">
            <RouterLink v-if="!userStore.userInfo" class="nav-link text-white" :to="{ name: 'login' }">로그인</RouterLink>
          </li>
          <li v-if="userStore.userInfo" class="nav-item">
            <RouterLink class="nav-link text-white" :to="{ name: 'profile', params: { id: userStore.userInfo.id }}">
              <img :src="images[userStore.userInfo.user_image]" alt="프로필 이미지" style="width: 50px; height: 50px;">
            </RouterLink>
          </li>
          <li v-if="userStore.userInfo" class="nav-item">
            <button class="btn btn-outline-success other text-white" @click="logOut">로그아웃</button>
          </li>
        </ul>
      </div>
    </div>
  </nav>
  
  <RouterView />
</template>

<style scoped>
.navbar-nav .nav-item {
  display: flex;
}
.dropdown-menu {
  border-radius: 5px;
  border-color: #CCB15F;
  background-color: black;
}
.navbar-toggler-icon {
  color: beige;
}
.navbar-toggler.collapsed {
  color: gray;
  border-color: gray;
  background-color: #1B1B1B;
}
.navbar-toggler {
  color: gray;
  border-color: #685a30;
  background-color: #1B1B1B;
}
span.navbar-toggler-icon {
  color: gray;
  border-color: #CCB15F;
}
.other {
  color: gray;
  border-color: #CCB15F;
  background-color: #1B1B1B;
  border-radius: 100px;
}
</style>



<style scoped>
.navbar-nav .nav-item {
  display: flex;
}
.dropdown-menu {
  border-radius: 5px;
  border-color: #CCB15F;
  background-color: black;
}
.navbar-toggler-icon {
  color: beige;
}
.navbar-toggler.collapsed {
  color: gray;
  border-color: gray;
  background-color: #1B1B1B;
}
.navbar-toggler {
  color: gray;
  border-color: #685a30;
  background-color: #1B1B1B;
}
span.navbar-toggler-icon {
  color: gray;
  border-color: #CCB15F;
}
.other {
  color: gray;
  border-color: #CCB15F;
  background-color: #1B1B1B;
  border-radius: 100px;
}

</style>