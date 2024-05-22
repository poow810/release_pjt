<template>
  <div class="container post-container mt-5">
    <div class="row">
      <div v-for="post in profileStore.posts" :key="post.id" class="col-md-4 mb-4">
        <div class="card post-card h-100" @click="goPost(post.id)">
          <div class="card-body">
            <h1 class="card-title post-title">{{ post.title }}</h1>
            <p class="card-text post-content">{{ post.content }}</p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { useProfileStore } from '@/stores/profileStore'
import { useRouter } from 'vue-router'

const profileStore = useProfileStore()
const router = useRouter()

const goPost = (post_id) => {
  router.push({name: 'articleDetail', params: {id: post_id}})
}
</script>

<style scoped>
body {
  background-color: #2C2C2C;
  color: #ffffff;
}

.post-container {
  padding: 20px;
}

.post-card {
  background-color: #2C2C2C;
  border: 1px solid #CCB15F;
  border-radius: 12px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  transition: transform 0.3s ease, box-shadow 0.3s ease;
}

.post-card:hover {
  transform: translateY(-10px);
  box-shadow: 0 8px 16px rgba(0, 0, 0, 0.2);
}

.post-title {
  color: #CCB15F;
  font-size: 24px;
  margin-bottom: 10px;
}

.post-content {
  color: #ffffff;
  font-size: 16px;
  line-height: 1.5;
}

@media (max-width: 600px) {
  .post-card {
    width: 100%;
  }
}
</style>