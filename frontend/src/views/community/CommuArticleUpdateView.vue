<template>
    <div>
      <h1>글쓰기</h1>
      <form @submit.prevent="submitData(postId)">
        <label for="category">카테고리</label>
        <select v-model="category" name="분류">
          <option value="">분류</option>
          <option value="1"> 영화 </option>
          <option value="2"> 배우 </option>
          <option value="3"> 잡담 </option>
        </select>
        <hr>
        <label for="title">제목: </label>
        <input type="text" id="title" v-model="title">
        <hr>
        <label for="content">내용: </label>
        <input type="textarea" id="content" v-model="content">
  
        <button>완료</button>
  
      </form>
      
    </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useArticleStore } from '@/stores/articleStore'

const router = useRouter()
const store = useArticleStore()
const route = useRoute()

const category = ref('')
const title = ref('')
const content = ref('')

const postId = ref(route.params.id)

const submitData = function (post_id) {
  // console.log(category.value)
  const article = {
    title: title.value,
    content: content.value,
    category: category.value,
  }
  store.updatePost(article, post_id)
  category.value = ''
  title.value = ''
  content.value = ''
}
</script>

<style scoped>

</style>