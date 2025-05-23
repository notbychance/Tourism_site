<template>
    <div class="tour-slider">
        <Splide :options="splideOptions" aria-label="Туры" class="splide-custom" ref="splide">
            <SplideSlide v-for="(tour, index) in tours" :key="index">
                <div class="tour-card" @click="handleTourClick(tour)">
                    <div class="image-wrapper">
                        <img :src="tour.image" :alt="tour.title" @error="handleImageError" class="tour-image"
                            loading="lazy">
                    </div>
                    <div class="card-content">
                        <h3 class="tour-title">{{ tour.title }}</h3>
                        <p v-if="tour.description" class="tour-description">{{ tour.description }}</p>
                        <div class="price-section">
                            <span class="tour-price">{{ formatPrice(tour.price) }}</span>
                            <button class="details-button">{{ buttonText }}</button>
                        </div>
                    </div>
                </div>
            </SplideSlide>
        </Splide>
    </div>
</template>

<script>
import { Splide, SplideSlide } from '@splidejs/vue-splide';
import '@splidejs/splide/dist/css/splide.min.css';

export default {
    name: 'TourSlider',
    components: {
        Splide,
        SplideSlide
    },
    props: {
        tours: {
            type: Array,
            require: true,
            validator: (value) => value.every(item =>
                item.title && item.price
            )
        },
        buttonText: {
            type: String,
            default: 'Подробнее'
        },
        itemsPerView: {
            type: Object,
            default: () => ({
                desktop: 3,
                tablet: 2,
                mobile: 1
            })
        }
    },
    data() {
        return {
            splideOptions: {
                type: 'loop',
                perPage: this.itemsPerView.desktop,
                perMove: 1,
                gap: '20px',
                focus: 'center',
                pagination: false,
                arrows: true,
                breakpoints: {
                    1200: { perPage: this.itemsPerView.desktop },
                    992: { perPage: this.itemsPerView.tablet, gap: '15px' },
                    768: { perPage: this.itemsPerView.mobile, gap: '10px' }
                }
            }
        };
    },
    methods: {
        formatPrice(price) {
            return new Intl.NumberFormat('ru-RU').format(price) + ' ₽';
        },
        handleImageError(event) {
            event.target.src = require('@/assets/images/default-tour.jpg');
        },
        handleTourClick(tour) {
            this.$emit('tour-click', tour.slug);
        },
        goToSlide(index) {
            this.$refs.splide.go(index);
        }
    }
};
</script>

<style scoped>
.tour-slider {
    max-width: 1400px;
    margin: 2rem auto;
    padding: 0 1rem;
}

.section-title {
    text-align: center;
    margin-bottom: 2rem;
    font-size: 2rem;
    color: var(--primary-color);
}

.splide-custom {
    padding: 1rem 0;
}

.tour-card {
    background: #ffffff;
    border-radius: 12px;
    overflow: hidden;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    transition: transform 0.3s ease, box-shadow 0.3s ease;
    height: 100%;
    display: flex;
    flex-direction: column;
    cursor: pointer;
    margin: 0 0.5rem;
}

.tour-card:hover {
    transform: translateY(-5px);
    box-shadow: 0 6px 12px rgba(0, 0, 0, 0.15);
}

.image-wrapper {
    height: 200px;
    overflow: hidden;
    position: relative;
}

.tour-image {
    width: 100%;
    height: 100%;
    object-fit: cover;
    transition: transform 0.3s ease;
}

.tour-card:hover .tour-image {
    transform: scale(1.05);
}

.card-content {
    padding: 1.25rem;
    flex-grow: 1;
    display: flex;
    flex-direction: column;
}

.tour-title {
    font-size: 1.25rem;
    margin-bottom: 0.75rem;
    color: #2d3748;
}

.tour-description {
    color: #4a5568;
    font-size: 0.9rem;
    line-height: 1.5;
    margin-bottom: 1rem;
    flex-grow: 1;
}

.price-section {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-top: 1rem;
}

.tour-price {
    font-weight: 700;
    color: #e53e3e;
    font-size: 1.1rem;
}

.details-button {
    background-color: #e53e3e;
    color: white;
    border: none;
    padding: 0.5rem 1rem;
    border-radius: 20px;
    cursor: pointer;
    font-size: 0.9rem;
    transition: background-color 0.3s ease;
}

.details-button:hover {
    background-color: #c53030;
}

:deep(.splide__arrow) {
    opacity: 0;
    width: 40px;
    height: 40px;
    opacity: 1;
    transition: opacity 0.3s ease;
}

:deep(.splide__arrow:hover) {
    opacity: 0.9;
}

:deep(.splide__arrow--prev) {
    left: -50px;
}

:deep(.splide__arrow--next) {
    right: -50px;
}

@media (max-width: 768px) {
    .section-title {
        font-size: 1.5rem;
    }

    :deep(.splide__arrow) {
        display: none;
    }

    .tour-card {
        margin: 0 0.25rem;
    }
}
</style>