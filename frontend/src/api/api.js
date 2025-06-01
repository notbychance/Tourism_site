import axios from 'axios'
import Cookies from 'js-cookie'

const api = axios.create({
  baseURL: 'http://127.0.0.1:8000/api/',
  headers: {
    'Content-Type': 'application/json',
    'Accept': 'application/json',
  }
})

const authApi = axios.create({
  baseURL: 'http://127.0.0.1:8000/api/',
  headers: {
    'Content-Type': 'application/json',
    'Accept': 'application/json',
  },
  withCredentials: true
})

// Request interceptor for authApi
authApi.interceptors.request.use(
  (config) => {
    const token = Cookies.get('access_token')
    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    }
    return config
  },
  (error) => {
    return Promise.reject(error)
  }
)

// Response interceptor for authApi
authApi.interceptors.response.use(
  (response) => response,
  async (error) => {
    const originalRequest = error.config

    if (!error.response) {
      return Promise.reject(error)
    }

    if (error.response.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true

      const refreshToken = Cookies.get('refresh_token')

      if (!refreshToken) {
        Cookies.remove('access_token')
        Cookies.remove('refresh_token')

        return Promise.reject(error)
      }

      try {
        alert(refreshToken)
        const response = await axios.post('http://127.0.0.1:8000/api/token/refresh/', 
          { refresh: refreshToken },
          {
            headers: {
              'Content-Type': 'application/json',
              'Accept': 'application/json'
            },
            withCredentials: true
          }
        )

        const { access } = response.data
        alert(JSON.stringify(response.data))

        Cookies.set('access_token', access, { expires: 1 / 48 })

        originalRequest.headers.Authorization = `Bearer ${access}`
        return authApi(originalRequest)
      } catch (refreshError) {
        console.error('Refresh token failed:', refreshError)

        Cookies.remove('access_token')
        Cookies.remove('refresh_token')

        return Promise.reject(refreshError)
      }
    }

    // Handle other error statuses
    // switch (error.response.status) {
    //   case 403:  // Forbidden
    //     console.error('Forbidden:', error.response.data)
    //     break
    //   case 404:  // Not Found
    //     console.error('Not Found:', error.response.data)
    //     break
    //   case 500:  // Server Error
    //     console.error('Server Error:', error.response.data)
    //     break
    //   default:
    //     console.error('Unhandled Error:', error.response.data)
    // }

    return Promise.reject(error)
  }
)

export { api, authApi }