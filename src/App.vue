<template>
  <div>
    <NavBar />
    <router-view />
    <Footer />
  </div>
</template>

<script setup>
import NavBar from "./components/NavBar.vue";
import Footer from "./components/Footer.vue";
</script>

<style scoped></style>
