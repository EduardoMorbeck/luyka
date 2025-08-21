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

import { supabase } from "/src/supabaseClient.js";
import { ref, onMounted } from "vue";

const produtos = ref([]);

async function getProdutos() {
  const { data, error } = await supabase.from("produtos").select("*"); // <-- equivalente ao SELECT * FROM produtos

  if (error) {
    console.error("Erro ao buscar produtos:", error.message);
  } else {
    produtos.value = data;
    console.log("Produtos:", data);
  }
}

onMounted(() => {
  getProdutos();
});
</script>

<style scoped></style>
