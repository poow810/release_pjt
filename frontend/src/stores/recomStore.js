import { ref, computed } from 'vue'
import { defineStore } from 'pinia'
import { useRouter } from 'vue-router'
import { useUserStore } from '@/stores/userStore'
import axios from 'axios'

export const useRecomStore = defineStore('recomStore', () => {
  const store = useUserStore()
  const router = useRouter()
  const SERVER_URL = 'http://43.202.204.222'
  const LOCAL_URL = 'http://192.168.0.13:8000'

  // 응답데이터 저장
  const userSetGenre = ref(null)
  const anyname = ref('qwer')

  const getGenreToServer = async (select) => {
    axios({
      method: 'get',
      url: `${LOCAL_URL}/movie/genreSelect/`,
      headers: {
        Authorization: `Token ${store.token}`
      },
      params: {
        genre: select
      },
    })
    .then(res => {
      console.log('성공:', res.data)
      userSetGenre.value = res.data
      router.push({ name: 'recommend' })
    })
    .catch(err => {
      console.error('영화 데이터 보내기 실패:', err)
    })
  }
  
  const isSelect = computed(() => {
    
    return Boolean(userSetGenre.value)
    // if (Boolean(userSetGenre.value)) {
    //   return false
    // } else {
    //   return true
    // }
  })
  
  const resetUserSetGenre = () => {
    userSetGenre.value = null;
  };

  return { store, SERVER_URL, LOCAL_URL, userSetGenre, getGenreToServer, isSelect, resetUserSetGenre, anyname}
  }, 
  {persist: { key: 'recomStore',
    paths: ['userSetGenre']
  }
})