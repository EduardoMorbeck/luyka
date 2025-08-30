<template>
  <div>
    <div
      class="w-72 h-full bg-white rounded-2xl shadow-sm hover:shadow-xl transition-all duration-500 cursor-pointer overflow-hidden flex flex-col border border-gray-100 hover:border-[#b9a994] group"
      @click="openProductModal"
    >
      <!-- Imagem em destaque -->
      <div
        class="relative w-full h-52 bg-gradient-to-br from-[#ede5dd] to-[#f5f0ea] overflow-hidden"
      >
        <!-- Imagem principal -->
        <img
          :src="product.imagem_url"
          alt="Produto"
          class="absolute inset-0 w-full h-full object-cover transition-all duration-500 group-hover:scale-110"
          :class="{ 'group-hover:opacity-0': hasSecondImage }"
          loading="lazy"
          @error="$event.target.style.display = 'none'"
          @load="$event.target.style.display = 'block'"
        />

        <!-- Segunda imagem (aparece no hover) -->
        <img
          v-if="hasSecondImage"
          :src="product.imagens_url[1]"
          alt="Produto - Vista adicional"
          class="absolute inset-0 w-full h-full object-cover transition-all duration-500 opacity-0 group-hover:opacity-100 group-hover:scale-110"
          loading="lazy"
          @error="$event.target.style.display = 'none'"
          @load="$event.target.style.display = 'block'"
        />

        <!-- Tag de estoque -->
        <span
          v-if="product.estoque > 0"
          class="absolute top-3 right-3 bg-[#735e59] text-white text-xs font-medium px-3 py-1.5 rounded-full shadow-lg backdrop-blur-sm bg-opacity-90"
        >
          {{ product.estoque }} em estoque
        </span>

        <!-- Se quiser mostrar "Esgotado" -->
        <span
          v-else
          class="absolute top-3 right-3 bg-gray-500 text-white text-xs font-medium px-3 py-1.5 rounded-full shadow-lg backdrop-blur-sm bg-opacity-90"
        >
          Esgotado
        </span>
      </div>

      <!-- Conteúdo -->
      <div class="flex-1 p-5 flex flex-col justify-between">
        <div class="text-center space-y-3">
          <h3
            class="text-xl font-semibold text-[#735e59] truncate font-['Prata',serif] tracking-wide"
          >
            {{ product.nome }}
          </h3>
          <p
            class="text-sm text-[#735e59] text-opacity-70 line-clamp-2 leading-relaxed px-2"
          >
            {{ product.descricao }}
          </p>
          <div class="pt-2">
            <div class="text-2xl font-bold text-[#735e59] font-['Prata',serif]">
              {{ precoBRL }}
            </div>
          </div>
        </div>

        <button
          :disabled="Number(product.estoque) == 0"
          @click.stop="addProduct"
          class="mt-6 w-full py-3 rounded-full bg-[#ede5dd] border-2 border-[#735e59] text-[#735e59] font-medium hover:bg-[#735e59] hover:text-white transition-all duration-300 disabled:opacity-50 disabled:cursor-not-allowed disabled:hover:bg-[#ede5dd] disabled:hover:text-[#735e59] shadow-sm hover:shadow-md transform hover:-translate-y-0.5"
        >
          {{
            Number(product.estoque) > 0
              ? "Adicionar ao Carrinho"
              : "Produto Esgotado"
          }}
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed } from "vue";
import { cartStore } from "../store/cartStore";

const props = defineProps({
  product: {
    type: Object,
    required: true,
  },
});

const emit = defineEmits(["open-modal"]);

const precoBRL = computed(() =>
  new Intl.NumberFormat("pt-BR", { style: "currency", currency: "BRL" }).format(
    Number(props.product?.preco ?? 0)
  )
);

const hasSecondImage = computed(() => {
  return props.product?.imagens_url && props.product.imagens_url.length > 1;
});

const hasMultipleImages = computed(() => {
  return props.product?.imagens_url && props.product.imagens_url.length > 1;
});

const openProductModal = () => {
  emit("open-modal", props.product);
};

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
};
</script>
