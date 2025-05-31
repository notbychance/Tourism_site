<template>
    <footer class="site-footer">
        <!-- Основной контент футера -->
        <div class="footer-content">
            <!-- Логотип и описание -->
            <div class="footer-section">
                <div class="logo">
                    <slot name="logo">
                        <!-- Слот для логотипа с дефолтным значением -->
                        <span class="logo-text">{{ companyName }}</span>
                    </slot>
                </div>
                <p class="description">
                    <slot name="description">
                        Хороший отдых для всех
                    </slot>
                </p>
            </div>

            <!-- Контактная информация -->
            <div class="footer-section">
                <h4 class="section-title">Контакты</h4>
                <ul class="contact-info">
                    <li v-if="email">
                        <i class="icon icon-email"></i> {{ email }}
                    </li>
                    <li v-if="phone">
                        <i class="icon icon-phone"></i> {{ phone }}
                    </li>
                    <li v-if="address">
                        <i class="icon icon-address"></i> {{ address }}
                    </li>
                </ul>
            </div>

            <!-- Социальные сети -->
            <div class="footer-section">
                <h4 class="section-title">Мы в соцсетях</h4>
                <div class="social-links">
                    <a v-for="(social, index) in socialLinks" :key="index" :href="social.url" :aria-label="social.name"
                        target="_blank" rel="noopener">
                        <i :class="`icon icon-${social.icon}`"></i>
                    </a>
                </div>
            </div>
        </div>

        <!-- Нижняя часть футера -->
        <div class="footer-bottom">
            <p>&copy; {{ currentYear }} {{ companyName }}. Все права защищены.</p>
            <div class="legal-links">
                <a v-for="(item, index) in legalLinks" :key="index" :href="item.url">
                    {{ item.title }}
                </a>
            </div>
        </div>
    </footer>
</template>

<script>
export default {
    name: 'AppFooter',
    props: {
        // Основные параметры
        companyName: {
            type: String,
            default: 'Моя Компания'
        },
        email: String,
        phone: String,
        address: String,

        // Социальные сети
        socialLinks: {
            type: Array,
            default: () => [
                { name: 'Telegram', icon: 'telegram', url: '#' },
                { name: 'VKontakte', icon: 'vk', url: '#' },
                { name: 'YouTube', icon: 'youtube', url: '#' }
            ]
        },

        // Юридические ссылки
        legalLinks: {
            type: Array,
            default: () => [
                { title: 'Политика конфиденциальности', url: '/privacy' },
                { title: 'Условия использования', url: '/terms' }
            ]
        }
    },
    computed: {
        currentYear() {
            return new Date().getFullYear();
        }
    }
};
</script>

<style scoped>
.site-footer {
    background-color: #2c3e50;
    color: #ecf0f1;
    padding: 40px 0 0;
    font-family: 'Arial', sans-serif;
}

.footer-content {
    display: flex;
    flex-wrap: wrap;
    justify-content: space-between;
    max-width: 1200px;
    margin: 0 auto;
    padding: 0 20px 40px;
}

.footer-section {
    flex: 1;
    min-width: 200px;
    margin-bottom: 20px;
    padding: 0 15px;
}

.logo-text {
    font-size: 24px;
    font-weight: bold;
    color: #3498db;
}

.description {
    margin: 15px 0;
    line-height: 1.6;
    opacity: 0.8;
}

.section-title {
    font-size: 18px;
    margin-bottom: 20px;
    position: relative;
    padding-bottom: 10px;
}

.section-title::after {
    content: '';
    position: absolute;
    bottom: 0;
    left: 0;
    width: 50px;
    height: 2px;
    background: #3498db;
}

.footer-links,
.contact-info {
    list-style: none;
    padding: 0;
}

.footer-links li,
.contact-info li {
    margin-bottom: 10px;
}

.footer-links a,
.contact-info a {
    color: #bdc3c7;
    text-decoration: none;
    transition: color 0.3s;
}

.footer-links a:hover,
.contact-info a:hover {
    color: #3498db;
}

.contact-info .icon {
    margin-right: 10px;
    width: 20px;
    display: inline-block;
}

.social-links {
    display: flex;
    gap: 15px;
}

.social-links a {
    display: inline-block;
    width: 40px;
    height: 40px;
    background: rgba(255, 255, 255, 0.1);
    border-radius: 50%;
    text-align: center;
    line-height: 40px;
    transition: background 0.3s;
}

.social-links a:hover {
    background: #3498db;
}

.footer-bottom {
    background: #1a252f;
    padding: 20px 0;
    text-align: center;
    font-size: 14px;
}

.legal-links {
    margin-top: 10px;
}

.legal-links a {
    color: #7f8c8d;
    margin: 0 10px;
    text-decoration: none;
}

.legal-links a:hover {
    color: #3498db;
}

@media (max-width: 768px) {
    .footer-content {
        flex-direction: column;
        align-items: center;
        text-align: center;
    }

    .section-title::after {
        left: 50%;
        transform: translateX(-50%);
    }

    .footer-section {
        width: 100%;
        max-width: 300px;
    }
}
</style>