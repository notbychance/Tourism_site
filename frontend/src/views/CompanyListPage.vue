<template>
  <Header />
  <div class="companies-page">
    <div class="header">
      <h1>Компании</h1>
      <div class="controls">
        <input v-model="searchQuery" type="text" placeholder="Поиск по названию..." class="search-input">
      </div>
    </div>

    <div v-if="loading" class="loading">
      <div class="spinner"></div>
      <p>Загрузка компаний...</p>
    </div>

    <div v-else-if="error" class="error">
      <p>{{ error }}</p>
      <button @click="fetchCompanies" class="btn-retry">Повторить попытку</button>
    </div>

    <div v-else-if="companies.length === 0" class="empty-state">
      <img src="../assets/empty-companies.svg" alt="Нет компаний">
      <h3>Компании не найдены</h3>
      <p v-if="searchQuery">Попробуйте изменить параметры поиска</p>
      <p v-else>В системе пока нет зарегистрированных компаний</p>
    </div>

    <div v-else class="companies-grid">
      <div v-for="company in companies" :key="company.slug" class="company-card">
        <router-link :to="`/company/${company.slug}/`" class="company-link">
          <div class="image-wrapper">
            <img :src="company.image || '../assets/company-placeholder.png'" :alt="company.name" class="company-image">
          </div>
          <div class="company-info">
            <h3 class="company-name">{{ company.name }}</h3>
            <p class="company-description">{{ truncateDescription(company.description) }}</p>
            <div class="company-contacts">
              <div class="contact-item">
                <svg class="icon"><!-- Иконка телефона --></svg>
                <span>{{ formatPhone(company.phone) }}</span>
              </div>
              <div class="contact-item">
                <svg class="icon"><!-- Иконка адреса --></svg>
                <span>{{ company.address }}</span>
              </div>
            </div>
          </div>
        </router-link>
      </div>
    </div>

    <div v-if="!loading" class="pagination">
      <button @click="prevPage" :disabled="!prev" class="pagination-btn">
        Назад
      </button>
      <span class="page-info">Страница {{ currentPage }}</span>
      <button @click="nextPage" :disabled="!next" class="pagination-btn">
        Вперед
      </button>
    </div>
  </div>
  <Footer :companyName="'TravelApp'" :email="'smth@gmail.com'" :phone="'+7-(999)-999-99-99'"
    :adrres="'Близжайшая мусорная яма'" />
</template>

<script>
import { api } from '../api/api'
import Header from '../components/Header.vue';
import Footer from '../components/Footer.vue';

export default {
  name: 'CompaniesPage',
  components: { Header, Footer },
  data() {
    return {
      companies: [],
      loading: false,
      error: '',
      searchQuery: '',
      currentPage: 1,
      prev: false,
      next: false
    }
  },
  created() {
    this.fetchCompanies()
  },
  methods: {
    async fetchCompanies() {
      this.loading = true
      this.error = ''
      try {
        const params = this.buildParams()
        params.page = this.currentPage

        const response = await api.get('company/', { params })

        this.companies = response.data.results

        this.prev = Boolean(response.data.prev)
        this.next = Boolean(response.data.next)
      } catch (error) {
        console.error('Ошибка загрузки компаний:', error)
        this.error = 'Не удалось загрузить список компаний'
      } finally {
        this.loading = false
      }
    },
    truncateDescription(text, length = 100) {
      return text.length > length ? text.substring(0, length) + '...' : text
    },
    formatPhone(phone) {
      return phone.replace(/(\d{1})(\d{3})(\d{3})(\d{2})(\d{2})/, '+$1 ($2) $3-$4-$5')
    },
    nextPage() {
      if (this.currentPage < this.totalPages) {
        this.currentPage++
        this.fetchCompanies()
      }
    },
    prevPage() {
      if (this.currentPage > 1) {
        this.currentPage--
        this.fetchCompanies()
      }
    },
    buildParams() {
      const params = {}

      if (this.searchQuery.trim() !== '') {
        params.name = this.searchQuery.trim();
      }

      return params
    }
  },
  watch: {
    searchQuery() {
      this.currentPage = 1
      this.fetchCompanies()
    }
  }
}
</script>

<style scoped>
.companies-page {
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
  min-height: calc(100vh - 70px - 40px - 317px);
}

.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 30px;
  flex-wrap: wrap;
  gap: 20px;
}

.controls {
  display: flex;
  gap: 15px;
  align-items: center;
}

.search-input {
  padding: 8px 15px;
  border: 1px solid #ddd;
  border-radius: 4px;
  min-width: 250px;
}

.btn-add {
  padding: 8px 16px;
  background: #42b983;
  color: white;
  border-radius: 4px;
  text-decoration: none;
  transition: background 0.2s;
}

.btn-add:hover {
  background: #3aa876;
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

.error {
  text-align: center;
  padding: 30px;
  color: #ff4444;
}

.btn-retry {
  padding: 8px 16px;
  background: #f8f8f8;
  border: 1px solid #ddd;
  border-radius: 4px;
  margin-top: 15px;
  cursor: pointer;
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

.companies-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: 25px;
  margin-bottom: 30px;
}

.company-card {
  border: 1px solid #eee;
  border-radius: 8px;
  overflow: hidden;
  transition: transform 0.2s, box-shadow 0.2s;
}

.company-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 5px 15px rgba(0, 0, 0, 0.1);
}

.company-link {
  display: flex;
  flex-direction: column;
  height: 100%;
  text-decoration: none;
  color: inherit;
}

.image-wrapper {
  height: 180px;
  overflow: hidden;
}

.company-image {
  width: 100%;
  height: 100%;
  object-fit: cover;
  transition: transform 0.3s;
}

.company-card:hover .company-image {
  transform: scale(1.05);
}

.company-info {
  padding: 15px;
  flex-grow: 1;
  display: flex;
  flex-direction: column;
}

.company-name {
  font-size: 1.2rem;
  margin-bottom: 10px;
}

.company-description {
  color: #666;
  margin-bottom: 15px;
  flex-grow: 1;
}

.company-contacts {
  margin-top: auto;
}

.contact-item {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-bottom: 8px;
  font-size: 0.9rem;
}

.contact-item .icon {
  width: 16px;
  height: 16px;
  color: #42b983;
}

.pagination {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 20px;
  margin-top: 30px;
}

.pagination-btn {
  padding: 8px 16px;
  background: #f8f8f8;
  border: 1px solid #ddd;
  border-radius: 4px;
  cursor: pointer;
}

.pagination-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.page-info {
  font-size: 0.9rem;
  color: #666;
}

@media (max-width: 768px) {
  .header {
    flex-direction: column;
    align-items: flex-start;
  }

  .controls {
    width: 100%;
    flex-direction: column;
    align-items: stretch;
  }

  .search-input {
    width: 100%;
    min-width: auto;
  }

  .companies-grid {
    grid-template-columns: 1fr;
  }
}
</style>