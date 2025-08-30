<template>
  <section
    class="w-full min-h-screen bg-gradient-to-br from-[#f5f0ea] via-white to-[#ede5dd] relative overflow-hidden"
  >
    <div class="max-w-7xl mx-auto px-6 lg:px-8 relative z-10 py-32">
      <!-- Cabeçalho aprimorado -->
      <div class="text-center mb-4">
        <h1
          class="text-5xl lg:text-6xl font-bold bg-gradient-to-r from-[#735e59] via-[#b9a994] to-[#735e59] bg-clip-text text-transparent font-['Prata',serif] tracking-wider mb-6 transform transition-all duration-700 hover:scale-105"
        >
          PRODUTOS
        </h1>
      </div>

      <!-- Seção de filtros aprimorada -->
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

          <!-- Indicador de filtros ativos -->
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

      <!-- Grid de produtos aprimorado -->
      <div class="mb-16">
        <div
          v-if="visibleProducts.length > 0"
          class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-8 justify-items-center"
        >
          <div
            v-for="(product, idx) in visibleProducts"
            :key="product.id ?? idx"
            class="transform transition-all duration-500 hover:-translate-y-2 animate-fade-in-up"
            :style="{ animationDelay: `${(idx % 8) * 100}ms` }"
          >
            <ProductCard :product="product" />
          </div>
        </div>

        <!-- Estado vazio aprimorado -->
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
                Tente ajustar os filtros ou remover algumas opções de busca para
                ver mais resultados.
              </p>
            </div>
            <button
              @click="clearAllFilters"
              class="inline-flex items-center gap-2 px-6 py-3 bg-[#735e59] text-white font-medium rounded-full hover:bg-[#5a4a46] transition-all duration-300 shadow-lg hover:shadow-xl transform hover:-translate-y-1"
            >
              <i class="fa-solid fa-refresh text-sm"></i>
              Limpar Filtros
            </button>
          </div>
        </div>
      </div>

      <!-- Estados de loading aprimorados -->
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
  </section>
</template>

<script setup>
import { ref, onMounted, computed, watch, onBeforeUnmount } from "vue";
import { useRoute, useRouter } from "vue-router";
import { getProdutos } from "/src/api.js";
import ProductCard from "../components/ProductCard.vue";

const route = useRoute();
const router = useRouter();

const consulta = computed(() => {
  const p = route.params?.consulta;
  return typeof p === "string" ? decodeURIComponent(p) : "";
});

const PAGE_LIMIT = 50;
const CHUNK_VISIBLE = 24;

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
  const set = new Set(
    allProducts.value
      .map((p) => p?.categoria)
      .filter((c) => typeof c === "string" && c.trim().length > 0)
  );
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

// Função para limpar todos os filtros
const clearAllFilters = () => {
  selectedCategory.value = "";
  priceOrder.value = "";
  nameOrder.value = "";
};

onBeforeUnmount(() => {
  if (observer && sentinel.value) observer.unobserve(sentinel.value);
});
</script>

<style scoped>
/* Animação de fade-in com movimento para cima */
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

/* Animação de flutuação para ícones */
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

/* Animação de pulsação suave */
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

/* Animação de rotação reversa para loading */
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

/* Efeitos hover melhorados para selects */
select:hover {
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(115, 94, 89, 0.15);
}

select:focus {
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(115, 94, 89, 0.25);
}

/* Animações responsivas */
@media (max-width: 768px) {
  .text-5xl {
    font-size: 2.5rem;
  }

  .lg\:text-6xl {
    font-size: 3rem;
  }

  .hover\:-translate-y-2:hover {
    transform: translateY(-8px);
  }
}

/* Efeito de hover específico para dispositivos touch */
@media (hover: none) {
  .hover\:-translate-y-2:active {
    transform: scale(0.98);
  }
}

/* Melhorias visuais para estados de foco */
select:focus-visible {
  outline: 2px solid #735e59;
  outline-offset: 2px;
}

/* Animação para os indicadores de filtros ativos */
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

/* Efeito de backdrop melhorado */
.backdrop-blur-sm {
  backdrop-filter: blur(8px);
  -webkit-backdrop-filter: blur(8px);
}
</style>
