<template>
  <div class="searchbar-group" ref="rootEl">
    <input
      v-model="q"
      :placeholder="placeholder"
      type="search"
      class="input"
      @focus="openPanel()"
    />
    <i class="icon fa-solid fa-magnifying-glass"></i>

    <div v-if="open && q.length >= minChars" class="panel" @keydown.stop>
      <div v-if="loadingFirst" class="state muted">Buscando…</div>

      <template v-else>
        <div
          v-for="(p, idx) in results"
          :key="p.id ?? idx"
          class="item"
          @click="handleSelect(p)"
        >
          <img :src="p.imagem_url || fallbackImg" :alt="p.nome" class="thumb" />
          <div class="meta">
            <div class="title">
              <strong>{{ (p.nome || "").toUpperCase() }}</strong>
            </div>
            <div class="price-row">
              <div class="price">
                {{ formatPrice(p.preco ?? p.valor) }}
              </div>
            </div>
          </div>
        </div>

        <div v-if="!loadingFirst && results.length === 0" class="state muted">
          Nenhum resultado.
        </div>

        <div v-if="loadingMore" class="state muted">Carregando mais…        </div>

        <div ref="sentinel" class="sentinel"></div>
      </template>
    </div>

    <Teleport to="body">
      <div
        v-if="showModal && selectedProduct"
        class="fixed inset-0 backdrop-blur-sm flex items-center justify-center z-[9999] p-4"
        @click="closeModal"
      >
        <div
          class="bg-white rounded-2xl shadow-2xl p-6 relative w-full max-w-6xl h-full max-h-[95vh] border border-[#b9a994] transform transition-all duration-300 overflow-y-auto"
          @click.stop
        >
          <button
            class="absolute top-4 right-4 w-10 h-10 rounded-full bg-[#ede5dd] hover:bg-[#b9a994] transition-all duration-200 flex items-center justify-center group z-10 cursor-pointer"
            @click="closeModal"
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
                    {{ formatPrice(selectedProduct.preco ?? selectedProduct.valor) }}
                  </p>
                </div>
              </div>

              <div class="flex justify-center lg:justify-start pt-4">
                <button
                  :disabled="Number(selectedProduct.estoque) == 0"
                  @click.stop="addProduct"
                  class="w-full lg:w-auto px-12 py-4 bg-[#735e59] text-white text-lg font-medium rounded-full hover:bg-[#5a4a46] transition-all duration-300 shadow-lg hover:shadow-xl transform hover:-translate-y-1 disabled:opacity-50 disabled:cursor-not-allowed disabled:hover:bg-[#735e59] disabled:hover:transform-none cursor-pointer"
                >
                  {{
                    Number(selectedProduct.estoque) > 0
                      ? "Adicionar ao Carrinho"
                      : "Produto Esgotado"
                  }}
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </Teleport>
  </div>
</template>

<script setup>
import { ref, watch, onMounted, onBeforeUnmount, nextTick, computed } from "vue";
import { getProdutos } from "/src/api.js";
import { cartStore } from "../store/cartStore";

const props = defineProps({
  placeholder: { type: String, default: "Buscar por..." },
  minChars: { type: Number, default: 2 },
  pageLimit: { type: Number, default: 25 },
  debounceMs: { type: Number, default: 300 },
  fallbackImg: { type: String, default: "/vue.svg" },
});

const q = ref("");
const open = ref(false);
const results = ref([]);
const loadingFirst = ref(false);
const loadingMore = ref(false);
const hasMoreServer = ref(true);
const nextCursorId = ref(null);
const rootEl = ref(null);
const sentinel = ref(null);
let observer = null;
let debounceId = null;

const showModal = ref(false);
const selectedProduct = ref(null);
const currentImageIndex = ref(0);

const formatPrice = (v) => {
  const n = Number(v ?? 0);
  return n.toLocaleString("pt-BR", { style: "currency", currency: "BRL" });
};

const openPanel = () => {
  if (!open.value) open.value = true;
};
const closePanel = () => {
  open.value = false;
};

const openModal = (p) => {
  selectedProduct.value = p;
  currentImageIndex.value = 0;
  showModal.value = true;
  closePanel();
};
const closeModal = () => {
  showModal.value = false;
  selectedProduct.value = null;
  currentImageIndex.value = 0;
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
  if (!selectedProduct.value) return fallbackImg;
  if (
    selectedProduct.value.imagens_url &&
    selectedProduct.value.imagens_url.length > 0
  ) {
    return selectedProduct.value.imagens_url[currentImageIndex.value];
  }
  return selectedProduct.value.imagem_url || fallbackImg;
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

const filterByTitle = (batch, term) => {
  const t = (term || "").trim().toLowerCase();
  if (!t) return [];
  return batch.filter((p) =>
    String(p?.nome || "")
      .toLowerCase()
      .includes(t)
  );
};

const fetchPage = async ({ cursor } = {}) => {
  const params = { limit: props.pageLimit };
  if (cursor) params.cursor_id = cursor;

  if (q.value.trim().length >= props.minChars) {
    params.q = q.value.trim();
  } else {
    return { filtered: [], raw: [] };
  }

  const raw = await getProdutos(params);
  const list = Array.isArray(raw) ? raw : [];

  if (list.length > 0) {
    const last = list[list.length - 1];
    nextCursorId.value = last?.id ?? null;
  }
  if (list.length < props.pageLimit) {
    hasMoreServer.value = false;
  }

  const filtered = filterByTitle(list, q.value);
  return { filtered, raw: list };
};

const loadFirstPage = async () => {
  results.value = [];
  nextCursorId.value = null;
  hasMoreServer.value = true;
  loadingFirst.value = true;

  try {
    const { filtered } = await fetchPage();
    results.value = filtered;
  } catch (e) {
    console.error("Erro na busca:", e);
  } finally {
    loadingFirst.value = false;
  }
};

const loadMore = async () => {
  if (!hasMoreServer.value || loadingMore.value) return;
  loadingMore.value = true;
  try {
    const { filtered } = await fetchPage({ cursor: nextCursorId.value });
    results.value = results.value.concat(filtered);
  } catch (e) {
    console.error(e);
  } finally {
    loadingMore.value = false;
  }
};

watch(
  () => q.value,
  () => {
    if (!open.value) open.value = true;
    if (debounceId) clearTimeout(debounceId);
    debounceId = setTimeout(async () => {
      if (q.value.trim().length >= props.minChars) {
        await loadFirstPage();
        await nextTick();
        const panelEl = rootEl.value?.querySelector(".panel");
        if (panelEl) panelEl.scrollTop = 0;
      } else {
        results.value = [];
        hasMoreServer.value = true;
        nextCursorId.value = null;
      }
    }, props.debounceMs);
  }
);

const onIntersect = async (entries) => {
  const e = entries[0];
  if (!e?.isIntersecting) return;
  await loadMore();
};

onMounted(() => {
  observer = new IntersectionObserver(onIntersect, {
    root: null,
    threshold: 0.1,
  });

  const connectObserverToPanel = () => {
    const panel = rootEl.value?.querySelector(".panel");
    if (panel && sentinel.value) {
      observer.disconnect();
      observer = new IntersectionObserver(onIntersect, {
        root: panel,
        threshold: 0.1,
      });
      observer.observe(sentinel.value);
    }
  };

  watch(open, async (isOpen) => {
    if (isOpen) {
      await nextTick();
      connectObserverToPanel();
    } else {
      if (observer) observer.disconnect();
    }
  });

  const onClickOutside = (ev) => {
    if (!rootEl.value) return;
    if (!rootEl.value.contains(ev.target)) {
      closePanel();
    }
  };
  document.addEventListener("click", onClickOutside);

  onBeforeUnmount(() => {
    if (observer) observer.disconnect();
    document.removeEventListener("click", onClickOutside);
    if (debounceId) clearTimeout(debounceId);
  });
});

const handleSelect = (p) => {
  openModal(p);
};

const addProduct = () => {
  const produto = selectedProduct.value;

  cartStore.addItem({
    id: produto.id,
    img: produto.imagem_url,
    title: produto.nome,
    description: produto.descricao,
    category: produto.categoria,
    stok: produto.estoque,
    price: Number(produto.preco),
    qty: 1,
  });
  cartStore.openCart();
  closeModal();
};
</script>

<style scoped>
.searchbar-group {
  position: relative;
  display: flex;
  align-items: center;
  line-height: 28px;
  width: 100%;
}

.input {
  width: 100%;
  height: 40px;
  padding: 0 1.2rem 0 3.5rem;
  border: 2px solid #ede5dd;
  border-radius: 28px;
  outline: none;
  background-color: #ede5dd;
  color: #232121;
  font-size: 18px;
  font-weight: 500;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  box-shadow: 0 2px 8px rgba(115, 94, 89, 0.1);
}

.input::placeholder {
  color: #735e59;
  opacity: 0.7;
  font-weight: 400;
}

.input:focus,
.input:hover {
  border-color: #735e59;
  background-color: #ffffff;
  box-shadow: 0 4px 20px rgba(115, 94, 89, 0.15);
  transform: translateY(-1px);
  cursor: pointer;
}

.input:focus {
  box-shadow: 0 4px 24px rgba(115, 94, 89, 0.2);
}

.icon {
  position: absolute;
  left: 1.4rem;
  color: #735e59;
  width: 1.4rem;
  height: 1rem;
  transition: all 0.3s ease;
  z-index: 10;
}

.input:focus + .icon,
.input:hover + .icon {
  color: #735e59;
}

.panel {
  position: absolute;
  top: 44px;
  left: 0;
  right: 0;
  z-index: 50;
  max-height: 480px;
  overflow: auto;
  background: #ffffff;
  border: 2px solid #ede5dd;
  border-radius: 16px;
  box-shadow: 0 16px 64px rgba(115, 94, 89, 0.15);
  padding: 8px 0;
  backdrop-filter: blur(10px);
  animation: slideDown 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

@keyframes slideDown {
  from {
    opacity: 0;
    transform: translateY(-10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.item {
  display: grid;
  grid-template-columns: 64px 1fr;
  gap: 12px;
  align-items: center;
  padding: 12px 16px;
  cursor: pointer;
  transition: all 0.2s ease;
  border-radius: 8px;
  margin: 0 8px;
}

.item:hover {
  background: linear-gradient(135deg, #ede5dd 0%, #f5f0e8 100%);
  transform: translateX(4px);
  box-shadow: 0 4px 12px rgba(115, 94, 89, 0.1);
}

.thumb {
  width: 64px;
  height: 64px;
  object-fit: cover;
  border-radius: 12px;
  background: #ede5dd;
  border: 2px solid #ffffff;
  box-shadow: 0 4px 12px rgba(115, 94, 89, 0.1);
  transition: all 0.2s ease;
}

.item:hover .thumb {
  transform: scale(1.05);
  box-shadow: 0 6px 16px rgba(115, 94, 89, 0.15);
}

.meta {
  display: flex;
  flex-direction: column;
  gap: 6px;
  min-width: 0;
}

.title {
  font-size: 12px;
  font-weight: 600;
  line-height: 1.4;
  color: #232121;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.price-row {
  display: flex;
  gap: 12px;
  align-items: baseline;
}

.price {
  font-weight: 700;
  font-size: 16px;
  color: #735e59;
  background: linear-gradient(135deg, #735e59 0%, #b9a994 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.muted {
  color: #735e59;
  opacity: 0.7;
  font-size: 14px;
  font-weight: 500;
}

.state {
  padding: 20px;
  text-align: center;
  color: #735e59;
  font-weight: 500;
}

.sentinel {
  height: 1px;
}

.panel::-webkit-scrollbar {
  width: 6px;
}

.panel::-webkit-scrollbar-track {
  background: #ede5dd;
  border-radius: 3px;
}

.panel::-webkit-scrollbar-thumb {
  background: #b9a994;
  border-radius: 3px;
}

.panel::-webkit-scrollbar-thumb:hover {
  background: #735e59;
}

@media (max-width: 768px) {
  .input {
    height: 52px;
    padding: 0 1rem 0 3rem;
    font-size: 16px;
    border-radius: 26px;
  }

  .icon {
    left: 1.2rem;
    width: 1.2rem;
    height: 1.2rem;
  }

  .panel {
    top: 56px;
  }

  .item {
    padding: 10px 12px;
    grid-template-columns: 56px 1fr;
    gap: 10px;
  }

  .thumb {
    width: 56px;
    height: 56px;
  }

  .title {
    font-size: 11px;
  }

  .price {
    font-size: 14px;
  }
}
</style>
