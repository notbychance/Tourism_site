<template>
    <Header />

    <div class="tour-page">
        <!-- Хлебные крошки -->
        <!-- <nav class="breadcrumbs">
      <router-link to="/">Главная</router-link> /
      <router-link :to="`/country/${tour.basic_info.country_slug}`">{{ tour.basic_info.country_name }}</router-link> /
      <router-link :to="`/company/${tour.basic_info.company_slug}`">{{ tour.basic_info.company_name }}</router-link> /
      <span>{{ tour.basic_info.title }}</span>
    </nav> -->

        <!-- Основная информация -->
        <section class="tour-header">
            <div class="tour-images">
                <img :src="tour.detailed_info.img_background_url" :alt="tour.basic_info.title" class="background-image">
                <img :src="tour.detailed_info.img_url" :alt="tour.basic_info.title" class="main-image">
            </div>

            <div class="tour-basic-info">
                <h1>{{ tour.basic_info.title }}</h1>
                <div class="meta-info">
                    <span class="company">
                        <router-link :to="`/company/${tour.basic_info.company_slug}`">
                            {{ tour.basic_info.company_name }}
                        </router-link>
                    </span>
                    <span class="country">
                        <div>
                            {{ tour.basic_info.country_name }}
                        </div>
                        <!-- <router-link :to="`/tours/?country=${tour.basic_info.country_name}`">
                            {{ tour.basic_info.country_name }}
                        </router-link> -->
                    </span>
                    <span class="favorites">
                        ♡ {{ tour.basic_info.favourites_count }}
                    </span>
                </div>

                <div class="short-description">
                    {{ tour.basic_info.short_description }}
                </div>

                <div class="price-section">
                    <div class="price">{{ formatPrice(tour.basic_info.price) }} ₽</div>
                    <button class="book-button" @click="openBookingModal">Забронировать</button>
                </div>
            </div>
        </section>

        <!-- Детальная информация -->
        <section class="tour-details">
            <div class="details-column">
                <h2>Описание тура</h2>
                <p class="description">{{ tour.detailed_info.description }}</p>

                <h2>Места посещения</h2>
                <div class="places">
                    {{ tour.detailed_info.placed }}
                </div>
            </div>

            <div class="timing-column">
                <h2>Даты и места</h2>
                <div class="timing-info">
                    <div class="timing-item">
                        <span class="label">Дата начала:</span>
                        <span class="value">{{ formatDate(tour.time_spans.date_from) }}</span>
                    </div>
                    <div class="timing-item">
                        <span class="label">Дата окончания:</span>
                        <span class="value">{{ formatDate(tour.time_spans.date_to) }}</span>
                    </div>
                    <div class="timing-item">
                        <span class="label">Группа:</span>
                        <span class="value">{{ tour.time_spans.group_name }}</span>
                    </div>
                    <div class="timing-item">
                        <span class="label">Свободных мест:</span>
                        <span class="value">{{ tour.time_spans.place_count - tour.time_spans.places_released }}</span>
                    </div>
                </div>

                <div class="action-buttons">
                    <button class="favorite-button" @click="toggleFavorite">
                        {{ isFavorite ? '★ В избранном' : '☆ Добавить в избранное' }}
                    </button>
                    <button class="share-button" @click="shareTour">
                        Поделиться
                    </button>
                </div>
            </div>
        </section>

        <!-- Модальное окно бронирования -->
        <!-- <BookingModal 
      v-if="showBookingModal"
      :tour="tour"
      @close="closeBookingModal"
    /> -->
    </div>

    <Footer :companyName="'TravelApp'" :email="'smth@gmail.com'" :phone="'+7-(999)-999-99-99'"
        :adrres="'Близжайшая мусорная яма'" />
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { api, authApi } from '../api/api.js'
import Header from '../components/Header.vue'
import Footer from '../components/Footer.vue'
import Cookies from 'js-cookie'
// import BookingModal from '@/components/BookingModal.vue'

const route = useRoute()
const tour = ref({
    basic_info: {},
    detailed_info: {},
    time_spans: {}
})
const isLoading = ref(true)
const error = ref(null)
const isFavorite = ref(false)
const showBookingModal = ref(false)

const fetchTour = async () => {
    try {
        const response = await api.get(`tour/${route.params.slug}/full/`)
        tour.value = response.data
        checkFavoriteStatus()
    } catch (err) {
        error.value = 'Не удалось загрузить информацию о туре'
    } finally {
        isLoading.value = false
    }
}

const checkFavoriteStatus = async () => {
    try {
        const response = await (Cookies.get('refresh_token') ? authApi : api).get(`favourites/${route.params.slug}/`)
        isFavorite.value = response.data.is_favorite
    } catch (err) {
        console.error('Ошибка проверки избранного:', err)
    }
}

const toggleFavorite = async () => {
    try {
        const method = isFavorite.value ? 'delete' : 'post'
        await authApi[method](`favourites/${route.params.slug}/`)
        isFavorite.value = !isFavorite.value
        // Обновляем счетчик
        if (isFavorite.value) {
            tour.value.basic_info.favourites_count++
        } else {
            tour.value.basic_info.favourites_count--
        }
    } catch (err) {
        console.error('Ошибка изменения избранного:', err)
    }
}

const shareTour = () => {
    if (navigator.share) {
        navigator.share({
            title: tour.value.basic_info.title,
            text: tour.value.basic_info.short_description,
            url: window.location.href
        }).catch(err => console.log('Ошибка sharing:', err))
    } else {
        // Fallback для браузеров без поддержки Web Share API
        alert('Скопируйте ссылку из адресной строки')
    }
}

const formatPrice = (price) => {
    return new Intl.NumberFormat('ru-RU').format(parseFloat(price))
}

const formatDate = (dateString) => {
    const options = { year: 'numeric', month: 'long', day: 'numeric' }
    return new Date(dateString).toLocaleDateString('ru-RU', options)
}

const openBookingModal = () => {
    showBookingModal.value = true
}

const closeBookingModal = () => {
    showBookingModal.value = false
}

onMounted(fetchTour)
</script>

<style scoped>
.tour-page {
    max-width: 1200px;
    margin: 0 auto;
    padding: 20px;
}

.breadcrumbs {
    margin-bottom: 20px;
    font-size: 0.9rem;
    color: #666;
}

.breadcrumbs a {
    color: #ff5722;
    text-decoration: none;
}

.breadcrumbs a:hover {
    text-decoration: underline;
}

.tour-header {
    display: flex;
    gap: 30px;
    margin-bottom: 40px;
}

.tour-images {
    position: relative;
    flex: 1;
    min-height: 400px;
}

.background-image {
    width: 100%;
    height: 100%;
    object-fit: cover;
    border-radius: 8px;
    filter: brightness(0.7);
}

.main-image {
    position: absolute;
    bottom: -30px;
    right: -30px;
    width: 60%;
    max-width: 400px;
    height: auto;
    border-radius: 8px;
    border: 3px solid white;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
}

.tour-basic-info {
    flex: 1;
    display: flex;
    flex-direction: column;
}

h1 {
    font-size: 2.2rem;
    margin-bottom: 15px;
    color: #333;
}

.meta-info {
    display: flex;
    gap: 15px;
    margin-bottom: 20px;
    font-size: 0.9rem;
    color: #666;
}

.meta-info a {
    color: #ff5722;
    text-decoration: none;
}

.meta-info a:hover {
    text-decoration: underline;
}

.favorites {
    margin-left: auto;
}

.short-description {
    font-size: 1.1rem;
    line-height: 1.6;
    margin-bottom: 30px;
    color: #444;
}

.price-section {
    margin-top: auto;
    display: flex;
    align-items: center;
    gap: 20px;
}

.price {
    font-size: 1.8rem;
    font-weight: bold;
    color: #ff5722;
}

.book-button {
    padding: 12px 25px;
    background-color: #ff5722;
    color: white;
    border: none;
    border-radius: 4px;
    font-size: 1rem;
    cursor: pointer;
    transition: background-color 0.3s;
}

.book-button:hover {
    background-color: #e64a19;
}

.tour-details {
    display: flex;
    gap: 40px;
    margin-top: 50px;
}

.details-column {
    flex: 2;
}

.timing-column {
    flex: 1;
}

h2 {
    font-size: 1.5rem;
    margin-bottom: 15px;
    color: #333;
    border-bottom: 2px solid #eee;
    padding-bottom: 8px;
}

.description {
    line-height: 1.7;
    margin-bottom: 30px;
    color: #555;
}

.places {
    background: #f9f9f9;
    padding: 15px;
    border-radius: 6px;
    line-height: 1.6;
}

.timing-info {
    background: #f5f5f5;
    padding: 20px;
    border-radius: 8px;
}

.timing-item {
    display: flex;
    justify-content: space-between;
    margin-bottom: 12px;
    padding-bottom: 12px;
    border-bottom: 1px solid #eee;
}

.timing-item:last-child {
    margin-bottom: 0;
    padding-bottom: 0;
    border-bottom: none;
}

.label {
    font-weight: 500;
    color: #666;
}

.value {
    font-weight: 600;
    color: #333;
}

.action-buttons {
    display: flex;
    flex-direction: column;
    gap: 10px;
    margin-top: 20px;
}

.favorite-button,
.share-button {
    padding: 10px 15px;
    border: 1px solid #ddd;
    background: white;
    border-radius: 4px;
    cursor: pointer;
    transition: all 0.3s;
}

.favorite-button {
    color: #ff5722;
    border-color: #ff5722;
}

.favorite-button:hover {
    background: #fff0e6;
}

.share-button:hover {
    background: #f5f5f5;
}

@media (max-width: 768px) {
    .tour-header {
        flex-direction: column;
    }

    .tour-details {
        flex-direction: column;
    }

    .main-image {
        position: relative;
        bottom: 0;
        right: 0;
        width: 100%;
        max-width: none;
        margin-top: 20px;
    }
}
</style>