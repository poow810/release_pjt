import { ref, computed } from 'vue'
import { defineStore } from 'pinia'
import { useRouter } from 'vue-router'
import { useUserStore } from '@/stores/userStore'
import axios from 'axios'

export const useMovieStore = defineStore('movieStore', () => {
  const store = useUserStore()
  const token =  store.token
  const router = useRouter()
  const LOCAL_URL = 'http://172.30.1.32:8000'
  const SERVER_URL = 'http://43.202.204.222'
  const TMDB_BASE_URL = 'https://api.themoviedb.org/3'
  const API_KEY = import.meta.env.VITE_TMDB_API_KEY

  const nowPlayingMovies = ref([]) // 상영중 영화
  const ratedMovies = ref([]) // 평점순 영화
  const genreMovies = ref([]) // 장르별 영화
  
  const isLiked = ref(false)
  const likeCount = ref(0)

  const movieReview = ref([])

  const detailMovies = ref({})

  const detailReviews = ref(null)

  // 평점 높은순
  const getRatedMovies = async () => {
    axios({
      method: 'get',
      url: `${TMDB_BASE_URL}/movie/top_rated`,
      params: {
        api_key: API_KEY,
        language: 'ko-KR'
      }
    })
    .then(res => {
      console.log('평점영화 데이터 가져오기 성공:', res.data)
      ratedMovies.value = res.data.results
    })
    .catch(err => {
      console.error('영화 데이터 가져오기 실패:', err)
    })
  }

  // 현재 상영중
  const getNowPlayingMovies = async () => {
    axios({
      method: 'get',
      url: `${TMDB_BASE_URL}/movie/now_playing`,
      params: {
        api_key: API_KEY,
        language: 'ko-KR'
      }
    })
    .then(res => {
      console.log('상영영화 데이터 가져오기 성공:', res.data)
      nowPlayingMovies.value = res.data.results
    })
    .catch(err => {
      console.error('영화 데이터 가져오기 실패:', err)
    })
  }
  
    // 장르별
    const getGenreList = async () => {
      axios({
        method: 'get',
        url: `${TMDB_BASE_URL}/genre/movie/list`,
        params: {
          api_key: API_KEY,
          language: 'ko-KR'
        }
      })
      .then((res) => {
        console.log('장르 영화 데이터 가져오기 성공:', res.data)
        genreMovies.value = res.data
      })
      .catch((err) => {
        console.log('데이터수집 실패:', err)
      })
    }

    // 장르별 인기 영화 가져오기
    const getPopularMoviesByGenre = async (genreId) => {
      try {
        const response = await axios({
          method: 'get',
          url: `${TMDB_BASE_URL}/discover/movie`,
          params: {
            api_key: API_KEY,
            language: 'ko-KR',
            sort_by: 'popularity.desc',
            include_adult: false,
            include_video: false,
            page: 1,
            with_genres: genreId // 장르 ID를 파라미터로 전달
          }
        });
        console.log('장르별 인기 영화 데이터 가져오기 성공:', response.data);
        genreMovies.value = response.data.results; // genreMovies에 결과 저장
      } catch (err) {
        console.error('장르별 인기 영화 데이터 가져오기 실패:', err);
      }
    };

  
  // 영화 상세 조회
  const movieDetail = async (movieId) => {
    try {
      const response = await axios({
        method: 'get',
        url: `${LOCAL_URL}/movie/detail/${movieId}/`,
        headers: {
          Authorization: `Token ${store.token}`
        }
      })
      console.log('영화 상세 조회 성공:', response.data)
      detailMovies.value = response.data
    } catch (err) {
      console.log('영화 상세 조회 기능 처리 중 에러', err);
    }
  }

  // 영화 좋아요
  const movieLike = async (movieId) => {
    try {
      const response = await axios({
        method: 'post',
        url: `${LOCAL_URL}/movie/like/${movieId}/`, 
        headers: {
          Authorization: `Token ${store.token}`
        }
      })
      console.log(response.data)
      return response.data; // 여기서 좋아요 상태와 개수를 반환합니다.
    } catch (err) {
      console.log('좋아요 기능 처리 중 에러', err);
      return null; // 에러 발생시 null 반환
    }
  }

  // 영화 리뷰
  const createReview = async (movieId, payload) => {
    const title = payload.title
    const content = payload.content
    const rating = payload.rating
    try {
      const response = await axios({
        method: 'post',
        url: `${LOCAL_URL}/movie/review/${movieId}/`,
        headers: {
          Authorization: `Token ${store.token}`
        },
        data: {
          title: title,
          content: content,
          rating: rating,
        }
      })
      router.push({ name:'movieDetail', params: { movieId } })
    }
    catch (err) {
      console.log('영화 리뷰 처리 중 에러', err);
    }
  }

  const updateReview = async (movieId, payload) => {

  }

  const getReview = async (movieId) => {
    try {
      const response = await axios({
        method: 'get',
        url: `${LOCAL_URL}/movie/review/${movieId}/`,
        headers: {
          Authorization: `Token ${store.token}`
        }
      })
      console.log(response.data)
      movieReview.value = response.data
      console.log(movieReview.value)
    }
    catch (err) {
      if (err.response && err.response.status === 404) {
        movieReview.value = []
      } else {
        console.log('영화 리뷰 데이터 가져오기 실패:', err);
      }
    }
  }

  const searchMovie = async (type, text) => {
    try {
      const response = await axios({
        method: 'get',
        url: `${LOCAL_URL}/movie/search/`,
        params: {
          type: type,
          text: text,
        }
      })
      console.log(response.data)
    }
    catch (err) {
      console.log('영화 검색 데이터 가져오기 실패:', err);
    }
  }
  
  const getDetailReview = async (reviewId) => {
    try {
      const response = await axios.get(`${LOCAL_URL}/movie/review/detail/${reviewId}/`, {
      headers: {
        Authorization: `Token ${store.token}`
      }
    })
    detailReviews.value = response.data
    }
    catch (err) {
      console.log('영화 리뷰 데이터 가져오기 실패:', err);
    }
  }

  return { API_KEY, token, SERVER_URL, LOCAL_URL, nowPlayingMovies, ratedMovies, genreMovies, movieLike,
    isLiked, likeCount, movieReview, detailMovies, detailReviews, movieDetail, getReview, createReview, getRatedMovies, getNowPlayingMovies, getGenreList,
    getPopularMoviesByGenre, searchMovie, getDetailReview }
}, {persist: true})
