<template>
  <div>
    <h1>회원가입 페이지</h1>
    <form @submit.prevent="signUp">
      <label for="username">username: </label>
      <input type="text" id="username" v-model.trim="username"><br>

      <label for="email">email: </label>
      <input type="text" id="email" v-model.trim="email"><br>

      <label for="nickname">nickname: </label>
      <input type="text" id="nickname" v-model.trim="nickname"><br>
      
      <label for="password1">password: </label>
      <input type="password" id="password1" v-model.trim="password1"><br>
      
      <label for="password2">password confirm: </label>
      <input type="password" id="password2" v-model.trim="password2"><br>

      <input type="submit" value="signUp">
    </form>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useUserStore } from '@/stores/userStore'
const store = useUserStore()

const username = ref('')
const nickname = ref('')
const email = ref('')
const password1 = ref('')
const password2 = ref('')

const signUp = function () {
  const payload = {
    username: username.value,
    nickname: nickname.value,
    email: email.value,
    password1: password1.value,
    password2: password2.value,
  }
  store.signUp(payload)
}
</script>

<style scoped>

</style>
