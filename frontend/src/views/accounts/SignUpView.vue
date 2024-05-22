<template>
  <div class="container mt-5">
    <h1 class="text-center text-white">회원가입 페이지</h1>
    <form @submit.prevent="signUp" class="mx-auto p-4 rounded" style="max-width: 400px; background-color: #2C2C2C;">
      <div class="mb-3">
        <label for="username" class="form-label">Username:</label>
        <input type="text" id="username" v-model.trim="username" class="form-control">
      </div>
      <div class="mb-3">
        <label for="email" class="form-label">Email:</label>
        <input type="text" id="email" v-model.trim="email" class="form-control">
      </div>
      <div class="mb-3">
        <label for="nickname" class="form-label">Nickname:</label>
        <input type="text" id="nickname" v-model.trim="nickname" class="form-control">
      </div>
      <div class="mb-3">
        <label for="password1" class="form-label">Password:</label>
        <input type="password" id="password1" v-model.trim="password1" class="form-control">
      </div>
      <div class="mb-3">
        <label for="password2" class="form-label">Password Confirm:</label>
        <input type="password" id="password2" v-model.trim="password2" class="form-control">
      </div>
      <div class="text-center">
        <input type="submit" value="Sign Up" class="btn btn-primary" style="background-color: #CCB15F; border-color: #CCB15F;">
      </div>
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
body {
  background-color: #2C2C2C;
  color: #ffffff;
}

.form-label, .form-control {
  color: #ffffff;
}

.form-control {
  background-color: #2C2C2C;
  border: 1px solid #CCB15F;
}

.form-control:focus {
  background-color: gainsboro;
  border-color: #CCB15F;
  box-shadow: none;
}

.btn-primary {
  background-color: #CCB15F;
  border-color: #CCB15F;
}

.btn-primary:hover {
  background-color: #B89D50;
  border-color: #B89D50;
}

.text-center {
  text-align: center;
}
</style>