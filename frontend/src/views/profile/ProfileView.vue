<template>
    <div>
        <ProfileDetailView
        :user="user"
        :user_id="user_id"
        />
    </div>
</template>

<script setup>
import ProfileDetailView from '@/components/profile/ProfileDetailView.vue'
import { onMounted, computed } from 'vue'
import { useRoute } from 'vue-router'
import { useProfileStore } from '@/stores/profileStore.js'

const route = useRoute()
const user_id = route.params.id
const profileStore = useProfileStore()
const username = profileStore.userName
const nickname = profileStore.nickName
const followers = profileStore.followers_count
const followings = profileStore.followings_count

const user = { username, nickname, followers, followings }
onMounted(() => {
    profileStore.getProfile(user_id)
})
</script>

<style scoped>

</style>
