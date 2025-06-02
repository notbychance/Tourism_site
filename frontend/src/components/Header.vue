<template>
  <header class="site-header">
    <div class="header-container">
      <!-- Левая часть: логотип и навигация -->
      <div class="left-section">
        <router-link to="/" class="logo">
          <!-- Замените на ваш логотип -->
          <span class="logo-text">TravelApp</span>
        </router-link>

        <nav class="main-nav">
          <router-link to="/tours" class="nav-link">Туры</router-link>
          <router-link to="/company" class="nav-link">Компании</router-link>
          <!-- Другие навигационные ссылки при необходимости -->
        </nav>
      </div>

      <!-- Правая часть: действия пользователя -->
      <div class="right-section">
        <!-- Корзина (только для авторизованных) -->
        <router-link v-if="isAuthenticated" to="/cart" class="action-icon" aria-label="Корзина">
          <i class="icon-cart"></i>
          <span v-if="cartCount > 0" class="badge">{{ cartCount }}</span>
        </router-link>

        <!-- Избранное (только для авторизованных) -->
        <router-link v-if="isAuthenticated" to="/wishlist" class="action-icon" aria-label="Избранное">
          <i class="icon-heart"></i>
        </router-link>

        <!-- Личный кабинет / Авторизация -->
        <div class="user-menu">
          <router-link v-if="isAuthenticated" to="/account" class="user-avatar">
            <img v-if="user.avatar" :src="user.avatar" :alt="user.name">
            <div v-else class="avatar-placeholder">
              {{ userInitials }}
            </div>
          </router-link>

          <div v-else class="auth-buttons">
            <router-link to="/auth" class="auth-link">Войти</router-link>
            <router-link to="/auth/?form=register" class="auth-link register">Регистрация</router-link>
          </div>
        </div>
      </div>
    </div>
  </header>
</template>

<script>
import { ref, computed, onMounted } from 'vue';
import { authApi } from '../api/api.js';
import Cookies from 'js-cookie';

export default {
  name: 'AppHeader',
  setup() {
    const isAuthenticated = ref(false);
    const user = ref({
      name: '',
      email: '',
      avatar: null
    });
    const cartCount = ref(0);

    // Проверка аутентификации
    const checkAuth = () => {
      const token = Cookies.get('refresh_token');
      isAuthenticated.value = !!token;
      return !!token;
    };

    // Загрузка данных пользователя
    const fetchUserData = async () => {
      if (!checkAuth()) return;

      try {
        const response = await authApi.get('auth/user/');
        user.value = response.data;
      } catch (error) {
        isAuthenticated.value = false;
      }
    };

    // Загрузка количества в корзине
    const fetchCartCount = async () => {
      if (!isAuthenticated.value) return;

      try {
        const response = await authApi.get('reservation/count/');
        cartCount.value = response.data.count;
      } catch (error) { }
    };

    // Инициалы пользователя для аватара
    const userInitials = computed(() => {
      if (!user.value.username) return 'U';
      const parts = user.value.username.split(' ');
      return parts
        .slice(0, 2)
        .map(p => p[0])
        .join('')
        .toUpperCase();
    });

    onMounted(() => {
      checkAuth();
      if (isAuthenticated.value) {
        fetchUserData();
        fetchCartCount();
      }
    });

    return {
      isAuthenticated,
      user,
      cartCount,
      userInitials
    };
  }
};
</script>

<style scoped>
.site-header {
  background-color: #ffffff;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
  position: sticky;
  top: 0;
  z-index: 1000;
}

.header-container {
  display: flex;
  justify-content: space-between;
  align-items: center;
  max-width: 1200px;
  margin: 0 auto;
  padding: 15px 20px;
}

.left-section {
  display: flex;
  align-items: center;
  gap: 40px;
}

.logo {
  font-size: 24px;
  font-weight: 700;
  color: #2c3e50;
  text-decoration: none;
}

.logo-text {
  color: #42b983;
}

.main-nav {
  display: flex;
  gap: 25px;
}

.nav-link {
  color: #2c3e50;
  text-decoration: none;
  font-weight: 500;
  font-size: 16px;
  position: relative;
  padding: 5px 0;
}

.nav-link:hover {
  color: #42b983;
}

.nav-link.router-link-active {
  color: #42b983;
}

.nav-link.router-link-active::after {
  content: '';
  position: absolute;
  bottom: 0;
  left: 0;
  width: 100%;
  height: 2px;
  background-color: #42b983;
}

.right-section {
  display: flex;
  align-items: center;
  gap: 20px;
}

.action-icon {
  position: relative;
  display: flex;
  align-items: center;
  justify-content: center;
  width: 36px;
  height: 36px;
  color: #2c3e50;
  text-decoration: none;
  border-radius: 50%;
  transition: all 0.3s ease;
}

.action-icon:hover {
  background-color: #f5f7fa;
  color: #42b983;
}

.badge {
  position: absolute;
  top: -5px;
  right: -5px;
  background-color: #e74c3c;
  color: white;
  font-size: 10px;
  font-weight: bold;
  min-width: 18px;
  height: 18px;
  border-radius: 9px;
  display: flex;
  justify-content: center;
  align-items: center;
  padding: 0 4px;
}

.user-avatar {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  overflow: hidden;
  display: flex;
  align-items: center;
  justify-content: center;
  background-color: #f1f5f9;
  border: 2px solid #e2e8f0;
  cursor: pointer;
  transition: all 0.3s ease;
}

.user-avatar:hover {
  border-color: #42b983;
}

.user-avatar img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.avatar-placeholder {
  font-weight: 600;
  font-size: 14px;
  color: #64748b;
}

.auth-buttons {
  display: flex;
  gap: 15px;
}

.auth-link {
  color: #2c3e50;
  text-decoration: none;
  font-weight: 500;
  padding: 8px 15px;
  border-radius: 4px;
  transition: all 0.3s ease;
}

.auth-link:hover {
  color: #42b983;
}

.auth-link.register {
  background-color: #42b983;
  color: white;
}

.auth-link.register:hover {
  background-color: #359a6d;
  color: white;
}

/* Иконки (замените на свои) */
.icon-cart::before {
  content: '🛒';
  font-size: 18px;
}

.icon-heart::before {
  content: '❤️';
  font-size: 18px;
}

/* Адаптивность */
@media (max-width: 768px) {
  .header-container {
    padding: 10px 15px;
  }

  .left-section {
    gap: 20px;
  }

  .main-nav {
    gap: 15px;
  }

  .auth-buttons {
    gap: 10px;
  }

  .auth-link {
    padding: 6px 10px;
    font-size: 14px;
  }
}
</style>