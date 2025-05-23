import axios from 'axios'
import Cookies from 'js-cookie'

const api = axios.create({
  baseURL: 'http://127.0.0.1:8000/api/',
  headers: {
    'Content-Type': 'application/json',    
    'X-CSRFToken': Cookies.get('csrftoken')
  }
})

// Только для маршрутов, требующих авторизации
const authApi = axios.create({
  baseURL: 'http://127.0.0.1:8000/api/',
  headers: {
    'Content-Type': 'application/json',
    'X-CSRFToken': Cookies.get('csrftoken')
  },
  withCredentials: true
})

// Интерцептор для authApi (добавляет токен)
authApi.interceptors.request.use(config => {
  const token = Cookies.get('access_token')
  if (token) {
    config.headers.Authorization = `Bearer ${token}`    
  }
  return config
})

// Интерцептор для обновления токена (только для authApi)
authApi.interceptors.response.use(
  response => response,
  async error => {
    if (error.response.status === 401 && !error.config._retry) {
      error.config._retry = true
      try {
        const { data } = await axios.post(
          'http://localhost:8000/api/token/refresh/',
          { refresh: Cookies.get('refresh_token') },
          { withCredentials: true }
        )
        Cookies.set('access_token', data.access)
        error.config.headers.Authorization = `Bearer ${data.access}`
        return authApi(error.config)
      } catch {
        Cookies.remove('access_token')
        window.location.href = '/login'
      }
    }
    return Promise.reject(error)
  }
)

export { api, authApi } // Два разных экземпляра