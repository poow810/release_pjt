<template>
  <div>
    <img :src="images[movieStore.detailReviews?.user_image || 0]" alt="User Image" style="width: 50px; height: 50px;">
    <p>{{ movieStore.detailReviews?.user.nickname }}</p>    
    <p>제목: {{ movieStore.detailReviews?.title }}</p>
    <p>내용: {{ movieStore.detailReviews?.content }}</p>
    <p>평점: {{ movieStore.detailReviews?.rating }}</p>
  </div>
</template>
<script setup>
import { useRoute } from 'vue-router'
import { ref, onMounted } from 'vue'
import axios from 'axios';
import noimage from '@/assets/static/noimage.png'
import image1 from '@/assets/static/cinnamoroll.png'
import image2 from '@/assets/static/kitty.png'
import image3 from '@/assets/static/kuromi.png'
import image4 from '@/assets/static/mymelody.png'
import image5 from '@/assets/static/pompompurin.png'
import { useMovieStore } from '@/stores/movieStore';

const images = [noimage, image1, image2, image3, image4, image5]
const route = useRoute()
const review_id = ref(route.params.review_id)
const movieStore = useMovieStore()

const reviews = ref(null)

onMounted(() => {
  movieStore.getDetailReview(review_id.value)
})
</script>