<template>
  <div class="landing">
    <!-- Hero-секция -->
    <section class="hero">
      <div class="hero-content">
        <h1 class="title">Откройте мир с нами!</h1>
        <p class="subtitle">Лучшие туры по выгодным ценам</p>
        <!-- <button @click="router.push('/tours')" class="cta-button">Смотреть все туры</button> -->
        <router-link :to="{ name: 'tours' }" class="cta-button">Смотреть все туры</router-link>
      </div>
    </section>

    <!-- Популярные направления -->
    <section class="destinations" ref="toursSection">
      <h2>Популярные туры</h2>
      <div v-if="isLoading" class="loading">Загрузка...</div>
      <div v-else-if="error" class="error">{{ error }}</div>
      <TourSlider v-else :tours="tours" @tour-click="gotoURL" />
    </section>

    <!-- Преимущества -->
    <section class="benefits">
      <h2>Почему выбирают нас?</h2>
      <div class="benefits-grid">
        <div v-for="(benefit, index) in benefits" :key="index" class="benefit">
          <div class="icon">{{ benefit.icon }}</div>
          <h3>{{ benefit.title }}</h3>
          <p>{{ benefit.text }}</p>
        </div>
      </div>
    </section>

    <Footer :companyName="'TravelApp'" :email="'smth@gmail.com'" :phone="'+7-(999)-999-99-99'" :adrres="'Близжайшая мусорная яма'"/>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import TourSlider from '../components/Slider.vue'
import Footer from '../components/Footer.vue'
import { api } from '../api/api.js'
import { useRouter } from 'vue-router'

const toursSection = ref(null)
const email = ref('')
const tours = ref([])
const isLoading = ref(true)
const error = ref(null)

const router = useRouter()

// Загрузка туров
const fetchTours = async () => {
  try {
    const response = await api.get('tour/popular/')
    tours.value = response.data
  } catch (err) {
    console.error('Ошибка загрузки туров:', err)
    error.value = 'Не удалось загрузить популярные туры'
  } finally {
    isLoading.value = false
  }
}

onMounted(() => {
  fetchTours()
})

const benefits = ref([
  { icon: '✈️', title: 'Авиабилеты', text: 'Прямые рейсы от проверенных авиакомпаний' },
  { icon: '🏨', title: 'Отели', text: 'Только лучшие отели с высоким рейтингом' },
  { icon: '🛡️', title: 'Страховка', text: 'Медицинская страховка в подарок' }
])

const scrollToTours = () => {
  toursSection.value?.scrollIntoView({ behavior: 'smooth' })
}

const submitForm = () => {
  alert(`Спасибо! Мы свяжемся с вами на ${email.value}`)
  email.value = ''
}

const gotoURL = (slug) => {
  router.push(`/tours/${slug}`)
}

const handleImageError = (event) => {
  const defaultImage = '/images/default-tour.jpg'
  if (event.target.src !== defaultImage) {
    event.target.src = defaultImage
  }
}
</script>

<style scoped>
.landing {
  font-family: 'Arial', sans-serif;
  color: #333;
  height: 100vh;
  width: 100vw;
}

.hero {
  background: linear-gradient(rgba(0, 0, 0, 0.5), rgba(0, 0, 0, 0.5)),
    url('../assets/hero.jpeg') no-repeat center/cover;
  height: 100vh;
  width: 100vw;
  display: flex;
  align-items: center;
  justify-content: center;
  text-align: center;
  color: white;
}

.hero-content {
  max-width: 800px;
  padding: 20px;
}

.title {
  font-size: 3rem;
  margin-bottom: 1rem;
}

.subtitle {
  font-size: 1.5rem;
  margin-bottom: 2rem;
}

.cta-button {
  background: #ff5722;
  color: white;
  border: none;
  padding: 12px 30px;
  font-size: 1.2rem;
  border-radius: 30px;
  cursor: pointer;
  transition: all 0.3s;
}

.cta-button:hover {
  background: #e64a19;
  transform: translateY(-3px);
}

section {
  /* padding: 80px 20px; */
  width: 100vw;
  text-align: center;
  align-items: center;
  justify-content: center;
}

.benefits,
.destinations,
.contacts {
  position: relative;
  max-width: 1200px;
  margin: 0 auto;
  padding: 40px 20px;
}

h2 {
  font-size: 2.5rem;
  margin-bottom: 50px;
}

.benefits-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 30px;
  max-width: 1200px;
  margin: 0 auto;
  justify-content: center;
}

.benefit {
  padding: 20px;
}

.icon {
  font-size: 2.5rem;
  margin-bottom: 20px;
}
</style>