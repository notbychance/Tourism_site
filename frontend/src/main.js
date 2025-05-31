import { createApp } from 'vue'
import './style.css'
import App from './App.vue'
import router from './router/router.js'
import { register } from 'swiper/element/bundle'

// Регистрируем Swiper элементы
register()

const app = createApp(App)
app.use(router)
app.mount('#app')
