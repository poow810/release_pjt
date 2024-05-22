<template>
  <div class="container mt-5">
    <div v-if="articleStore.detailPosts" class="card p-3">
      <h1 class="card-title mt-4">{{ articleStore.detailPosts.title }}</h1>
      <div>
        <p>{{ articleStore.detailNickName }}</p>
        <div v-show="userStore.userId == articleStore.detailUserId">
          <button @click="updatePost(articleStore.detailPosts.id)">수정</button>
          <button @click="deletePost(articleStore.detailPosts.id)">삭제</button>
        </div>
      </div>
      <hr>
      <p class="card-text">조회수: {{ articleStore.detailPosts.click_count }}</p>
      <div class="card-body">
        <p class="card-text">{{ articleStore.detailPosts.content }}</p>
        <button @click="handleFavorite(articleStore.detailPosts.id)" class="btn">
          <span v-if="articleStore.isLiked">좋아요 취소</span>
          <span v-else>좋아요</span>
        </button>
      </div>
      <hr>
      <div v-if="articleStore.detailPosts.id">
        <CommentView :articleId="articleStore.detailPosts.id" :key="articleStore.detailPosts.id"/>
      </div>
    </div>
    <div v-else class="text-center">
      <div class="spinner-border" role="status">
        <span class="visually-hidden">Loading...</span>
      </div>
      <p>게시글 불러오는 중..</p>
    </div>
  </div>
</template>


<script setup>
import axios from 'axios';
import { onMounted, ref, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useUserStore } from '@/stores/userStore'
import { useArticleStore } from '@/stores/articleStore'
import CommentView from '@/components/community/CommentView.vue';

const articleStore = useArticleStore()
const userStore = useUserStore()
const route = useRoute()
const router = useRouter()
const article = ref(null)
const postId = ref(null)

const updatePost = (post_id) => {
  router.push({name: 'update', params: {'id': post_id}})    
}

const deletePost = (post_id) => {
  articleStore.deletePost(post_id)
}

watch(() => route.params.id, async (newId) => {
  if (newId) {
    postId.value = newId
    await articleStore.getDetailPost(postId.value)
  }
}, {deep: true})

const handleFavorite = (postId) => {
  articleStore.favoriteArticle(postId)
}

onMounted(() => {
  if (route.params.id) {
    postId.value = route.params.id
    articleStore.getDetailPost(postId.value)
  }
})
</script>
<style scoped>
div.card {
  background-color: black;
}
button {
  margin-top: 10px;
  background-color: #CCB15F;
}
* {
  color: #ffffff;
}

.container {
  background-color: #343a40;
  color: #ffffff;
  padding: 20px;
  border-radius: 10px;
}

.card {
  background-color: #212529;
  color: #ffffff;
}

.card-title {
  color: #ffffff;
}

.card-subtitle {
  color: #adb5bd;
}

.card-text {
  color: #ffffff;
}

.btn-primary {
  margin-top: 10px;
}

.spinner-border {
  margin-top: 20px;
}
</style>
