<template>
    <div class="auth-form">
        <h2>Регистрация</h2>
        <form @submit.prevent="handleRegister">
            <div class="form-group">
                <label>ФИО:</label>
                <input v-model="form.phone" type="text" required placeholder="Иван Иванов">
            </div>

            <div class="form-group">
                <label>Email:</label>
                <input v-model="form.email" type="email" required placeholder="ivan@example.com">
            </div>

            <div class="form-group">
                <label>Логин:</label>
                <input v-model="form.username" type="text" required placeholder="ivan_2023">
            </div>

            <div class="form-group">
                <label>Пароль:</label>
                <input v-model="form.password" type="password" required placeholder="securepassword123">
            </div>

            <div class="form-group">
                <label>Подтверждение пароля:</label>
                <input v-model="form.password_confirm" type="password" required placeholder="securepassword123"
                    @blur="validatePassword">
                <p v-if="passwordError" class="error">{{ passwordError }}</p>
            </div>

            <button type="submit" :disabled="loading">
                {{ loading ? 'Регистрация...' : 'Зарегистрироваться' }}
            </button>

            <p v-if="error" class="error">{{ error }}</p>
            <p v-if="success" class="success">{{ success }}</p>
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
                phone: '',
                email: '',
                username: '',
                password: ''
            },
            loading: false,
            error: '',
            success: '',
            passwordError: ''
        }
    },
    methods: {
        validatePassword() {
            if (this.form.password !== this.form.password_confirm) {
                this.passwordError = 'Пароли не совпадают'
                return false
            }
            this.passwordError = ''
            return true
        },
        async handleRegister() {
            if (!this.validatePassword()) return

            this.loading = true
            this.error = ''
            this.success = ''

            try {
                let response = await api.post('auth/register/', {
                    phone: this.form.phone,
                    email: this.form.email,
                    username: this.form.username,
                    password: this.form.password,
                })

                this.success = 'Регистрация успешна!'
                // Перенаправление или очистка формы

                response = await api.post('auth/login/', {
                    username: this.form.username,
                    password: this.form.password
                })
                Cookie.set('access_token', response.data.access, { expires: 14 })
                Cookie.set('refresh_token', response.data.refresh, { expires: 14 })

                this.$router.push('/tours');
            } catch (err) {
                if (err.response) {
                    this.error = err.response.data.message || 'Ошибка регистрации'
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

.success {
    color: #42b983;
    margin-top: 5px;
}
</style>