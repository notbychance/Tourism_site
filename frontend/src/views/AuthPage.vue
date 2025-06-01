<template>
  <div class="auth-container">
    <div class="auth-switcher">
      <button @click="setActiveForm('login')" :class="{ active: activeForm === 'login' }">
        Вход
      </button>
      <button @click="setActiveForm('register')" :class="{ active: activeForm === 'register' }">
        Регистрация
      </button>
    </div>

    <transition name="fade" mode="out-in">
      <LoginForm v-if="activeForm === 'login'"/>
      <RegisterForm v-else/>
    </transition>
  </div>
</template>

<script>
import LoginForm from '../components/Login.vue'
import RegisterForm from '../components/Register.vue'
import { useRouter } from 'vue-router'
import { ref } from 'vue'

const activeForm = ref('login')

export default {
  components: { LoginForm, RegisterForm },
  data() {
    return {
      activeForm: 'login' // По умолчанию показываем форму входа
    }
  },
  methods: {
    setActiveForm(form) {
      this.activeForm = form
    },
    handleLoginSuccess() {
      // Перенаправление после успешного входа
      this.$router.push('/dashboard')
    },
    handleRegisterSuccess() {
      // После регистрации можно автоматически войти или переключить на логин
      this.setActiveForm('login')
      // Или показать сообщение о успешной регистрации
    }
  },
  created() {
    // Опционально: проверяем query-параметр для определения начальной формы
    if (this.$route.query.form === 'register') {
      this.activeForm = 'register'
    }
  }
}
</script>

<style scoped>
.auth-container {
  max-width: 400px;
  margin: 0 auto;
  padding: 20px;
}

.auth-switcher {
  display: flex;
  margin-bottom: 20px;
  border-bottom: 1px solid #eee;
}

.auth-switcher button {
  flex: 1;
  padding: 10px;
  background: none;
  border: none;
  cursor: pointer;
  font-size: 16px;
  color: #666;
  position: relative;
}

.auth-switcher button.active {
  color: #42b983;
  font-weight: bold;
}

.auth-switcher button.active::after {
  content: '';
  position: absolute;
  bottom: -1px;
  left: 0;
  right: 0;
  height: 2px;
  background: #42b983;
}

.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.3s;
}

.fade-enter,
.fade-leave-to {
  opacity: 0;
}
</style>