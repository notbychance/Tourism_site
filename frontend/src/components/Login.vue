<template>
    <div class="auth-form">
        <h2>Вход</h2>
        <form @submit.prevent="handleLogin">
            <div class="form-group">
                <label>Логин:</label>
                <input v-model="form.login" type="text" required placeholder="ivan_2023">
            </div>

            <div class="form-group">
                <label>Пароль:</label>
                <input v-model="form.password" type="password" required placeholder="securepassword123">
            </div>

            <button type="submit" :disabled="loading">
                {{ loading ? 'Вход...' : 'Войти' }}
            </button>

            <p v-if="error" class="error">{{ error }}</p>
        </form>
    </div>
</template>

<script>
import { api } from '../api/api.js'
import Cookie from 'js-cookie'

export default {
    data() {
        return {
            form: {
                login: '',
                password: ''
            },
            loading: false,
            error: ''
        }
    },
    methods: {
        async handleLogin() {
            this.loading = true
            this.error = ''

            try {
                const response = await api.post('login/', {
                    login: this.form.login,
                    password: this.form.password
                })

                // Сохраняем токен (пример для JWT)
                Cookie.set('access_token', response.data.tokens.access, { expires: 1/48 })
                Cookie.set('refresh_token', response.data.tokens.refresh, { expires: 14 })

                // Перенаправление после успешного входа
                this.$router.push('/tours');
            } catch (err) {
                if (err.response) {
                    this.error = err.response.data.message || 'Неверный логин или пароль'
                } else {
                    this.error = 'Не удалось подключиться к серверу'
                }
            } finally {
                this.loading = false
            }
        }
    }
}
</script>

<style scoped>
/* Стили аналогичные Register.vue */
.auth-form {
    max-width: 400px;
    margin: 0 auto;
    padding: 20px;
    border: 1px solid #ddd;
    border-radius: 5px;
}

.form-group {
    margin-bottom: 15px;
}

label {
    display: block;
    margin-bottom: 5px;
}

input {
    width: 100%;
    padding: 8px;
    border: 1px solid #ddd;
    border-radius: 4px;
}

button {
    width: 100%;
    padding: 10px;
    background-color: #42b983;
    color: white;
    border: none;
    border-radius: 4px;
    cursor: pointer;
}

button:disabled {
    background-color: #cccccc;
}

.error {
    color: #ff4444;
    margin-top: 5px;
}
</style>