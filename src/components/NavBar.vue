<template>
  <nav
    class="w-full fixed top-0 left-0 z-50 bg-dark backdrop-blur-md shadow-lg"
  >
    <div class="max-w-7xl mx-auto px-6 lg:px-8">
      <div class="flex items-center justify-between h-20">
        <!-- Logo e navegação principal -->
        <div class="flex items-center justify-between flex-1 max-w-4xl">
          <!-- Logo -->
          <div class="flex-shrink-0">
            <a
              href="/"
              class="group flex items-center cursor-pointer transition-all duration-300 hover:-translate-y-0.5"
            >
              <h1
                class="text-3xl font-bold bg-gradient-to-r from-[#735e59] to-[#b9a994] bg-clip-text text-transparent tracking-wide font-['Prata',serif] group-hover:from-[#b9a994] group-hover:to-[#735e59] transition-all duration-300"
              >
                LUYKA
              </h1>
              <div
                class="ml-2 w-2 h-2 bg-[#735e59] rounded-full group-hover:bg-[#b9a994] transition-colors duration-300"
              ></div>
            </a>
          </div>

          <!-- Menu de navegação -->
          <div class="hidden md:flex items-center space-x-8">
            <a
              href="/produtos"
              class="nav-link group relative flex items-center py-2 px-1 text-[#735e59] font-medium transition-all duration-300 hover:text-[#232121]"
            >
              <i
                class="fa-solid fa-box mr-2 text-sm text-[#735e59] group-hover:text-[#232121] transition-colors duration-300"
              ></i>
              <span class="relative">
                Produtos
                <span
                  class="absolute bottom-0 left-0 w-0 h-0.5 bg-gradient-to-r from-[#735e59] to-[#b9a994] transition-all duration-300 group-hover:w-full"
                ></span>
              </span>
            </a>
            <a
              href="/trocas-devolucoes"
              class="nav-link group relative flex items-center py-2 px-1 text-[#735e59] font-medium transition-all duration-300 hover:text-[#232121]"
            >
              <i
                class="fa-solid fa-refresh mr-2 text-sm text-[#735e59] group-hover:text-[#232121] transition-colors duration-300"
              ></i>
              <span class="relative">
                Trocas & Devoluções
                <span
                  class="absolute bottom-0 left-0 w-0 h-0.5 bg-gradient-to-r from-[#735e59] to-[#b9a994] transition-all duration-300 group-hover:w-full"
                ></span>
              </span>
            </a>
            <a
              href="/cuidados"
              class="nav-link group relative flex items-center py-2 px-1 text-[#735e59] font-medium transition-all duration-300 hover:text-[#232121]"
            >
              <i
                class="fa-solid fa-heart mr-2 text-sm text-[#735e59] group-hover:text-[#232121] transition-colors duration-300"
              ></i>
              <span class="relative">
                Cuidados
                <span
                  class="absolute bottom-0 left-0 w-0 h-0.5 bg-gradient-to-r from-[#735e59] to-[#b9a994] transition-all duration-300 group-hover:w-full"
                ></span>
              </span>
            </a>
          </div>
        </div>

        <!-- Área de busca e carrinho -->
        <div class="flex items-center space-x-4 ml-6">
          <!-- Barra de busca -->
          <div class="w-80 hidden lg:block">
            <SearchBar />
          </div>

          <!-- Carrinho -->
          <div class="relative">
            <Cart />
          </div>

          <!-- Menu mobile -->
          <button
            class="md:hidden flex items-center justify-center w-10 h-10 rounded-full bg-white bg-opacity-60 hover:bg-opacity-80 transition-all duration-300 hover:shadow-md border border-[#ede5dd]"
            @click="toggleMobileMenu"
            aria-label="Menu"
          >
            <i class="fa-solid fa-bars text-[#735e59]"></i>
          </button>
        </div>
      </div>

      <!-- Menu mobile expandido -->
      <div
        v-if="showMobileMenu"
        class="md:hidden bg-white bg-opacity-95 backdrop-blur-md border-t border-[#ede5dd] rounded-b-2xl shadow-xl"
      >
        <div class="px-4 py-6 space-y-4">
          <!-- Busca mobile -->
          <div class="lg:hidden mb-4">
            <SearchBar />
          </div>

          <!-- Links de navegação mobile -->
          <a
            href="/produtos"
            class="flex items-center px-4 py-3 text-[#735e59] font-medium transition-all duration-300 hover:text-[#232121] hover:bg-[#ede5dd] rounded-xl"
            @click="closeMobileMenu"
          >
            <i class="fa-solid fa-box mr-3 text-[#b9a994]"></i>
            Produtos
          </a>
          <a
            href="/trocas-devolucoes"
            class="flex items-center px-4 py-3 text-[#735e59] font-medium transition-all duration-300 hover:text-[#232121] hover:bg-[#ede5dd] rounded-xl"
            @click="closeMobileMenu"
          >
            <i class="fa-solid fa-refresh mr-3 text-[#b9a994]"></i>
            Trocas & Devoluções
          </a>
          <a
            href="/cuidados"
            class="flex items-center px-4 py-3 text-[#735e59] font-medium transition-all duration-300 hover:text-[#232121] hover:bg-[#ede5dd] rounded-xl"
            @click="closeMobileMenu"
          >
            <i class="fa-solid fa-heart mr-3 text-[#b9a994]"></i>
            Cuidados
          </a>
        </div>
      </div>
    </div>
  </nav>
</template>

<script setup>
import { ref } from "vue";
import SearchBar from "./SearchBar.vue";
import Cart from "./Cart.vue";

// Estado do menu mobile
const showMobileMenu = ref(false);

// Funções do menu mobile
const toggleMobileMenu = () => {
  showMobileMenu.value = !showMobileMenu.value;
};

const closeMobileMenu = () => {
  showMobileMenu.value = false;
};
</script>
