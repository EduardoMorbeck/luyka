<template>
  <div>
    <div
      class="w-96 h-full flex flex-col items-center justify-between border border-dark rounded-lg p-4 cursor-pointer hover:shadow-xl"
    >
      <div
        @click="showModal = true"
        class="flex flex-col items-center justify-between"
      >
        <div class="flex flex-col items-center">
          <img :src="product.img" alt="Produto" class="w-12 h-12" />
          <div class="flex flex-col text-center">
            <div class="font-medium">
              {{ product.title }}
            </div>
            <div class="text-xs">
              {{ product.subtitle }}
            </div>
          </div>
        </div>
        <div class="font-medium mt-2">R$ {{ product.price }}</div>
      </div>
      <div class="flex justify-center items-center mt-4">
        <div
          class="w-fit px-8 py-2.5 bg-btn text-dark font-medium rounded-full border-2 border-dark"
          @click="addProduct"
        >
          Comprar
        </div>
      </div>
    </div>

    <div
      v-if="showModal"
      class="fixed inset-0 bg-black/50 backdrop-blur-sm flex items-center justify-center z-50"
    >
      <div class="bg-white rounded-lg shadow-lg p-12 relative" @click.stop>
        <button class="p-2 absolute top-2 right-2" @click="showModal = false">
          <div
            class="flex items-center justify-center cursor-pointer py-2.5 px-3 rounded-full bg-gray-100 hover:bg-gray-200"
          >
            <i class="fa-solid fa-xmark text-xl"></i>
          </div>
        </button>

        <img :src="product.img" alt="Produto" class="w-20 h-20 mx-auto" />
        <h2 class="text-2xl font-bold text-center mt-4">{{ product.title }}</h2>
        <p class="text-gray-600 text-center">{{ product.subtitle }}</p>
        <p class="text-2xl font-bold text-center mt-4">
          R$ {{ product.price }}
        </p>
        <div class="flex justify-center mt-6">
          <div
            @click="addProduct"
            class="px-10 py-4 bg-btn text-xl text-dark font-medium rounded-full border-2 border-dark"
          >
            Comprar
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from "vue";
import { cartStore } from "../store/cartStore";

const props = defineProps({
  product: {
    type: Object,
    required: true,
  },
});

const showModal = ref(false);

const addProduct = () => {
  cartStore.addItem({
    id: props.product.id,
    img: props.product.img,
    title: props.product.title,
    price: props.product.price,
    qty: 1,
  });
  cartStore.openCart();
};
</script>
