import { ref, computed } from 'vue'
import { defineStore } from 'pinia'
import { useRouter } from 'vue-router'
import axios from 'axios'

export const useUserStore = defineStore('userStore', () => {
  const token = ref(null)
  const router = useRouter()
  const SERVER_URL = 'http://43.202.204.222'
  const LOCAL_URL = 'http://192.168.0.13:8000'
  const userId = ref(null)

  // 로그인 확인
  const isLogIn = computed(() => {
    if (token.value === null) {
      return false
    } else {
      return true
    }
  })
  
  // 로그인
  const logIn = async function (payload) { // async 키워드 추가
    const { username, password } = payload
    try {
      const res = await axios({
        method: 'post',
        url: `${LOCAL_URL}/accounts/login/`,
        data: { username, password },
        headers: { 'Content-Type': 'application/json' }
      })
      
      token.value = res.data.key
      await checkUser(token.value) // await를 사용하여 비동기 처리 기다림
      router.push({ name: 'home' }) // userId가 업데이트된 후에 홈으로 이동
    } catch (err) {
      alert(err.response.data.non_field_errors)
      console.log(err);
    }
  }

  // 로그인 후 사용자 확인 및 정의
  const checkUser = (token) => {
    axios({
      method: 'GET',
      url: `${LOCAL_URL}/accounts/user/`,
      headers: {
        'Authorization': `Token ${token}`
      }
    })
    .then(res => {
      console.log(res.data)
      userId.value = res.data.pk
    })
    .catch(err => { console.log(err) })
  }

  // 로그아웃
  const logOut = function () {
    console.log(token.value)
    axios({
      method: 'post',
      url: `${LOCAL_URL}/accounts/logout/`,
      headers: { Authorization: `Token ${token.value}`}
    })
    .then((res) => {
      token.value = null // token 초기화
      router.push({ name: 'login' })
    })
    .catch((err) => {
      console.log('로그아웃 실패')
      console.log(err)
    })
  }
  
  // 회원가입
  const signUp = function (payload) {
    const { username, nickname, email, password1, password2 } = payload

    if (password1 !== password2) {
      alert('비밀번호가 일치하지 않습니다.')
      return router.push({name:'signup'})
    }
    axios({
      method: 'post',
      url: `${LOCAL_URL}/accounts/signup/`,
      data: {
        username, nickname, email, password1, password2
      }
    })
    .then((res) => {
      console.log(res)
      const password = password1
      logIn({ username, password })
    })
    .catch((err) => {
      const errorResponse = JSON.parse(err.response.request.responseText);
      const firstErrorField = Object.keys(errorResponse)[0];
      const firstErrorMessage = errorResponse[firstErrorField][0];
      
      alert(`${firstErrorMessage}`);
      console.log(err);
    })
  }


  return { userId, token, SERVER_URL, LOCAL_URL, isLogIn,
  signUp, logIn, logOut, checkUser }
}, {persist: true})
