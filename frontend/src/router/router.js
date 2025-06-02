import { createRouter, createWebHistory } from 'vue-router'
import LandingPage from '../views/LandingPage.vue'
import TourListPage from '../views/TourListPage.vue'
import TourPage from '../views/TourPage.vue'
import AuthPage from '../views/AuthPage.vue'
import FavouritePage from '../views/FavouritePage.vue'
import ProfilePage from '../views/ProfilePage.vue'
import CompanyListPage from '../views/CompanyListPage.vue'
import CompanyPage from '../views/CompanyPage.vue'
import CartPage from '../views/CartPage.vue'

const routes = [
  { path: '/cart', name: 'cart', component: CartPage },
  { path: '/company/:slug', component: CompanyPage },
  { path: '/company', name: 'companies', component: CompanyListPage },
  { path: '/tours/:slug', component: TourPage },
  { path: '/tours', name: 'tours', component: TourListPage },
  { path: '/auth', name: "auth", component: AuthPage },
  { path: '/wishlist', name: 'wishlist', component: FavouritePage },
  { path: '/account', name: 'account', component: ProfilePage },
  { path: '/', name: 'main', component: LandingPage, exact: true },
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router