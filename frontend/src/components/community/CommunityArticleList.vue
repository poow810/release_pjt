<template>
  <div>
    <ul>
      <div>         
        <p>작성자 : {{ article.category }}</p>
        <p>제목 : {{ article.title }}</p>
        <p>내용 : {{ article.content }}</p>
        <hr>
      </div>
    </ul>
  </div>
</template>

<script setup>
import { onMounted } from 'vue';
import { useRouter } from 'vue-router'
const router = useRouter()

defineProps({
  article: Object
})

</script>

<style scoped>

</style>