<template>
  <div class="w-full h-screen flex items-center justify-center">
    <div class="w-full relative flex items-center overflow-hidden h-[100vh]">
      <!-- Slides -->
      <div
        class="w-full h-full flex flex-col transition-all duration-500"
        :style="{ transform: `translateY(-${active * 100}%)` }"
      >
        <div
          v-for="(slide, idx) in slides"
          :key="idx"
          class="min-h-full w-full flex items-center justify-between px-14 ml-8"
        >
          <!-- Esquerda: Texto -->
          <div class="flex flex-col w-1/2">
            <h2 class="text-6xl text-dark leading-tight">
              {{ slide.title }}
            </h2>
            <p class="text-base text-gray mb-8">
              {{ slide.subtitle }}
            </p>
            <a
              :href="slide.href"
              class="w-fit px-8 py-2.5 bg-btn text-dark font-medium rounded-full border-2 border-dark mt-2 cursor-pointer"
            >
              {{ slide.button }}
            </a>
          </div>
          <!-- Direita: Imagem do produto -->
          <div class="flex-1 flex justify-center items-center w-1/2">
            <img
              :src="slide.img"
              alt="Produto"
              class="object-contain w-[32rem]"
            />
          </div>
        </div>
      </div>

      <!-- Bullets -->
      <div class="absolute right-8 top-2/4 flex flex-col gap-12">
        <span
          v-for="(_, idx) in slides"
          :key="'bullet-' + idx"
          :class="[
            'block w-2.5 h-2.5 rounded-full bg-slate-950 transition cursor-pointer',
            active === idx ? 'scale-125 ' : 'opacity-50',
          ]"
          @click="goTo(idx)"
        ></span>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from "vue";

const slides = [
  {
    title: "Acessórios de Prata",
    subtitle:
      "O brilho ideal para todos os momentos. Feita com prata 925 legítima.",
    button: "Ver detalhes",
    href: "",
    img: "/src/assets/5.png",
  },
  {
    title: "Anel com Zircônia",
    subtitle: "Delicadeza e sofisticação em uma peça atemporal.",
    button: "Ver mais",
    href: "",
    img: "/src/assets/6.png",
  },
  {
    title: "Acessórios de Prata",
    subtitle:
      "O brilho ideal para todos os momentos. Feita com prata 925 legítima.",
    button: "Ver mais",
    href: "",
    img: "/src/assets/2.png",
  },
];

const active = ref(0);

function next() {
  active.value = (active.value + 1) % slides.length;
}
function prev() {
  active.value = (active.value - 1 + slides.length) % slides.length;
}
function goTo(idx) {
  active.value = idx;
}
</script>

<style scoped></style>
