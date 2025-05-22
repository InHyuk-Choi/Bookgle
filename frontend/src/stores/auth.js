import { defineStore } from 'pinia'
import { ref } from 'vue'
import axios from 'axios'

export const useAuthStore = defineStore('auth', () => {
  const username = ref('')
  const password1 = ref('')
  const password2 = ref('')
  const nickname = ref('')
  const readPages = ref(0)
  const totalPoints = ref(0)

  // 토큰 저장 및 헤더 설정
  const setAuthToken = (accessToken) => {
    localStorage.setItem('access', accessToken)
    axios.defaults.headers.common['Authorization'] = `Bearer ${accessToken}`
  }

  const initAuth = () => {
    const token = localStorage.getItem('access')
    if (token) {
      axios.defaults.headers.common['Authorization'] = `Bearer ${token}`
    }
  } 


  // 사용자 정보 로드
  const fetchUserStatus = async () => {
    try {
      const res = await axios.get('http://localhost:8000/api/v1/accounts/me/', {
        headers: {
          Authorization: `Bearer ${localStorage.getItem('access')}`,
        }
      })
      console.log(res.data)
      totalPoints.value = res.data.total_points
      readPages.value = res.data.read_pages
    } catch (err) {
      console.error('사용자 정보 조회 실패:', err)
    }
  }

  // 로그인
  const login = async (router, Swal) => {
    try {
      const res = await axios.post('http://localhost:8000/api/v1/accounts/token/', {
        username: username.value,
        password: password1.value,
      })

      setAuthToken(res.data.access)
      localStorage.setItem('refresh', res.data.refresh)

      await fetchUserStatus()

      await Swal.fire({
        icon: 'success',
        title: '로그인 성공!',
        text: '환영합니다!',
        confirmButtonText: '확인',
        customClass: { confirmButton: 'custom-ok-button-blue' }
      })

      router.push({ name: 'home' })
    } catch (err) {
      Swal.fire({
        icon: 'error',
        title: '로그인 실패!',
        text: '아이디 또는 비밀번호를 확인해주세요.',
        confirmButtonText: '확인',
        customClass: { confirmButton: 'custom-ok-button-red' }
      })
    }
  }

  // 회원가입
  const signup = async (router, Swal) => {
    if (!nickname.value.trim()) {
      return Swal.fire({
        icon: 'error',
        title: '닉네임 필수!',
        text: '닉네임을 입력해주세요.',
        confirmButtonText: '확인',
        customClass: { confirmButton: 'custom-ok-button-red' },
      })
    }
    console.log(password1)

    if (password1.value !== password2.value) {
      return Swal.fire({
        icon: 'error',
        title: '비밀번호 불일치!',
        text: '비밀번호가 서로 다릅니다.',
        confirmButtonText: '확인',
        customClass: { confirmButton: 'custom-ok-button-red' },
      })
    }

    try {
      await axios.post('http://localhost:8000/api/v1/accounts/registration/', {
        username: username.value,
        email: `${username.value}@kkubook.com`,
        password1: password1.value,
        password2: password2.value,
        nickname: nickname.value,
      })

      await login(router, Swal)
    } catch (err) {
      console.error('회원가입 실패 응답:', err.response?.data)
      Swal.fire({
        icon: 'error',
        title: '에러!',
        text: err.response?.data?.nickname?.[0] ||
              err.response?.data?.username?.[0] ||
              err.response?.data?.email?.[0] ||
              err.response?.data?.non_field_errors?.[0] ||
              '회원가입에 실패했습니다.',
        confirmButtonText: '확인',
        customClass: { confirmButton: 'custom-ok-button-red' }
      })
    }
  }

  return {
    username, password1, password2, nickname,
    readPages, totalPoints,
    login, signup, fetchUserStatus, initAuth
  }
})
