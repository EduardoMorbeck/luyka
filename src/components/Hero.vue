<template>
  <div
    class="w-full min-h-screen flex items-center justify-center px-6 py-12 mt-8"
  >
    <div
      class="grid gap-8 w-full max-w-7xl grid-cols-1 sm:grid-cols-2 lg:grid-cols-3"
    >
      <img
        v-for="(slide, idx) in slides"
        :key="idx"
        :src="slide.img"
        :alt="`Imagem ${idx + 1}`"
        class="w-full max-h-[500px] object-contain rounded-2xl border border-gray-200 shadow-sm bg-white p-4"
        loading="lazy"
        decoding="async"
      />
    </div>
  </div>
</template>

<script setup>
const slides = [{ img: "/1.jpeg" }, { img: "/3.jpeg" }, { img: "/2.jpeg" }];
</script>
