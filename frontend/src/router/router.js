import { createRouter, createWebHistory } from 'vue-router'
import LandingPage from '../views/LandingPage.vue'

const routes = [
  { path: '/', component: LandingPage },
  { path: '/landing', component: LandingPage}
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router