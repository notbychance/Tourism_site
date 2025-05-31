import { createRouter, createWebHistory  } from 'vue-router'
import LandingPage from '../views/LandingPage.vue'
import TourList from '../views/TourList.vue'
import TourPage from '../views/TourPage.vue'

const routes = [
  { path: '/tours', name:'tours', component: TourList },
  { path: '/tours/:slug', component:TourPage },
  { path: '/', name:'main', component: LandingPage, exact: true },
]

const router = createRouter({
  history: createWebHistory (),
  routes
})

export default router