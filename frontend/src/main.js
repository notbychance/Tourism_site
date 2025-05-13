import { createApp } from 'vue'
import './style.css'
import Landing from './views/LandingPage.vue'
import router from './router/router.js'

const app = createApp(Landing)
app.use(router)
app.mount('#app')
