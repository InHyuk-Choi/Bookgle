import { createRouter, createWebHistory } from 'vue-router'

import HomeView from '@/views/Homeview.vue'
import SignInView from '@/views/SignInView.vue'
import SignUpView from '@/views/SignUpView.vue'
import ProfileView from '@/views/ProfileView.vue'
import StoreView from '@/views/StoreView.vue'

const routes = [
  { path: '/', name: 'home', component: HomeView },
  { path: '/signin', name: 'signin', component: SignInView },
  { path: '/signup', name: 'signup', component: SignUpView },
  { path: '/profile', name: 'profile', component: ProfileView },
  { path: '/store', name: 'store', component: StoreView },
  {
  path: '/profile/upload',
  name: 'profile-upload',
  component: () => import('@/views/ProfileImageUpload.vue'),
},
{
  path: '/profile/following',
  name: 'following-list',
  component: () => import('@/views/FollowListView.vue'),
  meta: {
    title: '팔로잉 목록',
    apiUrl: 'http://localhost:8000/api/v1/accounts/following/<user_id>/', // 이 부분 실제 user_id로 교체 필요
  }
},
{
  path: '/profile/followers',
  name: 'follower-list',
  component: () => import('@/views/FollowListView.vue'),
  meta: {
    title: '팔로워 목록',
    apiUrl: 'http://localhost:8000/api/v1/accounts/followers/<user_id>/', // 이 부분 실제 user_id로 교체 필요
  }
}
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
