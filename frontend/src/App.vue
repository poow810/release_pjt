<script setup>
import { computed, ref, onMounted } from 'vue';
import { RouterLink, RouterView } from 'vue-router'
import { useUserStore } from '@/stores/userStore'
import { useMovieStore } from '@/stores/movieStore';
const userStore = useUserStore()
const searchText = ref('')
const movieStore = useMovieStore()

const id = computed(() => {
  return userStore.userId
})

const searchMovie = () => {
  movieStore.searchMovie(searchText.value)
  searchText.value = ''
}

const logOut = function () { 
  userStore.logOut()
}

onMounted(() => {
  console.log(userStore.isLogIn)
})
</script>

<template>
  <header>
    <nav class="navbar navbar-expand-lg" style="background-color: #1b1b1b;">
      <div class="container-fluid">
        <RouterLink class="navbar-brand fw-bold text-white" to="/">MOVIE</RouterLink>
        <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav" aria-controls="navbarNav" aria-expanded="false" aria-label="Toggle navigation">
          <span class="navbar-toggler-icon"></span>
        </button>
        <div class="collapse navbar-collapse" id="navbarNav">
          <ul class="navbar-nav me-auto mb-2 mb-lg-0">
            <li class="nav-item" v-if="userStore.isLogIn">
              <RouterLink class="nav-link text-white" :to="{ name: 'actor' }">배우</RouterLink>
              <RouterLink class="nav-link text-white" :to="{ name: 'recommend' }">영화추천</RouterLink>
              <RouterLink class="nav-link text-white" :to="{ name: 'weather' }">날씨추천</RouterLink>
            </li>
            <li class="nav-item">
              <RouterLink class="nav-link text-white" :to="{ name: 'community' }">커뮤니티</RouterLink>
            </li>
          </ul>
          <ul class="navbar-nav ms-auto mb-2 mb-lg-0">
            <li class="nav-item">
              <div class="input-group">
                <input type="text" class="form-control" placeholder="검색어를 입력해주세요." aria-label="Input group example" aria-describedby="basic-addon1" v-model="searchText" @keypress.enter="searchMovie">
                <span class="input-group-text" id="basic-addon1" @click="searchMovie">
                  <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-search" viewBox="0 0 16 16">
                    <path d="M11.742 10.344a6.5 6.5 0 1 0-1.397 1.398h-.001q.044.06.098.115l3.85 3.85a1 1 0 0 0 1.415-1.414l-3.85-3.85a1 1 0 0 0-.115-.1zM12 6.5a5.5 5.5 0 1 1-11 0 5.5 5.5 0 0 1 11 0"/></svg>
                </span>
              </div>
            </li>
            <li class="nav-item" v-if="userStore.isLogIn">
              <RouterLink class="nav-link text-white" :to="{ name: 'profile', params: {'id': id}}">프로필</RouterLink>
              <button class="btn btn-outline-success" @click="logOut">로그아웃</button>
            </li>
            <li class="nav-item" v-else>
              <RouterLink class="nav-link text-white" :to="{ name: 'signup' }">회원가입</RouterLink>
              <RouterLink class="nav-link text-white" :to="{ name: 'login' }">로그인</RouterLink>
            </li>
          </ul>
        </div>
      </div>
    </nav>
  </header>

  <RouterView />
</template>



<style scoped>
.navbar-nav .nav-item {
  display: flex;
}
</style>
