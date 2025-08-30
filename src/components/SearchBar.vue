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

    <!-- Painel de resultados -->
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

        <div v-if="loadingMore" class="state muted">Carregando mais…</div>

        <!-- Sentinela do scroll infinito -->
        <div ref="sentinel" class="sentinel"></div>
      </template>
    </div>

    <!-- Modal do produto -->
    <div
      v-if="showModal && selectedProduct"
      class="modal-overlay"
      @click="closeModal"
    >
      <div class="modal-content" @click.stop>
        <button class="modal-close" @click="closeModal">
          <i class="fa-solid fa-xmark"></i>
        </button>

        <div class="modal-image-wrapper">
          <img
            :src="selectedProduct.imagem_url || fallbackImg"
            :alt="selectedProduct.nome"
            class="modal-image"
          />
        </div>

        <div class="modal-info">
          <h2 class="modal-title">
            {{ selectedProduct.nome }}
          </h2>
          <p class="modal-description">
            {{ selectedProduct.descricao }}
          </p>
          <p class="modal-price">
            {{ formatPrice(selectedProduct.preco ?? selectedProduct.valor) }}
          </p>

          <button
            :disabled="Number(selectedProduct.estoque) == 0"
            @click.stop="addProduct"
            class="modal-button"
            :class="{
              'modal-button-disabled': Number(selectedProduct.estoque) == 0,
            }"
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
</template>

<script setup>
import { ref, watch, onMounted, onBeforeUnmount, nextTick } from "vue";
import { getProdutos } from "/src/api.js";
import { cartStore } from "../store/cartStore";

/**
 * Props
 */
const props = defineProps({
  placeholder: { type: String, default: "Buscar por..." },
  minChars: { type: Number, default: 2 },
  pageLimit: { type: Number, default: 25 },
  debounceMs: { type: Number, default: 300 },
  fallbackImg: { type: String, default: "/vue.svg" },
  /**
   * Função a ser chamada ao clicar em "Comprar" no modal.
   * Recebe o produto selecionado como argumento.
   * (Mantém o nome solicitado: addProcuct)
   */
  // addProcuct: { type: Function, default: () => {} },
});

/**
 * Estado
 */
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

/**
 * Utils
 */
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
  showModal.value = true;
};
const closeModal = () => {
  showModal.value = false;
  selectedProduct.value = null;
};

/**
 * Filtrar por TÍTULO (nome) no client
 */
const filterByTitle = (batch, term) => {
  const t = (term || "").trim().toLowerCase();
  if (!t) return [];
  return batch.filter((p) =>
    String(p?.nome || "")
      .toLowerCase()
      .includes(t)
  );
};

/**
 * Buscar uma página do servidor (respeita cursor e q)
 */
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

/**
 * Carregar primeira página
 */
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

/**
 * Carregar mais (scroll infinito)
 */
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

/**
 * Debounce da digitação
 */
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

/**
 * IntersectionObserver para scroll infinito
 */
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

/**
 * Ações
 */
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

/* Scrollbar personalizada */
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

/* Estilos do Modal */
.modal-overlay {
  position: fixed;
  inset: 0;
  background: rgba(115, 94, 89, 0.6);
  backdrop-filter: blur(8px);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 100;
  animation: fadeIn 0.3s ease;
}

@keyframes fadeIn {
  from {
    opacity: 0;
  }
  to {
    opacity: 1;
  }
}

.modal-content {
  background: linear-gradient(135deg, #ffffff 0%, #fdfcfa 100%);
  border-radius: 24px;
  box-shadow: 0 24px 80px rgba(115, 94, 89, 0.3);
  position: relative;
  max-width: 420px;
  width: 90%;
  max-height: 90vh;
  overflow-y: auto;
  border: 2px solid #ede5dd;
  animation: slideUp 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

@keyframes slideUp {
  from {
    opacity: 0;
    transform: translateY(20px) scale(0.95);
  }
  to {
    opacity: 1;
    transform: translateY(0) scale(1);
  }
}

.modal-close {
  position: absolute;
  top: 16px;
  right: 16px;
  width: 40px;
  height: 40px;
  border-radius: 50%;
  background: rgba(255, 255, 255, 0.9);
  border: 2px solid #ede5dd;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: all 0.2s ease;
  z-index: 10;
  color: #735e59;
  font-size: 16px;
}

.modal-close:hover {
  background: #ede5dd;
  transform: scale(1.1);
  box-shadow: 0 4px 12px rgba(115, 94, 89, 0.2);
}

.modal-image-wrapper {
  padding: 24px 24px 0;
}

.modal-image {
  width: 100%;
  height: 280px;
  object-fit: cover;
  border-radius: 16px;
  background: #ede5dd;
  box-shadow: 0 8px 24px rgba(115, 94, 89, 0.15);
}

.modal-info {
  padding: 20px 24px 24px;
}

.modal-title {
  font-size: 24px;
  font-weight: 700;
  color: #232121;
  text-align: center;
  margin-bottom: 12px;
  font-family: "Prata", serif;
  line-height: 1.2;
}

.modal-description {
  color: #735e59;
  text-align: center;
  margin-bottom: 16px;
  font-size: 14px;
  line-height: 1.5;
  opacity: 0.8;
}

.modal-price {
  font-size: 28px;
  font-weight: 700;
  text-align: center;
  margin-bottom: 24px;
  background: linear-gradient(135deg, #735e59 0%, #b9a994 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  font-family: "Prata", serif;
}

.modal-button {
  width: 100%;
  padding: 16px 24px;
  border-radius: 16px;
  background: linear-gradient(135deg, #ede5dd 0%, #f5f0e8 100%);
  border: 2px solid #735e59;
  color: #735e59;
  font-weight: 600;
  font-size: 16px;
  cursor: pointer;
  transition: all 0.3s ease;
  box-shadow: 0 4px 12px rgba(115, 94, 89, 0.1);
}

.modal-button:hover:not(.modal-button-disabled) {
  background: linear-gradient(135deg, #735e59 0%, #b9a994 100%);
  color: #ffffff;
  transform: translateY(-2px);
  box-shadow: 0 8px 24px rgba(115, 94, 89, 0.2);
}

.modal-button-disabled {
  opacity: 0.5;
  cursor: not-allowed;
  background: #f3f3f4;
  border-color: #e6e6e8;
  color: #9e9ea7;
}

/* Responsividade */
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

  .modal-content {
    max-width: 350px;
    margin: 20px;
  }

  .modal-image {
    height: 240px;
  }

  .modal-title {
    font-size: 20px;
  }

  .modal-price {
    font-size: 24px;
  }

  .modal-button {
    padding: 14px 20px;
    font-size: 14px;
  }
}
</style>
