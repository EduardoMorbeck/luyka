<template>
  <div class="searchbar-group" ref="rootEl">
    <i class="icon fa-solid fa-magnifying-glass"></i>
    <input
      v-model="q"
      :placeholder="placeholder"
      type="search"
      class="input"
      @focus="openPanel()"
    />

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
      class="fixed inset-0 bg-black/50 backdrop-blur-sm flex items-center justify-center z-50"
      @click="closeModal"
    >
      <div
        class="bg-white rounded-lg shadow-lg p-8 relative max-w-md w-full"
        @click.stop
      >
        <button class="p-2 absolute top-2 right-2" @click="closeModal">
          <div
            class="flex items-center justify-center cursor-pointer py-2 px-3 rounded-full bg-gray-100 hover:bg-gray-200"
          >
            <i class="fa-solid fa-xmark text-xl"></i>
          </div>
        </button>

        <img
          :src="selectedProduct.imagem_url || fallbackImg"
          :alt="selectedProduct.nome"
          class="w-80 h-80 mx-auto object-cover rounded-lg"
        />
        <h2 class="text-2xl font-bold text-center mt-4">
          {{ selectedProduct.nome }}
        </h2>
        <p class="text-gray-600 text-center">
          {{ selectedProduct.descricao }}
        </p>
        <p class="text-2xl font-bold text-center mt-4 text-gray-800">
          {{ formatPrice(selectedProduct.preco ?? selectedProduct.valor) }}
        </p>

        <div class="flex justify-center mt-6">
          <button
            :disabled="Number(selectedProduct.estoque) == 0"
            @click.stop="addProduct"
            class="mt-4 w-full py-2 rounded-full bg-btn border-2 border-dark text-dark font-medium hover:brightness-110 transition disabled:opacity-50 disabled:cursor-not-allowed"
          >
            {{ Number(selectedProduct.estoque) > 0 ? "Comprar" : "Esgotado" }}
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
  padding: 0 1rem 0 2.5rem;
  border: 2px solid transparent;
  border-radius: 8px;
  outline: none;
  background-color: #f3f3f4;
  color: #0d0c22;
  transition: 0.2s ease;
}
.input::placeholder {
  color: #9e9ea7;
}
.input:focus,
.input:hover {
  border-color: #735e59;
  background-color: #fff;
}
.icon {
  position: absolute;
  left: 1rem;
  color: #9e9ea7;
  width: 1rem;
  height: 1rem;
}

.panel {
  position: absolute;
  top: 44px;
  left: 0;
  right: 0;
  z-index: 50;
  max-height: 420px; /* scroll aqui */
  overflow: auto;
  background: #fff;
  border: 1px solid #e6e6e8;
  border-radius: 10px;
  box-shadow: 0 8px 30px rgba(0, 0, 0, 0.08);
  padding: 6px 0;
}

.item {
  display: grid;
  grid-template-columns: 56px 1fr 18px;
  gap: 10px;
  align-items: center;
  padding: 10px 12px;
  cursor: pointer;
}
.item:hover {
  background: #f8f8f9;
}
.thumb {
  width: 56px;
  height: 56px;
  object-fit: cover;
  border-radius: 6px;
  background: #f3f3f4;
}
.meta {
  display: flex;
  flex-direction: column;
  gap: 4px;
}
.title {
  font-size: 12px;
  line-height: 1.2;
}
.price-row {
  display: flex;
  gap: 10px;
  align-items: baseline;
}
.price {
  font-weight: 700;
  font-size: 14px;
}
.muted {
  color: #7b7b84;
  font-size: 12px;
}
.arrow {
  font-size: 18px;
  color: #bdbdc5;
}

.see-all {
  display: block;
  width: 100%;
  text-align: center;
  background: transparent;
  border: 0;
  color: #2a66f1;
  font-weight: 600;
  padding: 10px 0;
  cursor: pointer;
}

.sentinel {
  height: 1px;
}
.state {
  padding: 12px;
  text-align: center;
}
</style>
