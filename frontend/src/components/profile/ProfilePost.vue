<template>
  <div class="post-container">
    <div v-for="post in profileStore.posts" :key="post.id" class="post-card" @click="goPost(post.id)">
      <h1 class="post-title">{{ post.title }}</h1>
      <p class="post-content">{{ post.content }}</p>
    </div>
  </div>
</template>

<script setup>
import { useProfileStore } from '@/stores/profileStore'
import { computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'

const profileStore = useProfileStore()
const router = useRouter()

const goPost = (post_id) => {
  router.push({name: 'articleDetail', params: {id: post_id}})
}
</script>

<style>
.post-container {
  display: flex;
  flex-wrap: wrap;
  justify-content: center;
  gap: 20px;
  padding: 20px;
}

.post-card {
  background-color: #fff;
  border-radius: 12px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  padding: 20px;
  width: 300px;
  transition: transform 0.3s ease, box-shadow 0.3s ease;
}

.post-card:hover {
  transform: translateY(-10px);
  box-shadow: 0 8px 16px rgba(0, 0, 0, 0.2);
}

.post-title {
  color: #333;
  font-size: 24px;
  margin-bottom: 10px;
}

.post-content {
  color: #666;
  font-size: 16px;
  line-height: 1.5;
}

@media (max-width: 600px) {
  .post-card {
    width: 100%;
  }
}
</style>
