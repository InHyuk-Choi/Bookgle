import { createRouter, createWebHistory } from 'vue-router'

import HomeView from '@/views/Homeview.vue'
import SignInView from '@/views/SignInView.vue'
import SignUpView from '@/views/SignUpView.vue'
import ProfileView from '@/views/ProfileView.vue'
import StoreView from '@/views/StoreView.vue'
import FeedView from '@/views/FeedView.vue'
import FeedWriteView from '@/views/FeedWriteView.vue'
import RankingView from '@/views/RankingView.vue'
import FollowListView from '@/views/FollowListView.vue'
import BookSearchView from '@/views/BookSearchView.vue'


const routes = [
  { path: '/', name: 'home', component: HomeView },
  { path: '/signin', name: 'signin', component: SignInView },
  { path: '/signup', name: 'signup', component: SignUpView },
  { path: '/profile', name: 'profile', component: ProfileView },
  { path: '/store', name: 'store', component: StoreView },
  
{
  path: '/followers/:username',
  name: 'followers',
  component: FollowListView,
  meta: {
    type: 'followers',
    title: '팔로워 목록'
  }
},
{
  path: '/following/:username',
  name: 'following',
  component: FollowListView,
  meta: {
    type: 'following',
    title: '팔로잉 목록'
  }
},
{ path: '/feed', name: 'feed', component: FeedView },

{ path: '/feed/write', name: 'feed-write', component: FeedWriteView },
{
  path: '/feeds/:id',
  name: 'feed-detail',
  component: () => import('@/views/FeedDetailView.vue'),
  props: true,
},
  {
    path: '/ranking',
    name: 'ranking',
    component: RankingView,
  },
 {
  path: '/user/:username',
  name: 'UserProfile',
  component: () => import('@/views/OthersProfileView.vue'),
  props: true,
  beforeEnter: (to, from, next) => {
    const currentUsername = localStorage.getItem('currentUsername')
    if (to.params.username === currentUsername) {
      next({ name: 'profile' })
    } else {
      next()
    }
  }
},
{ path: '/books/search', name: 'book-search', component: BookSearchView },
{
  path: '/quiz',
  name: 'QuizView',
  component: () => import('@/views/QuizView.vue'),
},




]
const router = createRouter({
  history: createWebHistory(),
  routes,
})

router.beforeEach((to, from, next) => {
  const publicPages = ['signin', 'signup']
  const isAuthRequired = !publicPages.includes(to.name)
  const hasToken = !!localStorage.getItem('access')

  if (isAuthRequired && !hasToken) {
    next({ name: 'signin' })
  } else {
    next()
  }
})

export default router
