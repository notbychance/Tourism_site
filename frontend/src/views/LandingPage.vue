<template>
  <div class="landing">
    <!-- Hero-секция -->
    <section class="hero">
      <div class="hero-content">
        <h1 class="title">Откройте мир с нами!</h1>
        <p class="subtitle">Лучшие туры по выгодным ценам</p>
        <button @click="scrollToTours" class="cta-button">Выбрать тур</button>
      </div>
    </section>

    <!-- Популярные направления -->
    <section class="destinations" ref="toursSection">
      <h2>Популярные направления</h2>
      <div class="cards">
        <div v-if="isLoading">Загрузка...</div>
        <div v-else>
          <div v-for="tour in tours" :key="tour.id" class="tour-card" @click="gotoURL(tour.slug)">
            <img :src="tour.image" :alt="tour.title">
            <h3>{{ tour.title }}</h3>
            <p>{{ tour.short_description }}</p>
            <span class="price">{{ tour.price.toLocaleString() }} ₽</span>
          </div>
        </div>
      </div>
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

    <!-- Контакты -->
    <section class="contacts">
      <h2>Остались вопросы?</h2>
      <form @submit.prevent="submitForm">
        <input v-model="email" type="email" placeholder="Ваш email">
        <button type="submit">Отправить</button>
      </form>
    </section>
  </div>
</template>

<script>
import { ref } from 'vue'
import { api } from '../api/api.js'

export default {
  name: 'LandingPage',
  setup() {
    const toursSection = ref(null);
    const email = ref('');
    const tours = ref([]);
    const isLoading = ref(true);
    
    const fetchTours = async () => {
      try {
        isLoading.value = true;
        const response = await api.get('/tour/popular');
        tours.value = response.data;
      } catch (err) {
        console.error('Ошибка загрузки туров:', err);
      } finally {
        isLoading.value = false;
      }
    };
    fetchTours();

    const benefits = [
      { icon: '✈️', title: 'Авиабилеты', text: 'Прямые рейсы от проверенных авиакомпаний' },
      { icon: '🏨', title: 'Отели', text: 'Только лучшие отели с высоким рейтингом' },
      { icon: '🛡️', title: 'Страховка', text: 'Медицинская страховка в подарок' }
    ];

    const scrollToTours = () => {
      toursSection.value?.scrollIntoView({ behavior: 'smooth' });
    };

    const submitForm = () => {
      alert(`Спасибо! Мы свяжемся с вами на ${email.value}`);
      email.value = '';
    };

    const gotoURL = (slug) => {
      window.location.href = `/${slug}`;
    };

    return { tours, isLoading, benefits, email, toursSection, scrollToTours, submitForm, gotoURL };
  }
};
</script>

<style scoped>
.landing {
  font-family: 'Arial', sans-serif;
  color: #333;
}

.hero {
  background: linear-gradient(rgba(0, 0, 0, 0.5), rgba(0, 0, 0, 0.5)), 
              url('../media/hero.jpeg') no-repeat center/cover;
  height: 100vh;
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
  padding: 80px 20px;
  text-align: center;
}

h2 {
  font-size: 2.5rem;
  margin-bottom: 50px;
}

.cards {
  display: flex;
  justify-content: center;
  gap: 30px;
  flex-wrap: wrap;
}

.tour-card {
  width: 300px;
  border-radius: 10px;
  overflow: hidden;
  box-shadow: 0 5px 15px rgba(0, 0, 0, 0.1);
  transition: transform 0.3s;
  cursor: pointer;
}

.tour-card:hover {
  transform: translateY(-10px);
}

.tour-card img {
  width: 100%;
  height: 200px;
  object-fit: cover;
}

.price {
  display: block;
  font-weight: bold;
  color: #ff5722;
  font-size: 1.2rem;
  margin-top: 10px;
}

.benefits-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 30px;
  max-width: 1200px;
  margin: 0 auto;
}

.benefit {
  padding: 20px;
}

.icon {
  font-size: 2.5rem;
  margin-bottom: 20px;
}

form {
  max-width: 500px;
  margin: 0 auto;
  display: flex;
}

input {
  width: 70%;
  padding: 12px;
  border: 1px solid #ddd;
  border-radius: 30px 0 0 30px;
  outline: none;
}

button[type="submit"] {
  width: 30%;
  padding: 12px;
  background: #ff5722;
  color: white;
  border: none;
  border-radius: 0 30px 30px 0;
  cursor: pointer;
}
</style>