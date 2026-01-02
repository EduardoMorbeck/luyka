<template>
  <section
    class="w-full min-h-screen bg-gradient-to-br from-[#f5f0ea] via-white to-[#ede5dd] relative overflow-hidden"
  >
    <div class="max-w-7xl mx-auto px-6 lg:px-8 relative z-10 py-32">
      <div class="text-center mb-4">
        <h1
          class="text-4xl lg:text-6xl font-bold bg-gradient-to-r from-[#735e59] via-[#b9a994] to-[#735e59] bg-clip-text text-transparent font-['Prata',serif] tracking-wider mb-6 transform transition-all duration-700 hover:scale-105 cursor-pointer"
        >
          PRODUTOS
        </h1>
      </div>

      <div class="mb-16">
        <div
          class="bg-white/80 backdrop-blur-sm rounded-3xl p-8 shadow-xl border border-[#ede5dd] max-w-5xl mx-auto"
        >
          <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
            <div class="relative">
              <label class="flex flex-col gap-3">
                <div class="flex items-center gap-2">
                  <i class="fa-solid fa-layer-group text-[#b9a994] text-sm"></i>
                  <span
                    class="font-semibold text-[#735e59] text-sm tracking-wide"
                    >CATEGORIA</span
                  >
                </div>
                <select
                  v-model="selectedCategory"
                  class="w-full px-4 py-3 bg-white border-2 border-[#ede5dd] rounded-xl text-[#735e59] font-medium transition-all duration-300 hover:border-[#b9a994] focus:border-[#735e59] focus:outline-none focus:ring-2 focus:ring-[#735e59]/20 cursor-pointer"
                >
                  <option value="">Todas as Categorias</option>
                  <option v-for="c in categories" :key="c" :value="c">
                    {{ c }}
                  </option>
                </select>
              </label>
            </div>

            <div class="relative">
              <label class="flex flex-col gap-3">
                <div class="flex items-center gap-2">
                  <i class="fa-solid fa-dollar-sign text-[#b9a994] text-sm"></i>
                  <span
                    class="font-semibold text-[#735e59] text-sm tracking-wide"
                    >PREÇO</span
                  >
                </div>
                <select
                  v-model="priceOrder"
                  class="w-full px-4 py-3 bg-white border-2 border-[#ede5dd] rounded-xl text-[#735e59] font-medium transition-all duration-300 hover:border-[#b9a994] focus:border-[#735e59] focus:outline-none focus:ring-2 focus:ring-[#735e59]/20 cursor-pointer"
                >
                  <option value="">Sem ordenação</option>
                  <option value="asc">Menor → Maior</option>
                  <option value="desc">Maior → Menor</option>
                </select>
              </label>
            </div>

            <div class="relative">
              <label class="flex flex-col gap-3">
                <div class="flex items-center gap-2">
                  <i
                    class="fa-solid fa-sort-alpha-down text-[#b9a994] text-sm"
                  ></i>
                  <span
                    class="font-semibold text-[#735e59] text-sm tracking-wide"
                    >NOME</span
                  >
                </div>
                <select
                  v-model="nameOrder"
                  class="w-full px-4 py-3 bg-white border-2 border-[#ede5dd] rounded-xl text-[#735e59] font-medium transition-all duration-300 hover:border-[#b9a994] focus:border-[#735e59] focus:outline-none focus:ring-2 focus:ring-[#735e59]/20 cursor-pointer"
                >
                  <option value="">Sem ordenação</option>
                  <option value="az">A → Z</option>
                  <option value="za">Z → A</option>
                </select>
              </label>
            </div>
          </div>

          <div
            v-if="selectedCategory || priceOrder || nameOrder"
            class="mt-6 pt-6 border-t border-[#ede5dd]"
          >
            <div class="flex flex-wrap items-center gap-3">
              <span class="text-sm text-[#735e59]/70 font-medium"
                >Filtros ativos:</span
              >
              <div
                v-if="selectedCategory"
                class="inline-flex items-center gap-2 bg-[#735e59] text-white px-3 py-1 rounded-full text-sm font-medium"
              >
                <i class="fa-solid fa-layer-group text-xs"></i>
                {{ selectedCategory }}
              </div>
              <div
                v-if="priceOrder"
                class="inline-flex items-center gap-2 bg-[#735e59] text-white px-3 py-1 rounded-full text-sm font-medium"
              >
                <i class="fa-solid fa-dollar-sign text-xs"></i>
                {{ priceOrder === "asc" ? "Menor → Maior" : "Maior → Menor" }}
              </div>
              <div
                v-if="nameOrder"
                class="inline-flex items-center gap-2 bg-[#735e59] text-white px-3 py-1 rounded-full text-sm font-medium"
              >
                <i class="fa-solid fa-sort-alpha-down text-xs"></i>
                {{ nameOrder === "az" ? "A → Z" : "Z → A" }}
              </div>
            </div>
          </div>
        </div>
      </div>

      <div class="mb-16">
        <div
          v-if="visibleProducts.length > 0"
          class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-8 justify-items-center"
        >
          <div
            v-for="(product, idx) in visibleProducts"
            :key="product.id ?? idx"
            class="transform transition-all duration-500 hover:-translate-y-2 animate-fade-in-up cursor-pointer"
            :style="{ animationDelay: `${(idx % 8) * 100}ms` }"
          >
            <ProductCard :product="product" @open-modal="openProductModal" />
          </div>
        </div>

        <div
          v-else-if="!loadingFirstPage && !loadingAll"
          class="text-center py-20"
        >
          <div class="inline-flex flex-col items-center space-y-6">
            <div
              class="w-24 h-24 bg-gradient-to-br from-[#ede5dd] to-[#b9a994] rounded-full flex items-center justify-center"
            >
              <i class="fa-solid fa-search text-3xl text-[#735e59]"></i>
            </div>
            <div class="space-y-2">
              <h3
                class="text-2xl font-bold text-[#735e59] font-['Prata',serif]"
              >
                Nenhum produto encontrado
              </h3>
              <p class="text-[#735e59]/70 max-w-md">
                <span v-if="allProducts.length === 0">
                  Ainda não há produtos cadastrados. Comece adicionando seu
                  primeiro produto!
                </span>
                <span v-else>
                  Tente ajustar os filtros ou remover algumas opções de busca
                  para ver mais resultados.
                </span>
              </p>
            </div>
            <div class="flex flex-col sm:flex-row gap-4">
              <button
                v-if="allProducts.length === 0"
                @click="goToCadastrarProdutos"
                class="inline-flex items-center gap-2 px-6 py-3 bg-[#735e59] text-white font-medium rounded-full hover:bg-[#5a4a46] transition-all duration-300 shadow-lg hover:shadow-xl transform hover:-translate-y-1 cursor-pointer"
              >
                <i class="fa-solid fa-plus text-sm"></i>
                Cadastrar Produtos
              </button>
              <button
                v-else
                @click="clearAllFilters"
                class="inline-flex items-center gap-2 px-6 py-3 bg-[#735e59] text-white font-medium rounded-full hover:bg-[#5a4a46] transition-all duration-300 shadow-lg hover:shadow-xl transform hover:-translate-y-1 cursor-pointer"
              >
                <i class="fa-solid fa-refresh text-sm"></i>
                Limpar Filtros
              </button>
            </div>
          </div>
        </div>
      </div>

      <div
        v-if="loadingFirstPage"
        class="flex flex-col items-center justify-center py-20"
      >
        <div class="relative">
          <div
            class="w-16 h-16 border-4 border-[#ede5dd] border-t-[#735e59] rounded-full animate-spin"
          ></div>
          <div
            class="absolute inset-0 w-16 h-16 border-4 border-transparent border-r-[#b9a994] rounded-full animate-spin-reverse"
          ></div>
        </div>
        <p class="mt-6 text-[#735e59] font-medium animate-pulse">
          Carregando produtos...
        </p>
      </div>

      <div v-else class="w-full flex justify-center">
        <div v-if="loadingMore" class="flex flex-col items-center py-8">
          <div
            class="w-8 h-8 border-2 border-[#ede5dd] border-t-[#735e59] rounded-full animate-spin"
          ></div>
          <p class="mt-3 text-sm text-[#735e59]/70 animate-pulse">
            Carregando mais produtos...
          </p>
        </div>
        <div ref="sentinel" class="h-6"></div>
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
import { ref, onMounted, computed, watch, onBeforeUnmount } from "vue";
import { useRoute, useRouter } from "vue-router";
import { getProdutos } from "/src/api.js";
import ProductCard from "../components/ProductCard.vue";
import { cartStore } from "../store/cartStore";

const route = useRoute();
const router = useRouter();

const consulta = computed(() => {
  const p = route.params?.consulta;
  return typeof p === "string" ? decodeURIComponent(p) : "";
});

const PAGE_LIMIT = 50;
const CHUNK_VISIBLE = 24;

const selectedProduct = ref(null);
const currentImageIndex = ref(0);

const allProducts = ref([]);
const loadingFirstPage = ref(false);
const loadingMore = ref(false);
const loadingAll = ref(false);
const nextCursorId = ref(null);
const hasMoreServer = ref(true);

const selectedCategory = ref("");
const priceOrder = ref("");
const nameOrder = ref("");
const revealedCount = ref(CHUNK_VISIBLE);

const sentinel = ref(null);
let observer;

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

// Funções de navegação de imagens
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

const currentQ = () => {
  const cat = (selectedCategory.value || "").trim();
  const fromRoute = (consulta.value || "").trim();
  return cat || fromRoute || undefined;
};

const fetchPage = async ({ cursor } = {}) => {
  const params = { limit: PAGE_LIMIT };
  if (cursor) params.cursor_id = cursor;
  const q = currentQ();
  if (q) params.q = q;

  const batch = await getProdutos(params);
  if (!Array.isArray(batch)) return;

  if (batch.length > 0) {
    const last = batch[batch.length - 1];
    nextCursorId.value = last?.id ?? null;
  }

  if (batch.length < PAGE_LIMIT) {
    hasMoreServer.value = false;
  }

  allProducts.value = allProducts.value.concat(batch);
};

const loadFirstPage = async () => {
  loadingFirstPage.value = true;
  allProducts.value = [];
  nextCursorId.value = null;
  hasMoreServer.value = true;
  revealedCount.value = CHUNK_VISIBLE;

  try {
    await fetchPage();
  } catch (e) {
    console.error("Erro ao carregar produtos:", e);
  } finally {
    loadingFirstPage.value = false;
  }
};

const loadAllPages = async () => {
  if (!hasMoreServer.value) return;
  loadingAll.value = true;
  try {
    while (hasMoreServer.value) {
      await fetchPage({ cursor: nextCursorId.value });
    }
  } catch (e) {
    console.error("Erro ao carregar páginas:", e);
  } finally {
    loadingAll.value = false;
  }
};

const syncFromRouteAndFetch = async () => {
  selectedCategory.value = consulta.value || "";
  await loadFirstPage();
};

watch(
  () => route.params.consulta,
  async () => {
    await syncFromRouteAndFetch();
  }
);

watch(selectedCategory, (cat) => {
  const val = (cat || "").trim();
  if (val) {
    router.replace({
      name: "produtosConsulta",
      params: { consulta: encodeURIComponent(val) },
    });
  } else {
    router.replace({ name: "produtos" });
  }
});

watch(
  () => route.params.consulta,
  (newVal) => {
    selectedCategory.value = newVal ? String(newVal) : "";
  }
);

watch([priceOrder, nameOrder], async () => {
  const wantsSorting = !!priceOrder.value || !!nameOrder.value;
  if (wantsSorting && hasMoreServer.value) {
    await loadAllPages();
  }
  revealedCount.value = CHUNK_VISIBLE;
});

const categories = computed(() => {
  const defaultCategories = ["Anel", "Colar", "Conjunto"];
  const set = new Set(defaultCategories);

  allProducts.value
    .map((p) => p?.categoria)
    .filter((c) => typeof c === "string" && c.trim().length > 0)
    .forEach((c) => set.add(c));

  return Array.from(set).sort((a, b) =>
    a.localeCompare(b, "pt-BR", { sensitivity: "base" })
  );
});

const filtered = computed(() => {
  const cat = (selectedCategory.value || "").trim().toLowerCase();
  if (!cat) return allProducts.value;
  return allProducts.value.filter(
    (p) => (p?.categoria ?? "").toLowerCase() === cat
  );
});

const sorted = computed(() => {
  const arr = [...filtered.value];

  if (priceOrder.value) {
    arr.sort((a, b) => {
      const va = Number(a?.preco ?? a?.valor ?? 0);
      const vb = Number(b?.preco ?? b?.valor ?? 0);
      return priceOrder.value === "asc" ? va - vb : vb - va;
    });
  }

  if (nameOrder.value) {
    arr.sort((a, b) => {
      const na = String(a?.nome ?? "");
      const nb = String(b?.nome ?? "");
      const base = na.localeCompare(nb, "pt-BR", { sensitivity: "base" });
      return nameOrder.value === "az" ? base : -base;
    });
  }

  return arr;
});

const visibleProducts = computed(() =>
  sorted.value.slice(0, revealedCount.value)
);

const onIntersect = async (entries) => {
  const entry = entries[0];
  if (!entry?.isIntersecting) return;

  if (revealedCount.value < sorted.value.length) {
    revealedCount.value += CHUNK_VISIBLE;
    return;
  }

  const wantsSorting = !!priceOrder.value || !!nameOrder.value;
  if (!wantsSorting && hasMoreServer.value && !loadingMore.value) {
    try {
      loadingMore.value = true;
      await fetchPage({ cursor: nextCursorId.value });
      revealedCount.value += CHUNK_VISIBLE;
    } finally {
      loadingMore.value = false;
    }
  }
};

onMounted(async () => {
  await syncFromRouteAndFetch();

  observer = new IntersectionObserver(onIntersect, {
    root: null,
    threshold: 0.1,
  });
  if (sentinel.value) observer.observe(sentinel.value);
  if (route.params.consulta) {
    selectedCategory.value = String(route.params.consulta);
  }
});

const clearAllFilters = () => {
  selectedCategory.value = "";
  priceOrder.value = "";
  nameOrder.value = "";
};

const goToCadastrarProdutos = () => {
  router.push("/cadastrar-produtos");
};

onBeforeUnmount(() => {
  if (observer && sentinel.value) observer.unobserve(sentinel.value);
});
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

@keyframes float {
  0%,
  100% {
    transform: translateY(0px);
  }
  50% {
    transform: translateY(-6px);
  }
}

.animate-float {
  animation: float 3s ease-in-out infinite;
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

@keyframes spin-reverse {
  from {
    transform: rotate(0deg);
  }
  to {
    transform: rotate(-360deg);
  }
}

.animate-spin-reverse {
  animation: spin-reverse 1.5s linear infinite;
}

select:hover {
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(115, 94, 89, 0.15);
  cursor: pointer;
}

select:focus {
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(115, 94, 89, 0.25);
}

@media (max-width: 768px) {
  .hover\:-translate-y-2:hover {
    transform: translateY(-8px);
  }
}

@media (hover: none) {
  .hover\:-translate-y-2:active {
    transform: scale(0.98);
  }
}

select:focus-visible {
  outline: 2px solid #735e59;
  outline-offset: 2px;
}

@keyframes slide-in {
  from {
    opacity: 0;
    transform: translateX(-10px);
  }
  to {
    opacity: 1;
    transform: translateX(0);
  }
}

.inline-flex[class*="bg-[#735e59]"] {
  animation: slide-in 0.3s ease-out;
}

.backdrop-blur-sm {
  backdrop-filter: blur(8px);
  -webkit-backdrop-filter: blur(8px);
}
</style>
