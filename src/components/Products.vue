<template>
  <section
    class="w-full py-16 bg-gradient-to-br from-[#ede5dd] via-white to-[#f5f0ea] relative overflow-hidden"
  >
    <div class="absolute inset-0 opacity-10">
      <div
        class="absolute top-10 left-10 w-32 h-32 bg-[#b9a994] rounded-full blur-3xl"
      ></div>
      <div
        class="absolute bottom-20 right-20 w-40 h-40 bg-[#735e59] rounded-full blur-3xl"
      ></div>
      <div
        class="absolute top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2 w-60 h-60 bg-[#b9a994] rounded-full blur-3xl"
      ></div>
    </div>

    <div class="max-w-7xl mx-auto px-6 lg:px-8 relative z-10">
      <div class="text-center mb-16">
        <div class="inline-flex items-center justify-center mb-4">
          <div
            class="h-px bg-gradient-to-r from-transparent via-[#735e59] to-transparent w-24"
          ></div>
          <i
            class="fa-solid fa-star mx-4 text-2xl text-[#735e59] animate-pulse"
          ></i>
          <div
            class="h-px bg-gradient-to-r from-transparent via-[#735e59] to-transparent w-24"
          ></div>
        </div>

        <h2
          class="text-4xl lg:text-6xl font-bold bg-gradient-to-r from-[#735e59] via-[#b9a994] to-[#735e59] bg-clip-text text-transparent font-['Prata',serif] tracking-wider mb-4 transform transition-all duration-700 hover:scale-105 cursor-pointer"
        >
          DESTAQUES
        </h2>

        <p class="text-lg text-[#735e59]/80 max-w-2xl mx-auto leading-relaxed">
          Descubra nossa seleção especial de joias exclusivas, criadas com
          carinho e atenção aos detalhes
        </p>
      </div>

      <div v-if="products.length > 0">
        <div
          class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-8 mb-16"
        >
          <div
            v-for="(product, idx) in products"
            :key="idx"
            class="transform transition-all duration-500 hover:-translate-y-2 animate-fade-in-up cursor-pointer flex items-center justify-center"
            :style="{ animationDelay: `${idx * 150}ms` }"
          >
            <ProductCard :product="product" @open-modal="openProductModal" />
          </div>
        </div>
      </div>

      <div v-else class="text-center py-20 mb-16">
        <div class="inline-flex flex-col items-center space-y-6">
          <div
            class="w-24 h-24 bg-gradient-to-br from-[#ede5dd] to-[#b9a994] rounded-full flex items-center justify-center"
          >
            <i class="fa-solid fa-box-open text-3xl text-[#735e59]"></i>
          </div>
          <div class="space-y-2">
            <h3 class="text-2xl font-bold text-[#735e59] font-['Prata',serif]">
              Nenhum produto cadastrado
            </h3>
            <p class="text-[#735e59]/70 max-w-md">
              Ainda não há produtos cadastrados. Comece adicionando seu primeiro
              produto!
            </p>
          </div>
          <button
            @click="goToCadastrarProdutos"
            class="inline-flex items-center gap-2 px-6 py-3 bg-[#735e59] text-white font-medium rounded-full hover:bg-[#5a4a46] transition-all duration-300 shadow-lg hover:shadow-xl transform hover:-translate-y-1 cursor-pointer"
          >
            <i class="fa-solid fa-plus text-sm"></i>
            Cadastrar Produtos
          </button>
        </div>
      </div>

      <div class="text-center">
        <div class="inline-flex flex-col items-center space-y-4">
          <a
            href="/produtos"
            class="group relative inline-flex items-center justify-center px-10 py-4 text-xl font-semibold text-[#735e59] bg-white border-3 border-[#735e59] rounded-full shadow-lg hover:shadow-2xl transition-all duration-500 hover:-translate-y-1 hover:bg-[#735e59] hover:text-white overflow-hidden cursor-pointer"
          >
            <span
              class="absolute inset-0 bg-gradient-to-r from-[#735e59] via-[#b9a994] to-[#735e59] transform scale-x-0 group-hover:scale-x-100 transition-transform duration-500 origin-left"
            ></span>

            <i
              class="fa-solid fa-gem mr-3 relative z-10 group-hover:rotate-12 transition-transform duration-300"
            ></i>
            <span class="relative z-10 tracking-wide"
              >Ver todos os Produtos</span
            >
            <i
              class="fa-solid fa-arrow-right ml-3 relative z-10 group-hover:translate-x-1 transition-transform duration-300"
            ></i>
          </a>

          <div class="flex items-center space-x-2 text-sm text-[#735e59]/60">
            <div class="w-2 h-2 bg-[#b9a994] rounded-full animate-pulse"></div>
            <span>Descubra a prata que combina com você</span>
            <div class="w-2 h-2 bg-[#b9a994] rounded-full animate-pulse"></div>
          </div>
        </div>
      </div>
    </div>

    <div
      v-if="selectedProduct"
      class="fixed inset-0 backdrop-blur-sm flex items-center justify-center z-[9999] p-4"
      @click="closeProductModal"
    >
      <div
        class="bg-white rounded-2xl shadow-2xl p-6 relative w-full max-w-6xl h-full max-h-[95vh] border border-[#b9a994] transform transition-all duration-300 overflow-y-auto"
        @click.stop
      >
        <button
          class="absolute top-4 right-4 w-10 h-10 rounded-full bg-[#ede5dd] hover:bg-[#b9a994] transition-all duration-200 flex items-center justify-center group z-10 cursor-pointer"
          @click="closeProductModal"
        >
          <i
            class="fa-solid fa-xmark text-[#735e59] group-hover:text-white transition-colors duration-200"
          ></i>
        </button>

        <div class="flex flex-col lg:flex-row gap-6 h-full">
          <div
            class="flex-1 flex items-center justify-center bg-gradient-to-br from-[#ede5dd] to-[#f5f0ea] rounded-xl p-4 relative"
          >
            <img
              :src="currentImageUrl"
              alt="Produto"
              class="w-full h-screen max-h-[80vh] object-contain rounded-lg transition-all duration-300"
            />

            <div
              v-if="hasMultipleImages"
              class="absolute inset-0 flex items-center justify-between p-4"
            >
              <button
                v-if="currentImageIndex > 0"
                @click="previousImage"
                class="w-12 h-12 bg-white bg-opacity-80 hover:bg-opacity-100 rounded-full shadow-lg flex items-center justify-center transition-all duration-200 hover:scale-110 cursor-pointer"
              >
                <i class="fa-solid fa-chevron-left text-[#735e59] text-xl"></i>
              </button>
              <div v-else class="w-12"></div>

              <button
                v-if="currentImageIndex < totalImages - 1"
                @click="nextImage"
                class="w-12 h-12 bg-white bg-opacity-80 hover:bg-opacity-100 rounded-full shadow-lg flex items-center justify-center transition-all duration-200 hover:scale-110 cursor-pointer"
              >
                <i class="fa-solid fa-chevron-right text-[#735e59] text-xl"></i>
              </button>
              <div v-else class="w-12"></div>
            </div>

            <div
              v-if="hasMultipleImages"
              class="absolute bottom-4 left-1/2 transform -translate-x-1/2 flex space-x-2"
            >
              <button
                v-for="(image, index) in selectedProduct.imagens_url"
                :key="index"
                @click="goToImage(index)"
                class="w-3 h-3 rounded-full transition-all duration-200"
                :class="
                  index === currentImageIndex
                    ? 'bg-[#735e59]'
                    : 'bg-white bg-opacity-60 hover:bg-opacity-80 cursor-pointer'
                "
              ></button>
            </div>

            <div
              v-if="hasMultipleImages"
              class="absolute top-4 left-4 bg-black bg-opacity-50 text-white text-sm px-3 py-1 rounded-full backdrop-blur-sm"
            >
              {{ currentImageIndex + 1 }} / {{ totalImages }}
            </div>
          </div>

          <div class="lg:w-80 flex flex-col justify-center space-y-6 p-4">
            <div class="text-center lg:text-left space-y-4">
              <h2
                class="text-3xl font-bold text-[#735e59] font-['Prata',serif]"
              >
                {{ selectedProduct.nome }}
              </h2>
              <p class="text-[#735e59] text-opacity-80 leading-relaxed">
                {{ selectedProduct.descricao }}
              </p>
              <div class="pt-2">
                <p
                  class="text-4xl font-bold text-[#735e59] font-['Prata',serif]"
                >
                  {{ formatPrice(selectedProduct.preco) }}
                </p>
              </div>
            </div>

            <div class="flex justify-center lg:justify-start pt-4">
              <button
                @click="addToCart"
                class="w-full lg:w-auto px-12 py-4 bg-[#735e59] text-white text-lg font-medium rounded-full hover:bg-[#5a4a46] transition-all duration-300 shadow-lg hover:shadow-xl transform hover:-translate-y-1 cursor-pointer"
              >
                Adicionar ao Carrinho
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  </section>
</template>

<script setup>
import { ref, onMounted, computed } from "vue";
import { useRouter } from "vue-router";
import { getProdutos } from "/src/api.js";
import ProductCard from "./ProductCard.vue";
import { cartStore } from "../store/cartStore";

const router = useRouter();

const products = ref([]);
const selectedProduct = ref(null);
const currentImageIndex = ref(0);

onMounted(() => {
  getProdutos()
    .then((res) => {
      products.value = res;
    })
    .catch((err) => {
      console.error("Erro ao carregar produtos:", err);
    });
});

const openProductModal = (product) => {
  selectedProduct.value = product;
  currentImageIndex.value = 0;
};

const closeProductModal = () => {
  selectedProduct.value = null;
  currentImageIndex.value = 0;
};

const formatPrice = (price) => {
  return new Intl.NumberFormat("pt-BR", {
    style: "currency",
    currency: "BRL",
  }).format(Number(price ?? 0));
};

const hasMultipleImages = computed(() => {
  return (
    selectedProduct.value?.imagens_url &&
    selectedProduct.value.imagens_url.length > 1
  );
});

const totalImages = computed(() => {
  return selectedProduct.value?.imagens_url?.length || 0;
});

const currentImageUrl = computed(() => {
  if (!selectedProduct.value) return "";
  if (
    selectedProduct.value.imagens_url &&
    selectedProduct.value.imagens_url.length > 0
  ) {
    return selectedProduct.value.imagens_url[currentImageIndex.value];
  }
  return selectedProduct.value.imagem_url;
});

const nextImage = () => {
  if (currentImageIndex.value < totalImages.value - 1) {
    currentImageIndex.value++;
  }
};

const previousImage = () => {
  if (currentImageIndex.value > 0) {
    currentImageIndex.value--;
  }
};

const goToImage = (index) => {
  if (index >= 0 && index < totalImages.value) {
    currentImageIndex.value = index;
  }
};

const addToCart = () => {
  if (selectedProduct.value) {
    cartStore.addItem({
      id: selectedProduct.value.id,
      img: selectedProduct.value.imagem_url,
      title: selectedProduct.value.nome,
      description: selectedProduct.value.descricao,
      category: selectedProduct.value.categoria,
      stok: selectedProduct.value.estoque,
      price: Number(selectedProduct.value.preco),
      qty: 1,
    });
    cartStore.openCart();
    closeProductModal();
  }
};

const goToCadastrarProdutos = () => {
  router.push("/cadastrar-produtos");
};
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

.group:hover .absolute {
  animation: wave 0.6s ease-in-out;
}

@keyframes wave {
  0% {
    transform: scaleX(0);
  }
  50% {
    transform: scaleX(0.5);
  }
  100% {
    transform: scaleX(1);
  }
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
</style>
