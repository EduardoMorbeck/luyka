<template>
  <div>
    <NavBar />
    <router-view />
    <Footer />
    <WhatsApp />
  </div>
</template>

<script setup>
import NavBar from "./components/NavBar.vue";
import Footer from "./components/Footer.vue";
import WhatsApp from "./components/WhatsApp.vue";
</script>

<style scoped></style>
