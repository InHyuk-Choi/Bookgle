import { createRouter, createWebHistory } from 'vue-router'

import HomeView from '@/views/HomeView.vue'
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
