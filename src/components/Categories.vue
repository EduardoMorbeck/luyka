<template>
  <section
    class="w-full py-16 bg-gradient-to-br from-[#f5f0ea] via-white to-[#ede5dd] relative overflow-hidden"
  >
    <div class="absolute inset-0 opacity-8">
      <div
        class="absolute top-20 right-10 w-40 h-40 bg-[#735e59] rounded-full blur-3xl"
      ></div>
      <div
        class="absolute bottom-10 left-20 w-32 h-32 bg-[#b9a994] rounded-full blur-3xl"
      ></div>
      <div
        class="absolute top-1/3 left-1/3 w-48 h-48 bg-[#ede5dd] rounded-full blur-3xl"
      ></div>
    </div>

    <div class="max-w-7xl mx-auto px-6 lg:px-8 relative z-10">
      <div class="text-center mb-16">
        <div class="inline-flex items-center justify-center mb-4">
          <div
            class="h-px bg-gradient-to-r from-transparent via-[#735e59] to-transparent w-20"
          ></div>
          <i
            class="fa-solid fa-layer-group mx-4 text-2xl text-[#735e59] animate-pulse"
          ></i>
          <div
            class="h-px bg-gradient-to-r from-transparent via-[#735e59] to-transparent w-20"
          ></div>
        </div>

        <h2
          class="text-4xl lg:text-6xl font-bold bg-gradient-to-r from-[#735e59] via-[#b9a994] to-[#735e59] bg-clip-text text-transparent font-['Prata',serif] tracking-wider mb-4 transform transition-all duration-700 hover:scale-105 cursor-pointer"
        >
          CATEGORIAS
        </h2>

        <p class="text-lg text-[#735e59]/80 max-w-2xl mx-auto leading-relaxed">
          Explore nossas coleções organizadas por categoria e encontre a joia
          perfeita para cada ocasião
        </p>
      </div>

      <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
        <article
          v-for="(category, idx) in categories"
          :key="idx"
          class="group relative cursor-pointer overflow-hidden rounded-2xl bg-white shadow-xl hover:shadow-2xl transition-all duration-500 transform hover:-translate-y-3 animate-fade-in-up border border-[#ede5dd] hover:border-[#b9a994]"
          :style="{ animationDelay: `${idx * 200}ms` }"
          @click="goToCategory(category.title)"
          @keyup.enter="goToCategory(category.title)"
          role="button"
          tabindex="0"
          :aria-label="`Abrir categoria ${category.title}`"
        >
          <figure class="relative aspect-[4/3] w-full overflow-hidden">
            <div
              class="absolute inset-0 bg-gradient-to-t from-[#735e59]/20 via-transparent to-transparent opacity-60 group-hover:opacity-80 transition-opacity duration-500 z-10"
            ></div>

            <img
              :src="category.img"
              :alt="category.title"
              class="h-full w-full object-cover transition-all duration-700 ease-out filter group-hover:brightness-110 group-hover:scale-110"
              loading="lazy"
            />

            <div
              class="absolute inset-0 bg-gradient-to-tr from-transparent via-white/10 to-white/20 opacity-0 group-hover:opacity-100 transition-opacity duration-500"
            ></div>

            <div
              class="pointer-events-none absolute bottom-6 left-1/2 -translate-x-1/2 transform transition-all duration-500 group-hover:bottom-8 z-20"
            >
              <div
                class="bg-white/95 backdrop-blur-sm px-8 py-3 rounded-full shadow-lg border border-[#ede5dd] group-hover:bg-[#735e59] group-hover:border-[#735e59] transition-all duration-500"
              >
                <span
                  class="block text-sm tracking-[0.3em] font-bold uppercase text-[#735e59] group-hover:text-white transition-colors duration-500 font-['Prata',serif]"
                >
                  {{ category.title }}
                </span>
              </div>
            </div>

            <div
              class="absolute top-4 right-4 w-10 h-10 bg-white/20 backdrop-blur-sm rounded-full flex items-center justify-center opacity-0 group-hover:opacity-100 transition-all duration-500 z-20"
            >
              <i
                class="fa-solid fa-arrow-right text-white text-sm group-hover:translate-x-0.5 transition-transform duration-300"
              ></i>
            </div>
          </figure>

          <div
            class="absolute inset-0 rounded-2xl ring-0 ring-[#735e59]/0 transition-all duration-500 group-hover:ring-2 group-hover:ring-[#735e59]/30"
          ></div>

          <div
            class="absolute inset-0 -translate-x-full group-hover:translate-x-full transition-transform duration-1000 bg-gradient-to-r from-transparent via-white/20 to-transparent skew-x-12"
          ></div>
        </article>
      </div>

      <div class="text-center mt-12">
        <div
          class="inline-flex items-center space-x-3 text-sm text-[#735e59]/60"
        >
          <div class="w-2 h-2 bg-[#b9a994] rounded-full animate-pulse"></div>
          <span>Clique em uma categoria para explorar os produtos</span>
          <div class="w-2 h-2 bg-[#b9a994] rounded-full animate-pulse"></div>
        </div>
      </div>
    </div>
  </section>
</template>

<script setup>
import { useRouter } from "vue-router";
const router = useRouter();

const categories = [
  { title: "Anel", img: "/1.png" },
  { title: "Colar", img: "/2.png" },
  { title: "Conjunto", img: "/3.png" },
];

function goToCategory(title) {
  router.push({
    name: "produtosConsulta",
    params: { consulta: encodeURIComponent(title) },
  });
}
</script>

<style scoped>
@keyframes fade-in-up {
  from {
    opacity: 0;
    transform: translateY(30px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.animate-fade-in-up {
  animation: fade-in-up 0.8s ease-out forwards;
}

@keyframes pulse-soft {
  0%,
  100% {
    opacity: 1;
  }
  50% {
    opacity: 0.7;
  }
}

.animate-pulse {
  animation: pulse-soft 2s ease-in-out infinite;
}

@keyframes shimmer {
  0% {
    transform: translateX(-100%) skewX(-12deg);
  }
  100% {
    transform: translateX(200%) skewX(-12deg);
  }
}

.group:hover .shimmer {
  animation: shimmer 1s ease-out;
}

@media (max-width: 768px) {
  .group:hover {
    transform: translateY(-8px);
  }
}

@media (hover: none) {
  .group:active {
    transform: scale(0.98);
  }
}

@keyframes float {
  0%,
  100% {
    transform: translateY(0px);
  }
  50% {
    transform: translateY(-3px);
  }
}

.fa-layer-group {
  animation: float 3s ease-in-out infinite;
}
</style>
