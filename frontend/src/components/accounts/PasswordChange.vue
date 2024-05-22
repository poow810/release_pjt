<template>
  <div>
    <h2>비밀번호 변경 페이지</h2>
    <form @submit.prevent="requestPasswordReset">
      <div>
        <label for="email">Email:</label>
        <input type="email" v-model="email" required />
      </div>
      <button type="submit">Send Password Reset Email</button>
    </form>
    <p v-if="message">{{ message }}</p>
  </div>
</template>

<script setup>
import { ref } from 'vue'

const email = ''
const user_email = ref(null)

const requestPasswordReset = async() => {
  try {
    const response = await axios({
      method: 'post',
      url: `http://192.168.214.13:8000/accounts/password/reset/${email}/`,
      })
    const message = response.data.detail;
    console.log(message)
  } catch (error) {
    console.log('다시 시도해주세요.')
  }
}
</script>
<style scoped>



</style>