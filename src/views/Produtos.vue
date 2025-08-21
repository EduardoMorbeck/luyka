<template>
  <div class="w-full flex flex-col py-28 px-4 gap-8">
    <h2 class="font-bold text-center text-3xl w-full mb-8">PRODUTOS</h2>
    <div class="w-full flex flex-wrap items-stretch justify-between px-4">
      <div
        v-for="(product, idx) in products"
        :key="idx"
        class="w-1/3 flex justify-center mb-8"
      >
        <ProductCard :product="product" />
      </div>
    </div>
  </div>
</template>

<script setup>
import ProductCard from "../components/ProductCard.vue";

const products = [
  {
    title: "Joia de Prata Minimalista",
    subtitle:
      "O brilho ideal para todos os momentos. Feita com prata 925 legítima.",
    price: 99.9,
    href: "",
    img: "/src/assets/vue.svg",
  },
  {
    title: "Anel com Zircônia",
    subtitle: "Delicadeza e sofisticação em uma peça atemporal.",
    price: 99.9,
    href: "",
    img: "/src/assets/vue.svg",
  },
  {
    title: "Colar Elegante",
    subtitle: "Para quem ama se destacar com simplicidade e beleza.",
    price: 99.9,
    href: "",
    img: "/src/assets/vue.svg",
  },
  {
    title: "Joia de Prata Minimalista",
    subtitle:
      "O brilho ideal para todos os momentos. Feita com prata 925 legítima.",
    price: 99.9,
    href: "",
    img: "/src/assets/vue.svg",
  },
  {
    title: "Anel com Zircônia",
    subtitle: "Delicadeza e sofisticação em uma peça atemporal.",
    price: 99.9,
    href: "",
    img: "/src/assets/vue.svg",
  },
  {
    title: "Colar Elegante",
    subtitle: "Para quem ama se destacar com simplicidade e beleza.",
    price: 99.9,
    href: "",
    img: "/src/assets/vue.svg",
  },
  {
    title: "Joia de Prata Minimalista",
    subtitle:
      "O brilho ideal para todos os momentos. Feita com prata 925 legítima.",
    price: 99.9,
    href: "",
    img: "/src/assets/vue.svg",
  },
  {
    title: "Anel com Zircônia",
    subtitle: "Delicadeza e sofisticação em uma peça atemporal.",
    price: 99.9,
    href: "",
    img: "/src/assets/vue.svg",
  },
  {
    title: "Colar Elegante",
    subtitle: "Para quem ama se destacar com simplicidade e beleza.",
    price: 99.9,
    href: "",
    img: "/src/assets/vue.svg",
  },
];
</script>
