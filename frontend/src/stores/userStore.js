import { ref, computed } from 'vue'
import { defineStore } from 'pinia'
import { useRouter } from 'vue-router'
import axios from 'axios'

export const useUserStore = defineStore('userStore', () => {
  // token 상태 유지
  const token = ref(null)
  const router = useRouter()
  const SERVER_URL = 'https://pkpk.o-r.kr/'
  const LOCAL_URL = 'http://192.168.85.248:8000'
  // userId 상태 제거
  const userInfo = ref(null)

  // userInfo가 null이 아닌 경우 로그인한 것으로 간주
  const isLogIn = computed(() => userInfo.value !== null)

  const logIn = async (payload) => {
    const { username, password } = payload
    try {
      const res = await axios.post(`${LOCAL_URL}/accounts/login/`, { username, password }, {
        headers: { 'Content-Type': 'application/json' }
      })
      token.value = res.data.key
      await checkUser(token.value)
      router.push({ name: 'home' })
    } catch (err) {
      alert(err.response.data.non_field_errors)
      console.log(err)
    }
  }

  const checkUser = async (token) => {
    try {
      const res = await axios.get(`${LOCAL_URL}/accounts/user/`, {
        headers: { 'Authorization': `Token ${token}` }
      })
      // userId 제거하고 userInfo만 업데이트
      userInfo.value = res.data
    } catch (err) {
      console.log(err)
    }
  }

  const logOut = async () => {
    try {
      await axios.post(`${LOCAL_URL}/accounts/logout/`, {}, {
        headers: { Authorization: `Token ${token.value}` }
      })
      token.value = null
      userInfo.value = null
      router.push({ name: 'login' })
    } catch (err) {
      console.log('로그아웃 실패')
      console.log(err)
    }
  }

  const signUp = async (payload) => {
    const { username, nickname, email, password1, password2 } = payload
    if (password1 !== password2) {
      alert('비밀번호가 일치하지 않습니다.')
      router.push({ name: 'signup' })
      return
    }
    try {
      await axios.post(`${LOCAL_URL}/accounts/signup/`, {
        username, nickname, email, password1, password2
      })
      await logIn({ username, password: password1 })
    } catch (err) {
      const errorResponse = JSON.parse(err.response.request.responseText)
      const firstErrorField = Object.keys(errorResponse)[0]
      const firstErrorMessage = errorResponse[firstErrorField][0]
      alert(`${firstErrorMessage}`)
      console.log(err)
    }
  }

  const updateImage = (index) => {
    userInfo.value.user_image = index
  }

  return { token, SERVER_URL, LOCAL_URL, isLogIn, userInfo, signUp, logIn, logOut, checkUser, updateImage }
}, { persist: true })
