<template>
  <nav
    class="w-full fixed top-0 left-0 z-50 bg-dark backdrop-blur-md shadow-lg"
  >
    <div class="max-w-7xl mx-auto px-6 lg:px-8">
      <div class="flex items-center justify-between h-20">
        <div class="flex items-center justify-between flex-1 max-w-4xl">
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

          <div class="hidden md:flex items-center space-x-8">
            <a
              href="/cadastrar-produtos"
              class="nav-link group relative flex items-center py-2 px-1 text-[#735e59] font-medium transition-all duration-300 hover:text-[#232121] cursor-pointer"
            >
              <i
                class="fa-solid fa-plus-circle mr-2 text-sm text-[#735e59] group-hover:text-[#232121] transition-colors duration-300"
              ></i>
              <span class="relative">
                Cadastrar Produtos
                <span
                  class="absolute bottom-0 left-0 w-0 h-0.5 bg-gradient-to-r from-[#735e59] to-[#b9a994] transition-all duration-300 group-hover:w-full"
                ></span>
              </span>
            </a>
            <a
              href="/produtos"
              class="nav-link group relative flex items-center py-2 px-1 text-[#735e59] font-medium transition-all duration-300 hover:text-[#232121]"
            >
              <i
                class="fa-solid fa-box mr-2 text-sm text-[#735e59] group-hover:text-[#232121] transition-colors duration-300"
              ></i>
              <span class="relative">
                Ver Produtos
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

        <div class="flex items-center space-x-4 ml-6">
          <div class="w-80 hidden lg:block">
            <SearchBar />
          </div>

          <div class="relative">
            <Cart />
          </div>

          <button
            class="md:hidden flex items-center justify-center w-10 h-10 rounded-full bg-white bg-opacity-60 hover:bg-opacity-80 transition-all duration-300 hover:shadow-md border border-[#ede5dd] cursor-pointer"
            @click="toggleMobileMenu"
            aria-label="Menu"
          >
            <i class="fa-solid fa-bars text-[#735e59]"></i>
          </button>
        </div>
      </div>

      <div
        v-if="showMobileMenu"
        class="md:hidden bg-white bg-opacity-95 backdrop-blur-md border-t border-[#ede5dd] rounded-2xl shadow-xl"
      >
        <div class="px-4 py-6 space-y-4 my-4">
          <div class="lg:hidden mb-4">
            <SearchBar />
          </div>

          <a
            href="/cadastrar-produtos"
            class="flex items-center px-4 py-3 text-[#735e59] font-medium transition-all duration-300 hover:text-[#232121] hover:bg-[#ede5dd] rounded-xl cursor-pointer"
            @click="closeMobileMenu"
          >
            <i class="fa-solid fa-plus-circle mr-3 text-[#b9a994]"></i>
            Cadastrar Produtos
          </a>
          <a
            href="/produtos"
            class="flex items-center px-4 py-3 text-[#735e59] font-medium transition-all duration-300 hover:text-[#232121] hover:bg-[#ede5dd] rounded-xl cursor-pointer"
            @click="closeMobileMenu"
          >
            <i class="fa-solid fa-box mr-3 text-[#b9a994]"></i>
            Ver Produtos
          </a>
          <a
            href="/cuidados"
            class="flex items-center px-4 py-3 text-[#735e59] font-medium transition-all duration-300 hover:text-[#232121] hover:bg-[#ede5dd] rounded-xl cursor-pointer"
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

const showMobileMenu = ref(false);

const toggleMobileMenu = () => {
  showMobileMenu.value = !showMobileMenu.value;
};

const closeMobileMenu = () => {
  showMobileMenu.value = false;
};
</script>
