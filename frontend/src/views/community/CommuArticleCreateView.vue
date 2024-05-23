<template>
  <div class="container mt-5">
    <h1 class="text-ccb15f mb-4">글쓰기</h1>
    <form @submit.prevent="submitData" class="p-4 border rounded custom-border">
      <div class="form-group mb-3 fs-5">
        <label for="category" class="form-label text-ccb15f">카테고리</label>
        <select v-model="category" class="form-select" name="분류">
          <option value="">분류</option>
          <option value="1"> 영화 </option>
          <option value="2"> 배우 </option>
          <option value="3"> 잡담 </option>
        </select>
      </div>
      <hr>
      <div class="form-group mb-3">
        <label for="title" class="form-label text-ccb15f fs-5">제목</label>
        <input type="text" id="title" v-model="title" class="form-control">
      </div>
      <hr>
      <div class="form-group mb-3">
        <label for="content" class="form-label text-ccb15f fs-5">내용</label>
        <textarea id="content" v-model="content" class="form-control"></textarea>
      </div>
      <button type="submit" class="btn btn-primary fs-4 custom-btn">완료</button>
    </form>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useArticleStore } from '@/stores/articleStore'

const router = useRouter()
const store = useArticleStore()

const category = ref('')
const title = ref('')
const content = ref('')

const submitData = function () {
  const article = {
    title: title.value,
    content: content.value,
    category: category.value,
  }
  store.createArticle(article)
  category.value = ''
  title.value = ''
  content.value = ''
}
</script>

<style scoped>
.container {
  background-color: #1b1b1b;
  color: #ffffff;
  padding: 20px;
  border-radius: 10px;
}

.text-ccb15f {
  color: #CCB15F;
}

.custom-border {
  border: 1px solid #CCB15F;
}

.form-label {
  color: #CCB15F;
}

.form-control {
  border: 1px solid #CCB15F;
  background-color: #1b1b1b;
  color: #ffffff;
}

.form-control:focus, .form-select:focus {
  border-color: #CCB15F;
  box-shadow: 0 0 0 0.2rem rgba(204, 177, 95, 0.25);
}

.custom-btn {
  background-color: #CCB15F;
  border-color: #CCB15F;
}

.custom-btn:hover {
  background-color: #b89a4e;
  border-color: #b89a4e;
}

.hr {
  border-top: 1px solid #CCB15F;
}
</style>