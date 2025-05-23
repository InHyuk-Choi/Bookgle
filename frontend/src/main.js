import './assets/main.css'
import { createApp } from 'vue'
import App from './App.vue'
import { createPinia } from 'pinia'
import router from './router'
import { setupAxiosInterceptor } from './stores/interceptor'

setupAxiosInterceptor()

const app = createApp(App)
const pinia = createPinia()
app.use(pinia)
app.use(router)

import { useAuthStore } from '@/stores/auth'

// ✅ authStore는 여기서 실행 (mount 전에)
const authStore = useAuthStore()
authStore.initAuth()

app.mount('#app')   // ✅ 마지막에 mount
