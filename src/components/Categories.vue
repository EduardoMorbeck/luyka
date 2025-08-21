<template>
  <div class="w-full flex flex-col items-center justify-center my-12">
    <h3 class="mb-8 text-4xl text-dark leading-tight">CATEGORIAS</h3>
    <div class="w-full flex flex-wrap items-stretch justify-between px-4">
      <div
        v-for="(category, idx) in categories"
        :key="idx"
        class="w-1/4 flex justify-center"
      >
        <div
          class="w-96 h-full flex flex-col items-center justify-between border border-dark rounded-lg p-4"
        >
          <div class="flex flex-col items-center">
            <img :src="category.img" alt="Produto" class="w-12 h-12" />
            <div class="flex flex-col text-center">
              <div class="font-medium">
                {{ category.title }}
              </div>
            </div>
          </div>
          <div class="flex justify-center items-center mt-4">
            <a
              :href="category.href"
              class="w-fit px-8 py-2.5 bg-btn text-dark font-medium rounded-full border-2 border-dark cursor-pointer"
            >
              Ver mais
            </a>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
const categories = [
  {
    title: "Aneis",
    href: "",
    img: "/vue.svg",
  },
  {
    title: "Brincos",
    href: "",
    img: "/vue.svg",
  },
  {
    title: "Colares",
    href: "",
    img: "/vue.svg",
  },
  {
    title: "Pulseiras",
    href: "",
    img: "/vue.svg",
  },
];
</script>
