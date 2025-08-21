<template>
  <div class="w-full flex flex-col items-center justify-center my-12">
    <h3 class="mb-8 text-4xl text-dark leading-tight">DESTAQUES</h3>
    <div class="w-full flex flex-wrap items-stretch justify-between px-4">
      <div
        v-for="(product, idx) in products"
        :key="idx"
        class="w-1/3 flex justify-center mb-8"
      >
        <ProductCard :product="product" />
      </div>
    </div>
    <div class="flex justify-center items-center mt-4">
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
import ProductCard from "./ProductCard.vue";

const products = [
  {
    title: "Joia de Prata Minimalista",
    subtitle:
      "O brilho ideal para todos os momentos. Feita com prata 925 legítima.",
    price: 99.9,
    href: "",
    img: "/vue.svg",
  },
  {
    title: "Anel com Zircônia",
    subtitle: "Delicadeza e sofisticação em uma peça atemporal.",
    price: 99.9,
    href: "",
    img: "/vue.svg",
  },
  {
    title: "Colar Elegante",
    subtitle: "Para quem ama se destacar com simplicidade e beleza.",
    price: 99.9,
    href: "",
    img: "/vue.svg",
  },
  {
    title: "Joia de Prata Minimalista",
    subtitle:
      "O brilho ideal para todos os momentos. Feita com prata 925 legítima.",
    price: 99.9,
    href: "",
    img: "/vue.svg",
  },
  {
    title: "Anel com Zircônia",
    subtitle: "Delicadeza e sofisticação em uma peça atemporal.",
    price: 99.9,
    href: "",
    img: "/vue.svg",
  },
  {
    title: "Colar Elegante",
    subtitle: "Para quem ama se destacar com simplicidade e beleza.",
    price: 99.9,
    href: "",
    img: "/vue.svg",
  },
  {
    title: "Joia de Prata Minimalista",
    subtitle:
      "O brilho ideal para todos os momentos. Feita com prata 925 legítima.",
    price: 99.9,
    href: "",
    img: "/vue.svg",
  },
  {
    title: "Anel com Zircônia",
    subtitle: "Delicadeza e sofisticação em uma peça atemporal.",
    price: 99.9,
    href: "",
    img: "/vue.svg",
  },
  {
    title: "Colar Elegante",
    subtitle: "Para quem ama se destacar com simplicidade e beleza.",
    price: 99.9,
    href: "",
    img: "/vue.svg",
  },
];
</script>
