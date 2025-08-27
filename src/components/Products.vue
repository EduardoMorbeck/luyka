<template>
  <div class="w-full flex flex-col items-center justify-center my-12">
    <h3 class="mb-8 text-4xl text-dark leading-tight">DESTAQUES</h3>
    <div class="w-full flex flex-wrap justify-center px-4 gap-8">
      <div v-for="(product, idx) in products" :key="idx">
        <ProductCard :product="product" />
      </div>
    </div>
    <div class="flex justify-center items-center mt-12">
      <a
        href="/produtos"
        class="w-fit text-xl px-8 py-2.5 bg-btn text-dark font-medium rounded-full border-2 border-dark cursor-pointer"
      >
        Ver todos os Produtos
      </a>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue";
import { getProdutos } from "/src/api.js";
import ProductCard from "./ProductCard.vue";

const products = ref([]);

onMounted(() => {
  getProdutos()
    .then((res) => {
      products.value = res;
    })
    .catch((err) => {
      console.error("Erro ao carregar produtos:", err);
    });
});
</script>
