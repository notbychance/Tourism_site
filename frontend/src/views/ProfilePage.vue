<template>
    <Header />

    <div class="profile-page">
        <div class="profile-header">
            <h1>Мой профиль</h1>
            <button @click="toggleEditMode" class="btn-edit">
                {{ editMode ? 'Отменить' : 'Редактировать' }}
            </button>
        </div>

        <div class="profile-content">
            <!-- Аватар -->
            <div class="avatar-section">
                <div class="avatar-wrapper">
                    <img :src="user.avatar || '../assets/default-avatar.png'" alt="Аватар" class="avatar">
                    <input v-if="editMode" type="file" ref="avatarInput" accept="image/*" @change="handleAvatarChange"
                        class="avatar-input">
                </div>
                <button v-if="editMode && user.avatar" @click="removeAvatar" class="btn-remove-avatar">
                    Удалить аватар
                </button>
            </div>

            <!-- Форма данных -->
            <form @submit.prevent="handleSubmit" class="profile-form">
                <div class="form-group">
                    <label>Имя пользователя:</label>
                    <input v-model="formData.username" type="text" :disabled="!editMode" required>
                </div>

                <div class="form-group">
                    <label>Email:</label>
                    <input v-model="formData.email" type="email" :disabled="!editMode" required>
                </div>

                <div class="form-group">
                    <label>Телефон:</label>
                    <input v-model="formData.phone" type="tel" :disabled="!editMode" placeholder="+7 (XXX) XXX-XX-XX">
                </div>

                <!-- Поля только для просмотра -->
                <div class="form-group">
                    <label>Дата регистрации:</label>
                    <input :value="formatDate(user.date_joined)" type="text" disabled>
                </div>

                <div class="form-group">
                    <label>API доступ:</label>
                    <input :value="user.is_api_user ? 'Активен' : 'Неактивен'" type="text" disabled>
                </div>

                <div v-if="editMode" class="form-actions">
                    <button type="submit" :disabled="loading" class="btn-save">
                        {{ loading ? 'Сохранение...' : 'Сохранить изменения' }}
                    </button>
                    <button type="button" @click="changePasswordDialog = true" class="btn-change-password">
                        Сменить пароль
                    </button>
                </div>

                <div v-if="!editMode" class="profile-actions">
                    <button @click="logout" class="btn-logout">
                        <svg class="icon"><!-- Иконка выхода --></svg>
                        Выйти из аккаунта
                    </button>
                    <button @click="remove" class="btn-logout">
                        <svg class="icon"><!-- Иконка выхода --></svg>
                        Удалить аккаунт
                    </button>
                </div>
            </form>
        </div>

        <!-- Диалог смены пароля -->
        <div v-if="changePasswordDialog" class="dialog-overlay">
            <div class="dialog-content">
                <h3>Смена пароля</h3>
                <form @submit.prevent="handlePasswordChange">
                    <div class="form-group">
                        <label>Текущий пароль:</label>
                        <input v-model="passwordData.password" type="password" required>
                    </div>
                    <div class="form-group">
                        <label>Новый пароль:</label>
                        <input v-model="passwordData.new_password" type="password" required>
                    </div>
                    <div class="form-group">
                        <label>Подтвердите пароль:</label>
                        <input v-model="passwordData.new_password_confirm" type="password" required>
                    </div>
                    <div class="dialog-actions">
                        <button type="button" @click="changePasswordDialog = false" class="btn-cancel">
                            Отмена
                        </button>
                        <button type="submit" :disabled="passwordLoading" class="btn-confirm">
                            {{ passwordLoading ? 'Сохранение...' : 'Сменить пароль' }}
                        </button>
                    </div>
                </form>
            </div>
        </div>
    </div>

    <Footer :companyName="'TravelApp'" :email="'smth@gmail.com'" :phone="'+7-(999)-999-99-99'"
        :adrres="'Близжайшая мусорная яма'" />
</template>

<script>
import { authApi } from '../api/api'
import { format } from 'date-fns'
import Footer from '../components/Footer.vue'
import Header from '../components/Header.vue'
import Cookies from 'js-cookie'

export default {
    name: 'ProfilePage',
    components: { Footer, Header },
    data() {
        return {
            user: {
                username: '',
                email: '',
                phone: '',
                avatar: null,
                date_joined: '',
                is_api_user: false
            },
            formData: {
                username: '',
                email: '',
                phone: ''
            },
            editMode: false,
            loading: false,
            changePasswordDialog: false,
            passwordData: {
                password: '',
                new_password: '',
                new_password_confirm: ''
            },
            passwordLoading: false
        }
    },
    created() {
        this.fetchUserData()
    },
    methods: {
        async fetchUserData() {
            try {
                const response = await authApi.get('auth/user/')
                this.user = response.data
                this.resetFormData()
            } catch (error) {
                console.error('Ошибка загрузки профиля:', error)
                this.$toast.error('Не удалось загрузить данные профиля')
            }
        },
        resetFormData() {
            this.formData = {
                username: this.user.username,
                email: this.user.email,
                phone: this.user.phone
            }
        },
        toggleEditMode() {
            this.editMode = !this.editMode
            if (!this.editMode) {
                this.resetFormData()
            }
        },
        formatDate(dateString) {
            if (!dateString) return 'Нет данных'

            try {
                // Проверяем, является ли dateString уже Date объектом
                const date = typeof dateString === 'string' ? new Date(dateString) : dateString

                // Проверяем валидность даты
                if (isNaN(date.getTime())) {
                    return 'Неверная дата'
                }

                return format(date, 'dd.MM.yyyy HH:mm')
            } catch (e) {
                console.error('Ошибка форматирования даты:', e)
                return 'Ошибка даты'
            }
        },
        async handleSubmit() {
            if (!this.editMode) return

            this.loading = true
            try {
                const formData = new FormData()

                // Добавляем текстовые поля
                Object.keys(this.formData).forEach(key => {
                    if (this.formData[key] !== this.user[key]) {
                        formData.append(key, this.formData[key])
                    }
                })

                // Добавляем аватар, если был выбран новый
                if (this.$refs.avatarInput?.files[0]) {
                    formData.append('avatar', this.$refs.avatarInput.files[0])
                }

                const response = await authApi.patch('auth/update/', formData)

                this.user = response.data
                this.editMode = false
            } catch (error) {
                console.error('Ошибка обновления профиля:', error)
            } finally {
                this.loading = false
            }
        },
        handleAvatarChange(event) {
            const file = event.target.files[0]
            if (file) {
                // Превью нового аватара
                const reader = new FileReader()
                reader.onload = (e) => {
                    this.user.avatar = e.target.result
                }
                reader.readAsDataURL(file)
            }
        },
        async removeAvatar() {
            try {
                await authApi.delete('user/avatar/')
                this.user.avatar = null
            } catch (error) {
                console.error('Ошибка удаления аватара:', error)
            }
        },
        async handlePasswordChange() {
            if (this.passwordData.new_password !== this.passwordData.new_password_confirm) {
                return
            }

            this.passwordLoading = true
            try {
                await authApi.post('user/change-password/', this.passwordData)
                this.changePasswordDialog = false
                this.passwordData = {
                    password: '',
                    new_password: '',
                    new_password_confirm: ''
                }
            } catch (error) {
                console.error('Ошибка смены пароля:', error)
            } finally {
                this.passwordLoading = false
            }
        },
        async logout() {
            try {
                Cookies.remove('access_token')
                Cookies.remove('refresh_token')
                this.$router.push('/auth')
            } catch (error) {
                console.error('Ошибка выхода:', error)
            }
        },
        async remove() {
            try {
                if (!confirm('Вы уверены, что хотите удалить аккаунт?')) return
                await authApi.delete('auth/delete/')
                this.logout()
            } catch (error) {
                console.error('Ошибка удаления:', error)
            }
        }
    }
}
</script>

<style scoped>
.profile-page {
    max-width: 800px;
    margin: 0 auto;
    padding: 20px;
    min-height: calc(100vh - 74px - 317px - 40px);
}

.profile-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 30px;
}

.btn-edit {
    padding: 8px 16px;
    background: #42b983;
    color: white;
    border: none;
    border-radius: 4px;
    cursor: pointer;
}

.profile-content {
    display: flex;
    gap: 40px;
}

.avatar-section {
    flex: 0 0 200px;
    display: flex;
    flex-direction: column;
    align-items: center;
}

.avatar-wrapper {
    position: relative;
    width: 150px;
    height: 150px;
    margin-bottom: 15px;
}

.avatar {
    width: 100%;
    height: 100%;
    border-radius: 50%;
    object-fit: cover;
    border: 2px solid #eee;
}

.avatar-input {
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    opacity: 0;
    cursor: pointer;
}

.btn-remove-avatar {
    padding: 6px 12px;
    background: #f8f8f8;
    border: 1px solid #e0e0e0;
    border-radius: 4px;
    cursor: pointer;
}

.profile-form {
    flex: 1;
}

.form-group {
    margin-bottom: 10px;
}

.form-group label {
    display: block;
    margin-bottom: 5px;
    font-weight: 500;
}

.form-group input {
    width: 100%;
    padding: 8px 12px;
    border: 1px solid #ddd;
    border-radius: 4px;
}

.form-group input:disabled {
    background: #f5f5f5;
    border-color: #eee;
}

.form-actions {
    display: flex;
    gap: 15px;
    margin-top: 30px;
}

.btn-save {
    padding: 10px 20px;
    background: #42b983;
    color: white;
    border: none;
    border-radius: 4px;
    cursor: pointer;
}

.btn-change-password {
    padding: 10px 20px;
    background: #f8f8f8;
    border: 1px solid #ddd;
    border-radius: 4px;
    cursor: pointer;
}

.dialog-overlay {
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background: rgba(0, 0, 0, 0.5);
    display: flex;
    justify-content: center;
    align-items: center;
    z-index: 1000;
}

.dialog-content {
    background: white;
    padding: 25px;
    border-radius: 8px;
    width: 100%;
    max-width: 400px;
}

.dialog-actions {
    display: flex;
    justify-content: flex-end;
    gap: 10px;
    margin-top: 20px;
}

.btn-cancel {
    padding: 8px 16px;
    background: #f8f8f8;
    border: 1px solid #ddd;
    border-radius: 4px;
    cursor: pointer;
}

.btn-confirm {
    padding: 8px 16px;
    background: #42b983;
    color: white;
    border: none;
    border-radius: 4px;
    cursor: pointer;
}

.profile-actions {
    margin-top: 40px;
    padding-top: 20px;
    border-top: 1px solid #eee;
    display: flex;
    column-gap: 20px;
}

.btn-logout {
    display: flex;
    align-items: center;
    gap: 8px;
    padding: 10px 20px;
    background: #f8f8f8;
    border: 1px solid #e0e0e0;
    border-radius: 4px;
    cursor: pointer;
    color: #ff4444;
}

.btn-logout:hover {
    background: #ffeeee;
    border-color: #ffcccc;
}

.icon {
    width: 18px;
    height: 18px;
}
</style>