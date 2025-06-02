<template>
  <Header />

  <div class="cart-page">
    <h1 class="page-title">Корзина туров</h1>

    <div v-if="loading" class="loading">Загрузка...</div>

    <div v-else-if="error" class="error-message">
      {{ error }}
      <button @click="fetchCart" class="retry-button">Попробовать снова</button>
    </div>

    <template v-else>
      <!-- Основное содержимое корзины -->
      <div class="cart-content">
        <div class="cart-items">
          <!-- Заголовки таблицы -->
          <div class="cart-header">
            <div class="header-item">Тур</div>
            <div class="header-item">Статус</div>
            <div class="header-item">Количество</div>
            <div class="header-item">Цена</div>
            <div class="header-item">Действия</div>
          </div>

          <!-- Список туров в корзине -->
          <div v-for="item in cartItems" :key="item.id" class="cart-item">
            <div class="item-info">
              <router-link :to="`/tours/${item.tour.slug}/`" class="tour-link">
                <img :src="item.tour.img_preview_url" :alt="item.tour.title" class="tour-image">
                <span class="tour-title">{{ item.tour.title }}</span>
              </router-link>
            </div>

            <div class="item-status">
              <span :class="`status-badge status-${item.status}`">
                {{ item.status_name }}
              </span>
            </div>

            <div class="item-quantity">
              <button @click="updateQuantity(item.id, item.count - 1)" :disabled="item.count <= 1"
                class="quantity-button">
                -
              </button>
              <span class="quantity">{{ item.count }}</span>
              <button @click="updateQuantity(item.id, item.count + 1)" :disabled="item.count >= item.target"
                class="quantity-button">
                +
              </button>
            </div>

            <div class="item-price">
              {{ formatPrice(item.tour.price * item.count) }} ₽
            </div>

            <div class="item-actions">
              <button @click="removeItem(item.id)" class="remove-button">
                Удалить
              </button>
            </div>
          </div>
        </div>

        <!-- Итоговая информация -->
        <div class="cart-summary">
          <div class="summary-row">
            <span>Количество туров:</span>
            <span>{{ cartCount }}</span>
          </div>
          <div class="summary-row total">
            <span>Итого:</span>
            <span>{{ formatPrice(totalPrice) }} ₽</span>
          </div>

          <button @click="proceedToCheckout" :disabled="!canCheckout" class="checkout-button">
            Оформить заказ
          </button>

          <router-link to="/tours" class="continue-shopping">
            Продолжить выбор туров
          </router-link>
        </div>
      </div>

      <!-- Пустая корзина -->
      <div v-if="cartCount === 0" class="empty-cart">
        <img src="../assets/images/empty-cart.svg" alt="Корзина пуста" class="empty-image">
        <h2>Ваша корзина пуста</h2>
        <p>Добавьте туры, чтобы продолжить</p>
        <router-link to="/tours" class="browse-tours">
          Посмотреть туры
        </router-link>
      </div>
    </template>
  </div>

  <Footer :companyName="'TravelApp'" :email="'smth@gmail.com'" :phone="'+7-(999)-999-99-99'"
    :adrres="'Близжайшая мусорная яма'" />
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { authApi } from '../api/api'
import Header from '../components/Header.vue'
import Footer from '../components/Footer.vue'

const cartItems = ref([])
const loading = ref(true)
const error = ref(null)

// Загрузка корзины
const fetchCart = async () => {
  try {
    loading.value = true
    error.value = null
    const response = await authApi.get('reservation/')
    cartItems.value = response.data.results
  } catch (err) {
    error.value = 'Не удалось загрузить корзину'
    console.error('Ошибка загрузки корзины:', err)
  } finally {
    loading.value = false
  }
}

// Обновление количества
const updateQuantity = async (itemId, newQuantity) => {
  try {
    await authApi.patch('reservation/update/', { count: newQuantity, id: itemId })
    fetchCart() // Обновляем данные
  } catch (err) {
    console.error('Ошибка обновления количества:', err)
  }
}

// Удаление элемента
const removeItem = async (itemId) => {
  try {
    await authApi.delete('reservation/delete/', { id: itemId })
    fetchCart() // Обновляем данные
  } catch (err) {
    console.error('Ошибка удаления:', err)
  }
}

// Оформление заказа
const proceedToCheckout = () => {
  // Здесь будет переход на страницу оформления
  console.log('Переход к оформлению')
}

// Форматирование цены
const formatPrice = (price) => {
  return new Intl.NumberFormat('ru-RU').format(parseFloat(price))
}

// Вычисляемые свойства
const cartCount = computed(() => cartItems.value.length)

const totalPrice = computed(() => {
  return cartItems.value.reduce((sum, item) => {
    return sum + (parseFloat(item.tour.price) * item.count)
  }, 0)
})

const canCheckout = computed(() => {
  return cartCount.value > 0 &&
    cartItems.value.every(item => item.status === 4) // 4 = waiting
})

onMounted(fetchCart)
</script>

<style scoped>
.cart-page {
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
  min-height: calc(100vh - 40px - 74px - 317px);
}

.page-title {
  font-size: 2rem;
  margin-bottom: 30px;
  color: #333;
  text-align: center;
}

.loading,
.error-message {
  text-align: center;
  padding: 40px;
  font-size: 1.2rem;
}

.error-message {
  color: #dc3545;
}

.retry-button {
  margin-top: 15px;
  padding: 8px 16px;
  background: #ff5722;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

.cart-content {
  display: flex;
  gap: 30px;
}

.cart-items {
  flex: 2;
}

.cart-summary {
  flex: 1;
  background: #f9f9f9;
  padding: 20px;
  border-radius: 8px;
  height: fit-content;
}

.cart-header {
  display: flex;
  padding: 15px 10px;
  background: #f5f5f5;
  border-radius: 6px;
  margin-bottom: 10px;
  font-weight: 500;
}

.header-item {
  flex: 1;
  text-align: center;
}

.header-item:first-child {
  flex: 2;
  text-align: left;
}

.cart-item {
  display: flex;
  align-items: center;
  padding: 15px 10px;
  border-bottom: 1px solid #eee;
}

.item-info {
  flex: 2;
}

.tour-link {
  display: flex;
  align-items: center;
  text-decoration: none;
  color: #333;
}

.tour-image {
  width: 80px;
  height: 60px;
  object-fit: cover;
  border-radius: 4px;
  margin-right: 15px;
}

.tour-title {
  font-weight: 500;
}

.tour-title:hover {
  color: #ff5722;
}

.item-status,
.item-quantity,
.item-price,
.item-actions {
  flex: 1;
  text-align: center;
}

.status-badge {
  padding: 4px 8px;
  border-radius: 12px;
  font-size: 0.8rem;
  font-weight: 500;
}

.status-4 {
  /* waiting */
  background: #e3f2fd;
  color: #1976d2;
}

.status-5 {
  /* confirmed */
  background: #e8f5e9;
  color: #388e3c;
}

.status-6 {
  /* cancelled */
  background: #ffebee;
  color: #d32f2f;
}

.quantity-button {
  width: 30px;
  height: 30px;
  border: 1px solid #ddd;
  background: white;
  border-radius: 4px;
  cursor: pointer;
  font-size: 1rem;
}

.quantity-button:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.quantity {
  display: inline-block;
  width: 30px;
  text-align: center;
}

.remove-button {
  padding: 6px 12px;
  background: #ffebee;
  color: #d32f2f;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 0.9rem;
}

.remove-button:hover {
  background: #ffcdd2;
}

.summary-row {
  display: flex;
  justify-content: space-between;
  margin-bottom: 12px;
  padding-bottom: 12px;
  border-bottom: 1px solid #eee;
}

.summary-row.total {
  font-size: 1.2rem;
  font-weight: bold;
  margin: 20px 0;
  padding-bottom: 0;
  border-bottom: none;
}

.checkout-button {
  width: 100%;
  padding: 12px;
  background: #ff5722;
  color: white;
  border: none;
  border-radius: 4px;
  font-size: 1rem;
  cursor: pointer;
  margin-bottom: 15px;
  transition: background 0.3s;
}

.checkout-button:hover {
  background: #e64a19;
}

.checkout-button:disabled {
  background: #ccc;
  cursor: not-allowed;
}

.continue-shopping,
.browse-tours {
  display: block;
  text-align: center;
  color: #ff5722;
  text-decoration: none;
  margin-top: 10px;
}

.continue-shopping:hover,
.browse-tours:hover {
  text-decoration: underline;
}

.empty-cart {
  text-align: center;
  padding: 40px 0;
}

.empty-image {
  width: 200px;
  height: auto;
  margin-bottom: 20px;
}

.empty-cart h2 {
  font-size: 1.5rem;
  margin-bottom: 10px;
  color: #333;
}

.empty-cart p {
  color: #666;
  margin-bottom: 20px;
}

.browse-tours {
  display: inline-block;
  padding: 10px 20px;
  background: #ff5722;
  color: white;
  border-radius: 4px;
  text-decoration: none;
}

@media (max-width: 768px) {
  .cart-content {
    flex-direction: column;
  }

  .cart-header {
    display: none;
  }

  .cart-item {
    flex-direction: column;
    align-items: flex-start;
    gap: 15px;
    padding: 20px;
    border: 1px solid #eee;
    border-radius: 8px;
    margin-bottom: 15px;
  }

  .item-info,
  .item-status,
  .item-quantity,
  .item-price,
  .item-actions {
    width: 100%;
    text-align: left;
  }

  .item-actions {
    text-align: center;
  }
}
</style>