import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '@/views/HomeView.vue'
import SignUpView from '@/views/accounts/SignUpView.vue'
import LogInView from '@/views/accounts/LogInView.vue'
import CommuView from '@/views/community/CommuView.vue'
import CommuArticleCreateView from '@/views/community/CommuArticleCreateView.vue'
import LogOug from '@/components/accounts/LogOut.vue'
import PasswordChange from '@/components/accounts/PasswordChange.vue'
import ActorView from '@/views/actors/ActorView.vue'
import RecommendView from '@/views/recommend/RecommendView.vue'
import CommuArticleDetail from '@/views/community/CommuArticleDetail.vue'
import ProfileView from '@/views/profile/ProfileView.vue'
import MovieView from '@/views/movie/MovieView.vue'
import Review from '@/views/review/Review.vue'
import WeatherRecommendView from '@/views/recommend/WeatherRecommendView.vue'
import ReviewDetail from '@/views/review/ReviewDetail.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomeView
    },

    // ACTOR
    {
      path: '/actors',
      name: 'actor',
      component: ActorView
    },

    // COMMUNITY
    {
      path: '/community',
      name: 'community',
      component: CommuView,
    },
    {
      path: '/community/create',
      name: 'create',
      component: CommuArticleCreateView
    },
    {
      path: '/community/:id',
      name: 'articleDetail',
      component: CommuArticleDetail
    },

    // RECOMMEND
    {
      path: '/movies/recommend',
      name: 'recommend',
      component: RecommendView
    },
    {
      path: '/movies/recommend/weather',
      name: 'weather',
      component: WeatherRecommendView
    },

    // ACCOUNT
    {
      path: '/signup',
      name: 'signup',
      component: SignUpView
    },
    {
      path: '/login',
      name: 'login',
      component: LogInView
    },
    {
      path: '/accounts/logout',
      name: 'logout',
      component: LogOug
    },
    {
      path: '/accounts/password/reset',
      name: 'passwordchange',
      component: PasswordChange
    },
    {
      path: '/profile/:id',
      name: 'profile',
      component: ProfileView
    },

    // Movie
    {
      path: '/movies/:id',
      name: 'movieDetail',
      component: MovieView
    },
    
    // Review
    {
      path: '/reviews/:id',
      name: 'review',
      component: Review
    },
    {
      path: '/reviews/detail/:review_id',
      name:'reviewDetail',
      component: ReviewDetail
    }
  ]
})

export default router