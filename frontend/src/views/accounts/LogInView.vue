<template>
  <div class="container mt-5">
    <h1 class="text-center text-white">로그인 페이지</h1>
    <form @submit.prevent="logIn" class="mx-auto p-4 rounded" style="max-width: 400px; background-color: #2C2C2C;">
      <div class="mb-3">
        <label for="username" class="form-label">Username:</label>
        <input type="text" id="username" v-model.trim="username" class="form-control">
      </div>
      <div class="mb-3">
        <label for="password" class="form-label">Password:</label>
        <input type="password" id="password" v-model.trim="password" class="form-control">
      </div>
      <div class="text-center">
        <input type="submit" value="Log In" class="btn btn-primary" style="background-color: #CCB15F; border-color: #CCB15F;">
      </div>
    </form>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useUserStore } from '@/stores/userStore'
import { useRouter } from 'vue-router';

const router = useRouter()
const store = useUserStore()

const username = ref('')
const password = ref('')

const logIn = function () {
  const payload = {
    username: username.value,
    password: password.value
  }
  store.logIn(payload)
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