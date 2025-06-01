<template>
    <Header />

    <div class="favorites-page">
        <div class="header">
            <h1>Избранное</h1>
            <div v-if="favorites.length > 0" class="actions">
                <button @click="clearAll" class="btn-clear" :disabled="loading">
                    Очистить всё
                </button>
            </div>
        </div>

        <div v-if="loading" class="loading">
            <div class="spinner"></div>
            <p>Загрузка избранного...</p>
        </div>

        <div v-else-if="favorites.length === 0" class="empty-state">
            <img src="../assets/empty-favorites.svg" alt="Нет избранных элементов">
            <h3>В избранном пока ничего нет</h3>
            <p>Добавляйте понравившиеся товары, чтобы они появились здесь</p>
            <router-link to="/tours" class="btn-primary">
                Перейти в каталог
            </router-link>
        </div>

        <div v-else class="favorites-list">
            <div v-for="item in favorites" :key="item.id" class="favorite-item">
                <router-link :to="`/tours/${item.tour_slug}`" class="item-link">
                    <img :src="item.tour_img" :alt="item.tour_title" class="item-image">
                    <div class="item-info">
                        <h3 class="item-title">{{ item.tour_title }}</h3>
                        <p class="item-price">{{ item.tour_price }} ₽</p>
                    </div>
                </router-link>
                <button @click="removeFromFavorites(item.id)" class="btn-remove">
                    <svg width="20" height="20" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                        <path d="M6 18L18 6M6 6L18 18" stroke="currentColor" stroke-width="2" stroke-linecap="round" />
                    </svg>
                </button>
            </div>
        </div>
    </div>

    <Footer :companyName="'TravelApp'" :email="'smth@gmail.com'" :phone="'+7-(999)-999-99-99'"
        :adrres="'Близжайшая мусорная яма'" />
</template>

<script>
import { authApi } from '../api/api'
import Header from '../components/Header.vue'
import Footer from '../components/Footer.vue'

export default {
    name: 'FavoritesPage',
    components: { Header, Footer },
    data() {
        return {
            favorites: [],
            loading: false,
            error: null
        }
    },
    created() {
        this.loadFavorites()
    },
    methods: {
        async loadFavorites() {
            this.loading = true
            this.error = null
            try {
                const response = await authApi.get('favourite/')
                this.favorites = response.data
            } catch (error) {
                console.error('Ошибка загрузки избранного:', error)
                this.error = 'Не удалось загрузить избранное'
            } finally {
                this.loading = false
            }
        },

        async removeFromFavorites(itemId) {
            try {
                await authApi.delete(`favourite/${itemId}/`)
                this.favorites = this.favorites.filter(item => item.id !== itemId)
            } catch (error) {
                console.error('Ошибка удаления:', error)
            }
        },

        async clearAll() {
            if (!confirm('Вы уверены, что хотите очистить всё избранное?')) return

            try {
                await authApi.delete('favourite/clear/')
                this.favorites = []
            } catch (error) {
                console.error('Ошибка очистки:', error)
            }
        }
    }
}
</script>

<style scoped>
.favorites-page {
    max-width: 1200px;
    margin: 0 auto;
    padding: 20px;
    min-height: calc(100vh - 74px - 317px - 40px);
}

.header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 30px;
}

.actions {
    display: flex;
    gap: 15px;
}

.btn-clear {
    padding: 8px 16px;
    background: #f8f8f8;
    border: 1px solid #e0e0e0;
    border-radius: 4px;
    cursor: pointer;
    transition: all 0.2s;
}

.btn-clear:hover {
    background: #f0f0f0;
}

.btn-clear:disabled {
    opacity: 0.6;
    cursor: not-allowed;
}

.loading {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    padding: 50px 0;
}

.spinner {
    width: 40px;
    height: 40px;
    border: 4px solid #f3f3f3;
    border-top: 4px solid #42b983;
    border-radius: 50%;
    animation: spin 1s linear infinite;
    margin-bottom: 15px;
}

@keyframes spin {
    0% {
        transform: rotate(0deg);
    }

    100% {
        transform: rotate(360deg);
    }
}

.empty-state {
    text-align: center;
    padding: 50px 0;
}

.empty-state img {
    max-width: 300px;
    margin-bottom: 20px;
}

.empty-state h3 {
    font-size: 1.5rem;
    margin-bottom: 10px;
}

.empty-state p {
    color: #666;
    margin-bottom: 20px;
}

.btn-primary {
    display: inline-block;
    padding: 10px 20px;
    background: #42b983;
    color: white;
    border-radius: 4px;
    text-decoration: none;
    transition: background 0.2s;
}

.btn-primary:hover {
    background: #3aa876;
}

.favorites-list {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
    gap: 20px;
}

.favorite-item {
    position: relative;
    border: 1px solid #eee;
    border-radius: 8px;
    overflow: hidden;
    transition: transform 0.2s, box-shadow 0.2s;
}

.favorite-item:hover {
    transform: translateY(-5px);
    box-shadow: 0 5px 15px rgba(0, 0, 0, 0.1);
}

.item-link {
    display: flex;
    flex-direction: column;
    height: 100%;
    text-decoration: none;
    color: inherit;
}

.item-image {
    width: 100%;
    height: 200px;
    object-fit: cover;
}

.item-info {
    padding: 15px;
}

.item-title {
    font-size: 1.1rem;
    margin-bottom: 8px;
}

.item-price {
    font-weight: bold;
    color: #42b983;
}

.btn-remove {
    position: absolute;
    top: 10px;
    right: 10px;
    width: 32px;
    height: 32px;
    background: rgba(255, 255, 255, 0.9);
    border: none;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    cursor: pointer;
    transition: all 0.2s;
}

.btn-remove:hover {
    background: rgba(255, 99, 71, 0.9);
    color: white;
}
</style>