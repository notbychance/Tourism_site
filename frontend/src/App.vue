<!-- src/App.vue -->
<template>
    <!-- Навигационное меню -->
    <!-- <nav class="router">
        <router-link to="/">Главная</router-link> |
        <router-link to="/tours">Все туры</router-link>
    </nav> -->

    <!-- Контейнер для отображения текущей страницы -->
    <router-view></router-view>
</template>

<script>
export default {
    name: 'App'
}
</script>

<style>
/* Базовые стили */
.router {
    display: none;
}
</style>