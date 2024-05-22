<template>
  <div>
    <h4>댓글</h4>
    <!-- 댓글 카드 -->
    <div class="comment-card p-3 my-2 border rounded" v-for="comment in articleStore.comments" :key="comment.id">
      <div class="d-flex align-items-center">
        <img class="rounded-circle m-2" :src="images[comment.user.user_image]"  alt="User Image" style="width: 50px; height: 50px;">
        <strong>{{ comment.user.nickname }}</strong>
      </div>
      <!-- 댓글 내용 -->
      <div class="comment-content text-left m-2">
        <p>{{ comment.content }}</p>
      </div>
      <!-- 댓글 작성 시간 -->
      <div class="text-muted m-2">
        <p class="text-secondary">{{ formatDate(comment.created_at) }}</p>
      </div>
    </div>
    <!-- 댓글 입력 폼 -->
    <form @submit.prevent="createComment">
      <input type="text" v-model="comment" placeholder="댓글을 남겨보세요" class="form-control my-2">
      <button type="submit" class="btn">등록</button>
    </form>    
  </div>
</template>

<script setup>
import { ref, watch, onMounted } from 'vue'
import { useArticleStore } from '@/stores/articleStore'
import noimage from '@/assets/static/noimage.png'
import image1 from '@/assets/static/cinnamoroll.png'
import image2 from '@/assets/static/kitty.png'
import image3 from '@/assets/static/kuromi.png'
import image4 from '@/assets/static/mymelody.png'
import image5 from '@/assets/static/pompompurin.png'

const images = [noimage, image1, image2, image3, image4, image5]

const { articleId } = defineProps({
  articleId: Number,
})

const articleStore = useArticleStore()
const comment = ref('')
const loading = ref(true) // 로딩 상태 추가

const createComment = async () => {
  if (comment.value.trim()) { 
    await articleStore.createComment(articleId, comment.value)
    comment.value = ''
    await articleStore.fetchComments(articleId) // 새 댓글 작성 후 댓글 목록 재로딩
  }
}

const fetchComments = async (articleId) => {
  loading.value = true // 로딩 시작
  await articleStore.fetchComments(articleId)
  loading.value = false // 로딩 끝
}

onMounted(() => {
  fetchComments(articleId) // 컴포넌트 마운트 시 댓글 로딩
})

watch(() => articleId, async (newVal, oldVal) => {
  if (newVal !== undefined && newVal !== oldVal) {
    await fetchComments(newVal)
  }
}, { immediate: true }) // 컴포넌트가 마운트될 때 즉시 실행

const formatDate = (dateString) => {
  const options = {
    year: 'numeric',
    month: '2-digit',
    day: '2-digit',
    hour: '2-digit',
    minute: '2-digit',
  };
  const date = new Date(dateString);
  const formattedDate = date.toLocaleString('ko-KR', options);
  return formattedDate.replace(/\. /g, '.').replace(/, /g, ' ');
}
</script>

<style scoped>
.btn {
  background-color: #CCB15F;
  color: #ffffff;
}

.card-subtitle {
  color: #adb5bd;
}

.comment-card {
  overflow: hidden; /* 댓글 카드 안에서 내용이 넘치지 않도록 함 */
}

.comment-content {
  word-wrap: break-word; /* 긴 단어나 URL 등이 넘칠 경우 자동으로 줄바꿈 */
  white-space: pre-line; /* 내용 내의 개행 문자를 줄바꿈으로 처리 */
}
</style>