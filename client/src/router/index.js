import { createRouter, createWebHistory } from 'vue-router'
import Home from '@/views/Home.vue'
import SearchResults from '@/views/SearchResults.vue'
import MovieDetail from '@/views/MovieDetail'
import UserProfile from '@/views/UserProfile'
import MyProfile from '@/views/MyProfile'
import ReviewDetail from '@/views/ReviewDetail'
import SetUser from '@/views/SetUser'
import NotFoundPage from '@/views/NotFoundPage'

const routes = [
  {
    path: '/',
    name: 'Home',
    component: Home
  },
  {
    path: '/search/:searchInput',
    name: 'SearchResults',
    component: SearchResults,
  },
  {
    path: '/moviedetail/:movieId',
    name: 'MovieDetail',
    component: MovieDetail,
  },
  {
    path: '/accounts/profile/:userId',
    name: 'UserProfile',
    component: UserProfile,
  },
  {
    path: '/accounts/profile/myprofile/',
    name: 'MyProfile',
    component: MyProfile,
  },
  {
    path: '/review/:reviewId',
    name: 'ReviewDetail',
    component: ReviewDetail,
  },
  {
    path: '/accounts/SetUser',
    name: 'SetUser',
    component: SetUser,
  },
  {
    path: '/:catchAll(.*)',
    redirect: '/404',
  },
  {
    path: '/404',
    name: 'NotFoundPage',
    component: NotFoundPage,
  },
]

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
})

export default router
