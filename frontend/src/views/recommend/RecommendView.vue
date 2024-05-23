<template>
    <div>
        <div v-if="recomStore.isSelect">
            <button @click="reload" class="reload-button">재추천</button>
            <MovieRecomView />
        </div>
        <div v-else>
            <MovieRecomselectView />
        </div>
    </div>
</template>

<script setup>
import { computed } from 'vue'
import { useRecomStore } from '@/stores/recomStore'
import MovieRecomselectView from '@/components/recommend/MovieRecomselectView.vue'
import MovieRecomView from '@/components/recommend/MovieRecomView.vue'
import { useRouter } from 'vue-router'

const router = useRouter()
const recomStore = useRecomStore()

const reload = () => {
    recomStore.resetUserSetGenre()
    router.push({name : "recommend"})
}
</script>

<style>
.reload-button {
    background-color: #1B1B1B; /* 배경색 */
    color: white; /* 글자색 */
    padding: 15px 32px; /* 상하 좌우 패딩 */
    text-align: center; /* 텍스트 가운데 정렬 */
    text-decoration: none; /* 텍스트 밑줄 제거 */
    display: inline-block; /* 인라인 블록 요소로 표시 */
    font-size: 16px; /* 글자 크기 */
    margin: 4px 2px; /* 마진 */
    cursor: pointer; /* 커서 모양을 포인터로 설정 */
    border: none; /* 테두리 없음 */
    border-radius: 12px; /* 테두리 둥근 모서리 */
    transition-duration: 0.4s; /* 전환 효과 시간 */
}

.reload-button:hover {
    background-color: #45a049; /* 호버 시 배경색 변경 */
}
</style>
