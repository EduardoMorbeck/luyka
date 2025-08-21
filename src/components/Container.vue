<template>
  <div class="flex flex-col items-center justify-between">
    <Hero id="home" />

    <Benefits id="benefits" />

    <Categories id="categories" />

    <Products id="products" />
  </div>
</template>

<script setup>
import Hero from "./Hero.vue";
import Benefits from "./Benefits.vue";
import Categories from "./Categories.vue";
import Products from "./Products.vue";
</script>
