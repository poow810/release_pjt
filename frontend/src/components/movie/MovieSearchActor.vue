<template>
  <div class="card-content">
    <img v-if="personImageUrl" :src="personImageUrl" alt="actor" class="actor-image">
    <p class="fs-2 mt-2">{{ searchMovie.name_kr }}</p>
    <p class="text-white">{{ searchMovie.overview }}</p>
  </div>
</template>

<script setup>
import axios from 'axios';
import { ref, onMounted } from 'vue';
import { useRouter } from 'vue-router';

const API_KEY = import.meta.env.VITE_TMDB_API_KEY;

const getPersonIdByName = async (name) => {
  try {
    const response = await axios.get(`https://api.themoviedb.org/3/search/person`, {
      params: {
        api_key: API_KEY,
        query: name,
      },
    });
    const person = response.data.results[0];
    return person ? person.id : null;
  } catch (error) {
    console.error(error);
    return null;
  }
};

const getPersonDetailsById = async (id) => {
  try {
    const response = await axios.get(`https://api.themoviedb.org/3/person/${id}`, {
      params: {
        api_key: API_KEY,
      },
    });
    console.log(response.data)
    return response.data;
  } catch (error) {
    console.error(error);
    return null;
  }
};

const getPersonImageByName = async (name) => {
  try {
    const personId = await getPersonIdByName(name);
    if (personId) {
      const personDetails = await getPersonDetailsById(personId);
      if (personDetails && personDetails.profile_path) {
        return `https://image.tmdb.org/t/p/w500${personDetails.profile_path}`;
      } else {
        throw new Error('No profile image found for that person.');
      }
    }
  } catch (error) {
    console.error(error);
    return null;
  }
};

const router = useRouter();
const props = defineProps({
  searchMovie: Object,
});

const goDetail = (movie_id) => {
  router.push({ name: 'movieDetail', params: { id: movie_id } });
};

const personImageUrl = ref(null);

onMounted(async () => {
  if (props.searchMovie.name_en) {
    personImageUrl.value = await getPersonImageByName(props.searchMovie.name_en);
  }
});
</script>

<style scoped>
.poster-image {
    width: 100%;
    height: auto;
    border-radius: 10px;
    margin-bottom: 15px;
}

.actor-image {
    width: 100px;
    height: auto;
    border-radius: 50%;
    margin-bottom: 15px;
}

.card-content {
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    align-items: center;
    text-align: center;
}
</style>
