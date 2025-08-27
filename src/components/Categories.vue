<template>
  <div class="w-full flex flex-col items-center justify-center my-12">
    <h3 class="mb-8 text-4xl text-dark leading-tight">CATEGORIAS</h3>

    <div
      class="w-full grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6 px-4"
    >
      <article
        v-for="(category, idx) in categories"
        :key="idx"
        class="group relative cursor-pointer overflow-hidden rounded-xl border border-dark/20 bg-white shadow-sm transition"
        @click="goToCategory(category.title)"
        @keyup.enter="goToCategory(category.title)"
        role="button"
        tabindex="0"
        :aria-label="`Abrir categoria ${category.title}`"
      >
        <!-- Imagem em destaque -->
        <figure class="relative aspect-[4/3] w-full overflow-hidden">
          <img
            :src="category.img"
            :alt="category.title"
            class="h-full w-full object-cover transition duration-500 ease-out grayscale group-hover:grayscale-0 group-hover:scale-[1.03]"
            loading="lazy"
          />
          <!-- Faixa com o nome (inspirada no exemplo) -->
          <div
            class="pointer-events-none absolute bottom-4 left-1/2 -translate-x-1/2 rounded-md bg-white/95 px-6 py-2 shadow border border-black/10"
          >
            <span
              class="block text-sm tracking-[0.25em] font-semibold uppercase"
            >
              {{ category.title }}
            </span>
          </div>

          <!-- Gradiente sutil para dar contraste ao texto -->
          <div
            class="pointer-events-none absolute inset-x-0 bottom-0 h-24 bg-gradient-to-t from-black/10 to-transparent"
          />
        </figure>

        <!-- Borda/sombra no hover para dar “clique” -->
        <div
          class="absolute inset-0 ring-0 ring-black/0 transition group-hover:ring-2 group-hover:ring-black/10"
        />
      </article>
    </div>
  </div>
</template>

<script setup>
import { useRouter } from "vue-router";
const router = useRouter();

const categories = [
  { title: "Colares", img: "/1.jpeg" },
  { title: "Anéis", img: "/2.jpeg" },
  { title: "Pulseiras", img: "/3.jpeg" },
  // adicione mais se quiser...
];

function goToCategory(title) {
  router.push({
    name: "produtosConsulta",
    params: { consulta: encodeURIComponent(title) },
  });
}
</script>
