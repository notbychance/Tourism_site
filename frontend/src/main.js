import { createApp } from 'vue'
import './style.css'
import Landing from './views/LandingPage.vue'
import router from './router/router.js'
import { register } from 'swiper/element/bundle'

// Регистрируем Swiper элементы
register()

const app = createApp(Landing)
app.use(router)
app.mount('#app')
