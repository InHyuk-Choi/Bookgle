import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import axios from 'axios'

export const useAuthStore = defineStore('auth', () => {
  const username = ref('')
  const password1 = ref('')
  const password2 = ref('')
  const nickname = ref('')
  const readPages = ref(0)
  const totalPoints = ref(0)
  const followersCount = ref(0)
  const followingCount = ref(0)
  const isLoading = ref(true)
  const basicFood = ref(0)
  const premiumFood = ref(0)
  const profileImage = ref('')
  const userId = ref(0)
  const currentBookTitle = ref('')
  const bookworm = ref({
    name: '',
    level: 1,
    experience: 0,
    exp_to_next: 100,
    progress: 0,
  })
const currentBook = ref({
  title: '',
  isbn: '',
  author: '',
  publisher: '',
  cover_image: '',
  description: ''
})


const kakaoLogin = async (router, Swal, kakaoAccessToken) => {
  try {
    const res = await axios.post('http://localhost:8000/api/v1/accounts/kakao/login/', {
  access_token: kakaoAccessToken,
}, {
  withCredentials: true  // ✅ 쿠키 포함
})

    // ✅ JWT 저장
    setAccessToken(res.data.access)
    localStorage.setItem('refresh', res.data.refresh)
    isAuthenticated.value = true

    await fetchUserStatus()
    await fetchBookwormStatus()

    await Swal.fire({
      icon: 'success',
      title: '카카오 로그인 성공!',
      text: '환영합니다 😊',
      confirmButtonText: '확인',
      customClass: { confirmButton: 'custom-ok-button-blue' }
    })

    router.push({ name: 'home' })
  } catch (err) {
    console.error('카카오 로그인 실패:', err.response?.data)
    Swal.fire({
      icon: 'error',
      title: '카카오 로그인 실패',
      text: err.response?.data?.error || '카카오 로그인 처리 중 오류가 발생했습니다.',
      confirmButtonText: '확인',
      customClass: { confirmButton: 'custom-ok-button-red' }
    })
  }
}

  const fetchBookwormStatus = async () => {
    try {
      const res = await axios.get('http://localhost:8000/api/v1/kkubook/bookworm/status/')
      bookworm.value = res.data
    } catch (err) {
      console.error('책벌레 상태 조회 실패:', err)
    }
  }

  const feedBookworm = async (type) => {
    try {
      const res = await axios.post('http://localhost:8000/api/v1/kkubook/bookworm/feed/', {
        type
      })

      bookworm.value.level = res.data.level
      bookworm.value.experience = res.data.experience
      bookworm.value.exp_to_next = res.data.exp_to_next
      bookworm.value.progress = Math.round(res.data.experience / res.data.exp_to_next * 1000) / 1000
      basicFood.value = res.data.basic_food
      premiumFood.value = res.data.premium_food
      profileImage.value = res.data.profile_image 

    } catch (err) {
      console.error('먹이 주기 실패:', err)
    }
  }

  const purchaseFood = async ({ type, quantity, cost }) => {
    try {
      const res = await axios.post('http://localhost:8000/api/v1/accounts/food/purchase/', {
        type, quantity, cost
      })

      totalPoints.value = res.data.total_points
      basicFood.value = res.data.basic_food
      premiumFood.value = res.data.premium_food
    } catch (err) {
      console.error('먹이 구매 실패:', err)
    }
  }

  const isAuthenticated = ref(false)
  const isLoggedIn = computed(() => isAuthenticated.value)

  const setAccessToken = (accessToken) => {
    localStorage.setItem('access', accessToken)
    axios.defaults.headers.common['Authorization'] = `Bearer ${accessToken}`
  }

  const initAuth = async () => {
    const token = localStorage.getItem('access')
    if (token) {
      setAccessToken(token)
      isAuthenticated.value = true
      await fetchUserStatus()
      await fetchBookwormStatus()
    } else {
      isAuthenticated.value = false
    }
    isLoading.value = false
  }

  const fetchUserStatus = async () => {
    try {
      const res = await axios.get('http://localhost:8000/api/v1/accounts/me/', {
        withCredentials: true
      })
      username.value = res.data.username
      localStorage.setItem('currentUsername', res.data.username)
      totalPoints.value = res.data.total_points
      nickname.value = res.data.nickname 
      readPages.value = res.data.read_pages
      followersCount.value = res.data.followers_count
      followingCount.value = res.data.following_count
      basicFood.value = res.data.basic_food
      premiumFood.value = res.data.premium_food
      profileImage.value = res.data.profile_image
      userId.value = res.data.id
      currentBookTitle.value = res.data.current_book_title
      currentBook.value = res.data.currentBook || {
  title: '', isbn: '', author: '', publisher: '', cover_image: '', description: ''
}


    } catch (err) {
      console.error('유저 상태 조회 실패:', err)
    }
  }

  const login = async (router, Swal) => {
    try {
      const res = await axios.post('http://localhost:8000/api/v1/accounts/custom-login/', {
        username: username.value,
        password: password1.value,
      }, { withCredentials: true })

      setAccessToken(res.data.access)
      isAuthenticated.value = true
      await new Promise(resolve => setTimeout(resolve, 100))

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

  const logout = async (Swal, router) => {
    localStorage.removeItem('access')
    delete axios.defaults.headers.common['Authorization']
    isAuthenticated.value = false

    username.value = ''
    password1.value = ''
    password2.value = ''
    nickname.value = ''

    if (Swal && router) {
      await Swal.fire({
        icon: 'success',
        title: '로그아웃 완료!',
        text: '다음에 또 만나요 😊',
        confirmButtonText: '확인',
        customClass: {
          confirmButton: 'custom-ok-button-blue',
        }
      })
      router.push({ name: 'signin' })
    }
  }

  const signup = async (router, Swal) => {
    if (!nickname.value.trim()) {
      return Swal.fire({
        icon: 'error',
        title: '닉네임 필수!',
        text: '닉네임을 입력해주세요.',
        confirmButtonText: '확인',
        customClass: { confirmButton: 'custom-ok-button-red' }
      })
    }

    if (password1.value !== password2.value) {
      return Swal.fire({
        icon: 'error',
        title: '비밀번호 불일치!',
        text: '비밀번호가 서로 다릅니다.',
        confirmButtonText: '확인',
        customClass: { confirmButton: 'custom-ok-button-red' }
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
      console.error('회원가입 실패:', err.response?.data)
      Swal.fire({
        icon: 'error',
        title: '회원가입 실패',
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
    readPages, totalPoints, isAuthenticated,
    isLoggedIn, profileImage,followersCount,currentBook,
  followingCount, userId, kakaoLogin,
    login, signup, logout, fetchUserStatus, initAuth,
    basicFood, premiumFood, bookworm, fetchBookwormStatus, feedBookworm, purchaseFood, currentBookTitle
  }
})
