<template>
    <div class="container" v-if="user">
        <div class="row">
            <!-- 이미지 열 -->
            <div class="col-md-6">
                <img :src="selectedImage" @click="showModal = true" alt="Selected" style="cursor: pointer; max-width: 100%;">
                <!-- 모달 -->
                <div v-if="showModal" @click.self="showModal = false" class="modal-backdrop">
                    <div class="modal-content">
                        <h3>이미지 선택</h3>
                        <div class="image-list">
                            <img v-for="(image, index) in images" :key="index" :src="image" @click="selectImage(index)" alt="Option">
                        </div>
                    </div>
                </div>
            </div>
            <!-- 컨텐츠 박스 열 -->
            <div class="col-md-4">
                <div class="row">
                    <div class="col-12">
                        <span>{{ profileStore.userName }}</span>
                        <br>
                        <span>{{ profileStore.nickName }}</span>
                        <div v-if="user_id==userId">
                        <input type="text" v-model="newNickName">
                        <button @click="changeNickname(userId)">닉네임 변경</button>
                    </div>
                    <div v-else>
                        <div v-if="profileStore.isFollowing">
                            <button @click="following(user_id)">팔로잉 취소</button>
                        </div>
                        <div v-else>
                            <button @click="following(user_id)">팔로잉</button>
                        </div>
                    </div>
                    </div>
                </div>
                <div class="row">
                    <div class="col-6">
                        <span>팔로워 수: {{ profileStore.followers_count }}명</span>
                    </div>
                    <div class="col-6">
                        <span>팔로잉 수: {{ profileStore.followings_count }}명</span>
                    </div>
                </div>
                <hr>
                <span>작성한 리뷰 수: {{ profileStore.review_count }}</span>
            </div>
        </div>
        <div class="row mt-4">
            <div class="col-md-4">
                <h3 @click="selectedComponent = ProfileLikeMovie">좋아요한 영화</h3>
            </div>
            <div class="col-md-4">
                <h3 @click="selectedComponent = ProfilePost">내 게시글</h3>
            </div>
            <div class="col-md-4">
                <h3 @click="selectedComponent = ProfileReview">내 리뷰</h3>
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
import { ref, markRaw, watch } from 'vue'
import { useProfileStore } from '@/stores/profileStore'
import { useUserStore } from '@/stores/userStore'
import noimage from '@/assets/static/noimage.png'
import image1 from '@/assets/static/cinnamoroll.png'
import image2 from '@/assets/static/kitty.png'
import image3 from '@/assets/static/kuromi.png'
import image4 from '@/assets/static/mymelody.png'
import image5 from '@/assets/static/pompompurin.png'

defineProps({
    user_id:String,
    user:Object,
})
// 컴포넌트 변수
const selectedComponent = ref(ProfileLikeMovie)

// 이미지 배열
const images = [noimage, image1, image2, image3, image4, image5]

// 프로필 스토어 사용
const profileStore = useProfileStore()
const userStore = useUserStore()
const userId = userStore.userId

// 유저 팔로잉
const following = (user_id) => {
    profileStore.userFollowing(user_id)
}

// 닉네임 변경
const newNickName = ref(null)
const changeNickname = (user_id) => {
    profileStore.changeNickname(user_id, newNickName.value)
    newNickName.value = null
}

// 선택된 이미지와 모달 상태
const selectedImage = ref(images[0]) // 기본 이미지로 noimage 설정
const showModal = ref(false)

// 이미지 선택 함수
function selectImage(index) {
    selectedImage.value = images[index]
    showModal.value = false
    updateUserImage(index)
}

// 사용자 이미지 업데이트 함수
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

// 프로필 데이터 가져오기
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
/* 스타일 작성 */
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