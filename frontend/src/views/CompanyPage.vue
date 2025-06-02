<template>
  <Header />

  <div class="company-page">
    <!-- Шапка компании -->
    <div class="company-header">
      <div class="company-image-container">
        <img :src="company.image" :alt="company.name" class="company-image" />
      </div>
      <div class="company-info">
        <h1>{{ company.name }}</h1>
        <p class="company-description">{{ company.description }}</p>

        <div class="company-contacts">
          <div class="contact-item">
            <i class="fas fa-phone"></i>
            <span>{{ formatPhone(company.phone) }}</span>
          </div>
          <div class="contact-item">
            <i class="fas fa-map-marker-alt"></i>
            <span>{{ company.address }}</span>
          </div>
        </div>
      </div>
    </div>

    <!-- Социальные сети -->
    <section class="company-section">
      <h2>Мы в социальных сетях</h2>
      <div class="social-media-grid">
        <a v-for="social in company.social_media" :key="social.media_type" :href="social.reference" target="_blank"
          class="social-media-card" :class="`social-type-${social.media_type}`">
          <div class="social-media-icon">
            <i :class="getSocialIcon(social.media_type)"></i>
          </div>
          <div class="social-media-info">
            <span class="social-name">{{ social.media_type_name }}</span>
            <span class="social-days">Действует ещё {{ social.days_remaining }} дней</span>
          </div>
        </a>
      </div>
    </section>

    <!-- Туры компании -->
    <section class="company-section">
      <h2>Наши туры</h2>
      <div class="tours-grid">
        <router-link v-for="tour in company.tours" :key="tour.slug" :to="`/tours/${tour.slug}`" class="tour-card">
          <div class="tour-image-container">
            <img :src="tour.img_preview_url" :alt="tour.title" class="tour-image" />
          </div>
          <div class="tour-info">
            <h3>{{ tour.title }}</h3>
            <p class="tour-description">{{ tour.short_description }}</p>
            <div class="tour-price">{{ formatPrice(tour.price) }} ₽</div>
          </div>
        </router-link>
      </div>
    </section>
  </div>

  <Footer :companyName="'TravelApp'" :email="'smth@gmail.com'" :phone="'+7-(999)-999-99-99'"
    :adrres="'Близжайшая мусорная яма'" />
</template>

<script>
import Header from '../components/Header.vue'
import Footer from '../components/Footer.vue'
import { useRouter } from 'vue-router'
import { api } from '../api/api'

export default {
  name: 'CompanyPage',
  components: { Header, Footer },
  data() {
    return {
      company: {
        social_media: [],
        tours: [],
        name: '',
        phone: '',
        address: '',
        slug: '',
        description: '',
        image: ''
      }
    }
  },
  created() {
    this.fetchCompanyData()
  },
  methods: {
    async fetchCompanyData() {
      try {
        // Замените на ваш реальный API endpoint
        const response = await api.get(`company/${this.$route.params.slug}/`)
        this.company = await response.data
      } catch (error) {
        console.error('Ошибка при загрузке данных компании:', error)
      }
    },
    formatPhone(phone) {
      return phone.replace(/(\d{1})(\d{3})(\d{3})(\d{2})(\d{2})/, '+$1 ($2) $3-$4-$5')
    },
    formatPrice(price) {
      return parseFloat(price).toLocaleString('ru-RU')
    },
    getSocialIcon(mediaType) {
      switch (mediaType) {
        case 1: return 'fab fa-facebook-f'
        case 2: return 'fab fa-instagram'
        case 3: return 'fab fa-twitter'
        case 4: return 'fab fa-youtube'
        case 5: return 'fab fa-vk'
        case 6: return 'fab fa-telegram'
        default: return 'fas fa-share-alt'
      }
    }
  }
}
</script>

<style scoped>
.company-page {
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
}

.company-header {
  display: flex;
  gap: 30px;
  margin-bottom: 40px;
  align-items: flex-start;
}

.company-image-container {
  flex: 0 0 300px;
}

.company-image {
  width: 100%;
  border-radius: 8px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.company-info {
  flex: 1;
}

.company-description {
  color: #555;
  font-size: 1.1rem;
  line-height: 1.6;
  margin: 15px 0;
}

.company-contacts {
  margin-top: 20px;
}

.contact-item {
  display: flex;
  align-items: center;
  margin-bottom: 10px;
  color: #333;
}

.contact-item i {
  margin-right: 10px;
  color: #4a6baf;
  width: 20px;
  text-align: center;
}

.company-section {
  margin-bottom: 50px;
}

.company-section h2 {
  border-bottom: 2px solid #4a6baf;
  padding-bottom: 8px;
  margin-bottom: 20px;
  color: #333;
}

.social-media-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
  gap: 20px;
}

.social-media-card {
  display: flex;
  align-items: center;
  padding: 15px;
  border-radius: 8px;
  text-decoration: none;
  color: white;
  transition: transform 0.2s;
}

.social-media-card:hover {
  transform: translateY(-3px);
}

.social-type-1 {
  background-color: #3b5998;
}

/* Facebook */
.social-type-2 {
  background: linear-gradient(45deg, #405de6, #5851db, #833ab4, #c13584, #e1306c, #fd1d1d);
}

/* Instagram */
.social-type-3 {
  background-color: #1da1f2;
}

/* Twitter */
.social-type-4 {
  background-color: #ff0000;
}

/* YouTube */
.social-type-5 {
  background-color: #45668e;
}

/* VK */
.social-type-6 {
  background-color: #0088cc;
}

/* Telegram */

.social-media-icon {
  font-size: 24px;
  margin-right: 15px;
  width: 40px;
  height: 40px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.social-media-info {
  display: flex;
  flex-direction: column;
}

.social-name {
  font-weight: bold;
  margin-bottom: 5px;
}

.social-days {
  font-size: 0.8rem;
  opacity: 0.9;
}

.tours-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(350px, 1fr));
  gap: 25px;
}

.tour-card {
  display: flex;
  flex-direction: column;
  border-radius: 8px;
  overflow: hidden;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  text-decoration: none;
  color: inherit;
  transition: transform 0.2s, box-shadow 0.2s;
}

.tour-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 8px 16px rgba(0, 0, 0, 0.15);
}

.tour-image-container {
  height: 200px;
  overflow: hidden;
}

.tour-image {
  width: 100%;
  height: 100%;
  object-fit: cover;
  transition: transform 0.3s;
}

.tour-card:hover .tour-image {
  transform: scale(1.05);
}

.tour-info {
  padding: 20px;
  flex: 1;
  display: flex;
  flex-direction: column;
}

.tour-info h3 {
  margin: 0 0 10px 0;
  color: #2c3e50;
}

.tour-description {
  color: #555;
  margin: 0 0 15px 0;
  flex: 1;
}

.tour-price {
  font-weight: bold;
  color: #4a6baf;
  font-size: 1.2rem;
  margin-top: auto;
}

@media (max-width: 768px) {
  .company-header {
    flex-direction: column;
  }

  .company-image-container {
    flex: 0 0 auto;
    width: 100%;
  }

  .tours-grid {
    grid-template-columns: 1fr;
  }
}
</style>