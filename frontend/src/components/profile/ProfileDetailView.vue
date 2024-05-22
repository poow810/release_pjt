<template>
    <div class="container mt-5" v-if="user">
      <div class="row">
        <div class="col-md-6">
          <img :src="selectedImage" @click="showModal = true" alt="Selected" class="img-fluid" style="cursor: pointer;">
          <div v-if="showModal" @click.self="showModal = false" class="modal-backdrop">
            <div class="modal-content">
              <h3>이미지 선택</h3>
              <div class="image-list d-flex flex-wrap">
                <img v-for="(image, index) in images" :key="index" :src="image" @click="selectImage(index, user_id)" alt="Option" class="img-thumbnail m-2" style="cursor: pointer; max-width: 100px;">
              </div>
            </div>
          </div>
        </div>
        <div class="col-md-6">
          <div class="mb-3">
            <h2>{{ profileStore.userName }}</h2>
            <h4>{{ profileStore.nickName }}</h4>
            <div v-if="user_id == userId" class="mt-3">
              <input type="text" v-model="newNickName" class="form-control mb-2">
              <button @click="changeNickname(userId)" class="btn btn-primary">닉네임 변경</button>
            </div>
            <div v-else>
              <button @click="following(user_id)" class="btn" :class="{'btn-secondary': profileStore.isFollowing, 'btn-primary': !profileStore.isFollowing}">
                {{ profileStore.isFollowing ? '팔로잉 취소' : '팔로잉' }}
              </button>
            </div>
          </div>
          <div class="row mt-4">
            <div class="col-6 fs-3">
              <span>팔로워 수: {{ profileStore.followers_count }}명</span>
            </div>
            <div class="col-6 fs-3">
              <span>팔로잉 수: {{ profileStore.followings_count }}명</span>
            </div>
          </div>
          <hr>
          <span>작성한 리뷰 수: {{ profileStore.review_count }}</span>
        </div>
      </div>
      <div class="row mt-4">
        <hr class="text-white">
        <div class="col-md-4 text-center text-white">
          <h3 @click="selectedComponent = ProfileLikeMovie" class="cursor-pointer">좋아요한 영화</h3>
        </div>
        <div class="col-md-4 text-center text-white">
          <h3 @click="selectedComponent = ProfilePost" class="cursor-pointer">내 게시글</h3>
        </div>
        <div class="col-md-4 text-center text-white">
          <h3 @click="selectedComponent = ProfileReview" class="cursor-pointer">내 리뷰</h3>
        </div>
      </div>
      <div class="row mt-4">
        <component :is="selectedComponent"></component>
      </div>
    </div>
  </template>
  
  <script setup>
  
  import ProfileLikeMovie from './ProfileLikeMovie.vue'
  import ProfilePost from './ProfilePost.vue'
  import ProfileReview from './ProfileReview.vue'
  
  import axios from 'axios'
  import { ref, watch } from 'vue'
  import { useProfileStore } from '@/stores/profileStore'
  import { useUserStore } from '@/stores/userStore'
  import noimage from '@/assets/static/noimage.png'
  import image1 from '@/assets/static/cinnamoroll.png'
  import image2 from '@/assets/static/kitty.png'
  import image3 from '@/assets/static/kuromi.png'
  import image4 from '@/assets/static/mymelody.png'
  import image5 from '@/assets/static/pompompurin.png'
  
  defineProps({
      user_id: String,
      user: Object,
  })
  
  const selectedComponent = ref(ProfileLikeMovie)
  
  const images = [noimage, image1, image2, image3, image4, image5]
  
  const profileStore = useProfileStore()
  const userStore = useUserStore()
  const userId = userStore.userId
  
  const following = (user_id) => {
      profileStore.userFollowing(user_id)
  }
  
  const newNickName = ref(null)
  const changeNickname = (user_id) => {
      profileStore.changeNickname(user_id, newNickName.value)
      newNickName.value = null
  }
  
  const selectedImage = ref(images[0])
  const showModal = ref(false)
  
  function selectImage(index, user_id) {
    if (userId == user_id) {
        selectedImage.value = images[index]
        showModal.value = false
        updateUserImage(index)
    } else {
      alert("자신의 프로필 이미지만 변경할 수 있습니다.")
      showModal.value = false
    }
  }
  
  function updateUserImage(imageIndex) {
      axios({
          method: 'PUT',
          url: `${profileStore.LOCAL_URL}/profile/${userStore.userId}/`,
          headers: {
              'Authorization': `Token ${userStore.token}`
          },
          data: {
              user_image: imageIndex
          }
      })
      .then(res => {
          console.log('이미지 업데이트 성공:', res.data)
      })
      .catch(err => {
          console.error('이미지 업데이트 실패:', err)
      })
  }
  
  watch(() => profileStore.userImage, (newValue) => {
      selectedImage.value = images[newValue] || noimage
  })
  
  if (profileStore.userImage !== null) {
      selectedImage.value = images[profileStore.userImage] || noimage
  } else {
      selectedImage.value = noimage
  }
  </script>
  
  <style scoped>
  body {
    background-color: #2C2C2C;
    color: #ffffff;
  }
  
  h2, h4, span {
    color: #ffffff;
  }
  
  .btn-primary {
    background-color: #CCB15F;
    border-color: #CCB15F;
  }
  
  .btn-primary:hover {
    background-color: #B89D50;
    border-color: #B89D50;
  }
  
  .btn-secondary {
    background-color: #ffffff;
    color: #2C2C2C;
    border-color: #ffffff;
  }
  
  .btn-secondary:hover {
    background-color: #e0e0e0;
    border-color: #e0e0e0;
  }
  
  .cursor-pointer {
    cursor: pointer;
  }
  
  .modal-backdrop {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background: rgba(0, 0, 0, 0.5);
    display: flex;
    justify-content: center;
    align-items: center;
  }
  
  .modal-content {
    background: white;
    padding: 20px;
    border-radius: 5px;
  }
  
  .image-list img {
    cursor: pointer;
    margin: 5px;
    max-width: 100px;
  }
  </style>