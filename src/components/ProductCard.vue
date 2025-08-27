<template>
  <div>
    <div
      class="w-72 h-full bg-white rounded-2xl shadow-md hover:shadow-2xl transition-shadow duration-300 cursor-pointer overflow-hidden flex flex-col"
      @click="showModal = true"
    >
      <!-- Imagem em destaque -->
      <div class="relative w-full bg-gray-100 flex items-center justify-center">
        <img
          :src="product.imagem_url"
          alt="Produto"
          class="object-cover w-full h-48 transition-transform duration-300 hover:scale-105"
        />

        <!-- Tag de estoque -->
        <span
          v-if="product.estoque > 0"
          class="absolute top-2 right-2 bg-red-500 text-white text-xs font-semibold px-3 py-1 rounded-full shadow-md"
        >
          {{ product.estoque }} unid.
        </span>

        <!-- Se quiser mostrar "Esgotado" -->
        <span
          v-else
          class="absolute top-2 right-2 bg-gray-400 text-white text-xs font-semibold px-3 py-1 rounded-full shadow-md"
        >
          Esgotado
        </span>
      </div>

      <!-- Conteúdo -->
      <div class="flex-1 p-4 flex flex-col justify-between text-center">
        <div>
          <h3 class="text-lg font-semibold text-gray-800 truncate">
            {{ product.nome }}
          </h3>
          <p class="text-sm text-gray-500 line-clamp-2">
            {{ product.descricao }}
          </p>
          <div class="mt-3 text-xl font-bold text-gray-800">
            {{ precoBRL }}
          </div>
        </div>

        <button
          :disabled="Number(product.estoque) == 0"
          @click.stop="addProduct"
          class="mt-4 w-full py-2 rounded-full bg-btn border-2 border-dark text-dark font-medium hover:brightness-110 transition disabled:opacity-50 disabled:cursor-not-allowed"
        >
          {{ Number(product.estoque) > 0 ? "Comprar" : "Esgotado" }}
        </button>
      </div>
    </div>

    <!-- Modal -->
    <div
      v-if="showModal"
      class="fixed inset-0 bg-black/50 backdrop-blur-sm flex items-center justify-center z-50"
    >
      <div
        class="bg-white rounded-lg shadow-lg p-8 relative max-w-md w-full"
        @click.stop
      >
        <button class="p-2 absolute top-2 right-2" @click="showModal = false">
          <div
            class="flex items-center justify-center cursor-pointer py-2 px-3 rounded-full bg-gray-100 hover:bg-gray-200"
          >
            <i class="fa-solid fa-xmark text-xl"></i>
          </div>
        </button>

        <img
          :src="product.imagem_url"
          alt="Produto"
          class="w-80 h-80 mx-auto object-cover rounded-lg"
        />
        <h2 class="text-2xl font-bold text-center mt-4">{{ product.nome }}</h2>
        <p class="text-gray-600 text-center">{{ product.descricao }}</p>
        <p class="text-2xl font-bold text-center mt-4 text-gray-800">
          {{ precoBRL }}
        </p>

        <div class="flex justify-center mt-6">
          <button
            @click="addProduct"
            class="px-10 py-3 bg-btn text-lg text-dark font-medium rounded-full border-2 border-dark hover:brightness-110 transition"
          >
            Comprar
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from "vue";
import { cartStore } from "../store/cartStore";

const props = defineProps({
  product: {
    type: Object,
    required: true,
  },
});

const showModal = ref(false);

const precoBRL = computed(() =>
  new Intl.NumberFormat("pt-BR", { style: "currency", currency: "BRL" }).format(
    Number(props.product?.preco ?? 0)
  )
);

const addProduct = () => {
  cartStore.addItem({
    id: props.product.id,
    img: props.product.imagem_url,
    title: props.product.nome,
    description: props.product.descricao,
    category: props.product.categoria,
    stok: props.product.estoque,
    price: Number(props.product.preco),
    qty: 1,
  });
  cartStore.openCart();
  showModal.value = false;
};
</script>
