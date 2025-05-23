// src/interceptor.js (예시)

import axios from 'axios'
import router from '@/router'

let isInitialized = false
const REFRESH_URL = 'http://localhost:8000/api/v1/accounts/token/refresh/'

export function setupAxiosInterceptor() {
  if (isInitialized) return
  isInitialized = true

  axios.interceptors.response.use(
    res => res,
    async err => {
      const originalRequest = err.config

      // 🔁 refresh 요청 자체는 인터셉터 제외
      if (originalRequest.url === REFRESH_URL) {
        return Promise.reject(err)
      }

      // 🔁 access 토큰 만료 시 재시도
      if (
        err.response?.status === 401 &&
        !originalRequest._retry
      ) {
        originalRequest._retry = true

        try {
          const res = await axios.post(
            REFRESH_URL,
            {},
            {
              withCredentials: true,
              headers: {
                // ✅ 기존 Authorization 헤더 제거
                'Authorization': null
              }
            }
          )

          const newAccess = res.data.access
          localStorage.setItem('access', newAccess)

          // ✅ 기본 헤더 갱신
          axios.defaults.headers.common['Authorization'] = `Bearer ${newAccess}`

          // ✅ 원래 요청에도 새 토큰 반영
          if (!originalRequest.headers) {
            originalRequest.headers = {}
          }
          originalRequest.headers['Authorization'] = `Bearer ${newAccess}`

          return axios(originalRequest)
        } catch (refreshErr) {
          console.error('🔁 자동 토큰 갱신 실패:', refreshErr)

          // ⛔ 로그아웃 처리
          localStorage.removeItem('access')
          axios.defaults.headers.common['Authorization'] = null
          router.push({ name: 'signin' })
        }
      }

      return Promise.reject(err)
    }
  )
}
