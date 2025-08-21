<template>
  <div
    class="w-full flex items-center justify-between px-8 py-4 bg-dark fixed top-0 left-0 z-50 shadow-md"
  >
    <div class="w-1/4">
      <h4 class="text-2xl font-medium">
        <a href="/" class="cursor-pointer">LUYKA </a>
      </h4>
    </div>
    <div class="w-2/4 flex justify-center gap-4">
      <a href="/produtos" class="cursor-pointer hover:underline"
        >Todos os Produtos
      </a>
      <a href="/trocas-devolucoes" class="cursor-pointer hover:underline"
        >Trocas/Devoluções
      </a>
      <a href="/cuidados" class="cursor-pointer hover:underline"
        >Cuidados com a prata 925
      </a>
    </div>
    <div class="w-1/4 flex items-center justify-end gap-4">
      <SearchBar />
      <Cart />
    </div>
  </div>
</template>

<script setup>
import SearchBar from "./SearchBar.vue";
import Cart from "./Cart.vue";
</script>
