import { ref, computed } from 'vue'
import { defineStore } from 'pinia'
import { useRouter } from 'vue-router'
import { useUserStore } from '@/stores/userStore'
import axios from 'axios'

export const useArticleStore = defineStore('articleStore', () => {
  const store = useUserStore()
  const router = useRouter()
  const articles = ref([])
  const SERVER_URL = 'http://43.202.204.222'
  const LOCAL_URL = 'http://192.168.0.13:8000'
  const isLiked = ref(false)
  const likeCount = ref(0)
  const comments = ref([])

  const detailPosts = ref([])

  const detailPostId = ref(null)
  const detailNickName = ref(null)
  const detailUserId = ref(null)

  const commentUserId = ref(null)
  const commentNickName = ref(null)


  const getArticles = function () {
    axios({
      method: 'get',
      url: `${LOCAL_URL}/community/`,
      headers: {
        Authorization: `Token ${store.token}`
      }
    })
    .then((res) => {
      console.log(res.data)
      articles.value = res.data
    })
    .catch((err) => {
      console.log('에러입니다')
      console.log(err)
    })
  }

  const createArticle = function (article) {
    const title = article.title
    const content = article.content
    const category = article.category
    axios({
      method: 'post',
      url: `${LOCAL_URL}/community/create/`,
      data: {
        title, content, category
      },
      headers: {
        Authorization: `Token ${store.token}`
      }
    })
    .then((res) => {
      router.push({ name: 'community' })
    })
    .catch((err) => {
      console.log(err)
    })
  }

  // 디테일 조회
  const getDetailPost = async (postId) => {
    try {
      const res = await axios({
        url: `${LOCAL_URL}/community/detail/${postId}/`,
        method: 'GET',
        headers: {
          Authorization: `Token ${store.token}`
        }
      })
      console.log(res.data)
      detailPosts.value = res.data
      detailNickName.value = res.data.user.nickname
      detailPostId.value = res.data.id
      detailUserId.value = res.data.user.id

      isLiked.value = res.data.is_liked_by_user
    } catch (err) {
      console.log(err)
    }
  }

   // 좋아요
  const favoriteArticle = async (articleId) => {
    try {
      const response = await axios({
        method: 'post',
        url: `${LOCAL_URL}/community/detail/like/${articleId}/`,
        headers: {
          Authorization: `Token ${store.token}`
        }
      })
      console.log(response.data.is_liked)
      isLiked.value = response.data.is_liked
      detailPosts.value.like_count = response.data.like_count
      return response.data
    } catch (err) {
      console.log('좋아요 기능 처리 중 에러', err);
      throw err
    }
  };

  // 게시글 수정
  const updatePost = async (article, post_id) => {
    try {
      const title = article.title
      const content = article.content
      const category = article.category
      const res = await axios({
        method: 'PUT',
        url: `${LOCAL_URL}/community/detail/${post_id}/`,
        headers: {
          Authorization: `Token ${store.token}`
        },
        data: {
          title, content, category
        }
      })
      detailPosts.value = res.data
      detailNickName.value = res.data.user.nickname
      detailPostId.value = res.data.id
      detailUserId.value = res.data.user.id
      alert('수정되었습니다.')
      router.push({name: 'articleDetail', params: {id: detailPostId.value}})
    } catch (err) {
      console.log('업데이트 실패')
    }
  }

  // 게시글 삭제
  const deletePost = async (post_id) => {
    try {
      await axios({
        method: 'DELETE',
        url: `${LOCAL_URL}/community/detail/${post_id}/`,
        headers: {
          Authorization: `Token ${store.token}`
        }
      });
      alert('삭제되었습니다.');
      router.push({name: 'community'})
      // 여기서 게시글 목록으로 리다이렉트하거나, 상태를 업데이트하여 UI를 변경할 수 있습니다.
    } catch (err) {
      console.log('삭제 실패', err);
    }
  }

  // 댓글
  const fetchComments = async (articleId) => {
    try {
      const response = await axios({
        method: 'get',
        url: `${LOCAL_URL}/community/comments/${articleId}/`,
        headers: {
          Authorization: `Token ${store.token}`
        }
      })
      console.log(response.data)
      comments.value = response.data
      commentNickName.value = response.data.nickname
      commentUserId.value = response.data.id
    } catch (err) {
      console.log('댓글 조회 기능 처리 중 에러', err);
    }
  }

  const createComment = async (articleId, content) => {
    try {
      const response = await axios({
        method: 'post',
        url: `${LOCAL_URL}/community/comments/${articleId}/`,
        headers: {
          Authorization: `Token ${store.token}`
        },
        data: {
          'content': content
        }
      })
      comments.value.push(response.data)
    } catch (err) {
      console.log('댓글 생성 기능 처리 중 에러', err);
    }
  }

  const updateComment = async (articleId, commentId, content) => {
    try {
      const response = await axios({
        method: 'PUT',
        url: `${LOCAL_URL}/community/comments/${articleId}/${commentId}/`,
        headers: {
          Authorization: `Token ${store.token}`
        },
        data: {
          content
        }
      })
      console.log(response.data)
      alert("수정되었습니다.")
    } catch (err) {
      console.log('수정 에러')
    }
  }

  const deleteComment = async (articleId, commentId) => {
    try {
      const response = await axios({
        method: 'DELETE',
        url: `${LOCAL_URL}/community/comments/delete/${commentId}/`,
        headers: {
          Authorization: `Token ${store.token}`,
        }
      })
      alert('삭제되었습니다.');
      fetchComments(articleId)
      router.push({name: 'articleDetail', params: {id: articleId}})
    } catch (err) {
      console.log('삭제 실패', err);
    }
  }

  return  {SERVER_URL, LOCAL_URL, articles, isLiked, likeCount, store, comments, detailPosts,
    detailPostId, detailNickName, detailUserId, commentUserId, commentNickName, updateComment, deleteComment,
    fetchComments, getDetailPost, getArticles, createArticle, favoriteArticle, createComment, updatePost, deletePost}
}, {persist: true})
