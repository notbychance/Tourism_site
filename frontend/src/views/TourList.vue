<template>
    <Header />

    <div class="tours-page">
        <!-- Фильтры -->
        <div class="filters-section">
            <div class="filter-group">
                <h3>Фильтры</h3>

                <!-- Фильтр по странам -->
                <div class="filter-item">
                    <label>Страны:</label>
                    <MultiSelect v-model="selectedCountries" :options="availableCountries" :enable-search="true" />
                </div>

                <!-- Ценовой диапазон -->
                <div class="filter-item">
                    <label>Ценовой диапазон:</label>
                    <div class="price-range">
                        <input type="number" v-model.number="minPrice" placeholder="От">
                        <span>-</span>
                        <input type="number" v-model.number="maxPrice" placeholder="До">
                    </div>
                </div>

                <!-- Кнопка применения фильтров -->
                <button class="apply-btn" @click="applyFilters">Применить фильтры</button>
            </div>
        </div>

        <!-- Список туров -->
        <div class="tours-container">
            <!-- Поиск -->
            <!-- <div class="search-box">
                <input type="text" v-model="searchQuery" placeholder="Поиск по названию или описанию"
                    @input="handleSearch">
            </div> -->

            <!-- Загрузка -->
            <div v-if="loading" class="loading">Загрузка туров...</div>

            <!-- Сообщение если ничего не найдено -->
            <div v-if="!loading && tours?.length === 0" class="no-results">
                Туры не найдены. Попробуйте изменить параметры поиска.
            </div>

            <!-- Список туров -->
            <div class="tour-list">
                <div v-for="tour in tours" :key="tour.id" class="tour-card">
                    <div class="tour-image">
                        <img :src="tour.image" :alt="tour.title">
                    </div>
                    <div class="tour-info">
                        <h3>{{ tour.title }}</h3>
                        <p class="tour-description">{{ tour.short_description }}</p>
                        <div class="tour-meta">
                            <span class="tour-country">{{ tour.country_name }}</span>
                            <span class="tour-price">{{ tour.price }} ₽</span>
                        </div>
                        <router-link :to="`/tours/${tour.slug}`" class="details-btn">Подробнее</router-link>
                    </div>
                </div>
            </div>

            <!-- Кнопка загрузки следующих туров -->
            <div class="load-more">
                <button v-if="hasNextPage" @click="loadMoreTours" :disabled="loadingMore">
                    {{ loadingMore ? 'Загрузка...' : 'Показать еще' }}
                </button>
            </div>
        </div>
    </div>

    <Footer :companyName="'TravelApp'" :email="'smth@gmail.com'" :phone="'+7-(999)-999-99-99'"
        :adrres="'Близжайшая мусорная яма'" />
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue';
import { api } from '../api/api.js';
import MultiSelect from '../components/MultiSelect.vue';
import Header from '../components/Header.vue';
import Footer from '../components/Footer.vue';

// Данные
const tours = ref([]);
const availableCountries = ref([]);
const selectedCountries = ref([]);
const minPrice = ref(null);
const maxPrice = ref(null);
// const searchQuery = ref('');
const currentPage = ref(1);
const hasNextPage = ref(false);
const loading = ref(false);
const loadingMore = ref(false);
const filtersApplied = ref(false);

// Загрузка начальных данных
const fetchInitialData = async () => {
    try {
        loading.value = true;

        // Параллельно получаем страны и туры
        const [countriesRes, toursRes] = await Promise.all([
            api.get('/country'),
            api.get('/tour', {
                params: { page: currentPage.value }
            })
        ]);

        availableCountries.value = countriesRes.data.map((country, index) => ({
            id: index + 1, // Генерируем id на основе индекса
            name: country.name
        }));
        tours.value = toursRes.data.results;
        hasNextPage.value = Boolean(toursRes.data.next);
    } catch (error) {
        console.error('Ошибка при загрузке данных:', error);
    } finally {
        loading.value = false;
    }
};

// Применение фильтров
const applyFilters = async () => {
    try {
        currentPage.value = 1;
        filtersApplied.value = true;
        loading.value = true;

        const params = buildParams();
        const response = await api.get('/tour', { params });

        tours.value = response.data.results;
        hasNextPage.value = Boolean(response.data.next);
    } catch (error) {
        console.error('Ошибка фильтрации:', error);
    } finally {
        loading.value = false;
    }
};

// Поиск с дебаунсом
let searchTimeout = null;
const handleSearch = () => {
    clearTimeout(searchTimeout);
    searchTimeout = setTimeout(() => {
        applyFilters();
    }, 500);
};

// Загрузка следующих туров
const loadMoreTours = async () => {
    try {
        loadingMore.value = true;
        currentPage.value += 1;

        const params = buildParams();
        params.page = currentPage.value;

        const response = await api.get('/tour', { params });

        tours.value = [...tours.value, ...response.data.results];
        hasNextPage.value = Boolean(response.data.next);
    } catch (error) {
        console.error('Ошибка загрузки:', error);
        currentPage.value -= 1;
    } finally {
        loadingMore.value = false;
    }
};

// Построение параметров запроса
const buildParams = () => {
    const params = {};

    if (selectedCountries.value.length > 0) {
        params.country = selectedCountries.value.map(c => c.name).join(',');
    }

    if (minPrice.value !== null) {
        params.min_price = minPrice.value;
    }

    if (maxPrice.value !== null) {
        params.max_price = maxPrice.value;
    }

    // if (searchQuery.value.trim() !== '') {
    //     params.search = searchQuery.value.trim();
    // }

    return params;
};

onMounted(fetchInitialData);
</script>

<style scoped>
.tours-page {
    display: flex;
    max-width: 1200px;
    margin: 0 auto;
    padding: 20px;
    gap: 30px;
    min-height: calc(100vh - 300px);
}

.filters-section {
    flex: 0 0 250px;
    background: #f8f9fa;
    padding: 20px;
    border-radius: 8px;
    height: fit-content;
}

.filter-group h3 {
    margin-top: 0;
    margin-bottom: 20px;
    padding-bottom: 10px;
    border-bottom: 1px solid #eee;
}

.filter-item {
    margin-bottom: 20px;
}

.filter-item label {
    display: block;
    margin-bottom: 8px;
    font-weight: 500;
}

.price-range {
    display: flex;
    gap: 10px;
    align-items: center;
}

.price-range input {
    width: 100%;
    padding: 8px;
    border: 1px solid #ddd;
    border-radius: 4px;
}

.apply-btn {
    width: 100%;
    padding: 10px;
    background: #42b983;
    color: white;
    border: none;
    border-radius: 4px;
    cursor: pointer;
    font-weight: 500;
    transition: background 0.3s;
}

.apply-btn:hover {
    background: #359a6d;
}

.tours-container {
    flex: 1;
}

.search-box {
    margin-bottom: 20px;
}

.search-box input {
    width: 100%;
    padding: 12px 15px;
    border: 1px solid #ddd;
    border-radius: 4px;
    font-size: 16px;
}

.tour-list {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
    gap: 25px;
}

.tour-card {
    background: white;
    border-radius: 8px;
    overflow: hidden;
    box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
    transition: transform 0.3s;
}

.tour-card:hover {
    transform: translateY(-5px);
}

.tour-image img {
    width: 100%;
    height: 180px;
    object-fit: cover;
}

.tour-info {
    padding: 15px;
}

.tour-info h3 {
    margin-top: 0;
    margin-bottom: 10px;
    font-size: 18px;
}

.tour-description {
    color: #555;
    font-size: 14px;
    margin-bottom: 15px;
    display: -webkit-box;
    line-clamp: 3;
    -webkit-line-clamp: 3;
    -webkit-box-orient: vertical;
    overflow: hidden;
}

.tour-meta {
    display: flex;
    justify-content: space-between;
    margin-bottom: 15px;
    font-size: 14px;
}

.tour-country {
    background: #eaf6ff;
    padding: 3px 8px;
    border-radius: 4px;
}

.tour-price {
    font-weight: bold;
    color: #42b983;
}

.details-btn {
    display: block;
    padding: 8px;
    background: #3498db;
    color: white;
    border: none;
    border-radius: 4px;
    cursor: pointer;
    transition: background 0.3s;
}

.details-btn:hover {
    background: #2980b9;
}

.load-more {
    margin-top: 30px;
    text-align: center;
}

.load-more button {
    padding: 10px 25px;
    background: #f1f1f1;
    border: none;
    border-radius: 4px;
    cursor: pointer;
    font-size: 16px;
    transition: background 0.3s;
}

.load-more button:hover:not(:disabled) {
    background: #e0e0e0;
}

.load-more button:disabled {
    opacity: 0.7;
    cursor: not-allowed;
}

.loading,
.no-results {
    text-align: center;
    padding: 40px;
    font-size: 18px;
    color: #777;
}
</style>