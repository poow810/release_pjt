<template>
  <div v-if="movieStore.movieReview.length > 0">
    <div v-for="review in movieStore.movieReview" :key="review.id">
      <div @click="goDetailReview(review.id)">
        <img :src="images[review.user.user_image]" alt="User Image" style="width: 50px; height: 50px;">
        {{ review.user.nickname }}
        {{ review.content }}
        {{ formatDate(review.created_at) }}
      </div>
    </div>
  </div>
  <div v-else>
    리뷰가 없습니다.
  </div>
</template>

<script setup>
import { onMounted } from 'vue'
import { useMovieStore } from '@/stores/movieStore'
import noimage from '@/assets/static/noimage.png'
import image1 from '@/assets/static/cinnamoroll.png'
import image2 from '@/assets/static/kitty.png'
import image3 from '@/assets/static/kuromi.png'
import image4 from '@/assets/static/mymelody.png'
import image5 from '@/assets/static/pompompurin.png'
import router from '@/router'
import { storeToRefs } from 'pinia'


const props = defineProps({
  movieId: String,
})

const images = [noimage, image1, image2, image3, image4, image5]

const movieStore = useMovieStore()

const goDetailReview = (review_id) => {
  console.log(movieStore.movieReview)  
  router.push({ name: 'reviewDetail', params: { review_id: review_id } })
}

const formatDate = function(dateString) {
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

onMounted(async () => {
  await movieStore.getReview(props.movieId)
})


</script>
