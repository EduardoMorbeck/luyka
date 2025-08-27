<template>
  <div class="w-full flex flex-col py-28 px-4 gap-8">
    <h2 class="font-bold text-center text-3xl w-full mb-2">PRODUTOS</h2>

    <div class="w-full max-w-5xl mx-auto grid grid-cols-1 md:grid-cols-3 gap-4">
      <label class="flex flex-col text-sm gap-1">
        <span class="font-medium">Categoria</span>
        <select v-model="selectedCategory" class="border rounded-lg px-3 py-2">
          <option value="">Todas</option>
          <option v-for="c in categories" :key="c" :value="c">{{ c }}</option>
        </select>
      </label>

      <label class="flex flex-col text-sm gap-1">
        <span class="font-medium">Ordenar por preço</span>
        <select v-model="priceOrder" class="border rounded-lg px-3 py-2">
          <option value="">Sem ordenar</option>
          <option value="asc">Menor → Maior</option>
          <option value="desc">Maior → Menor</option>
        </select>
      </label>

      <label class="flex flex-col text-sm gap-1">
        <span class="font-medium">Ordenar por nome</span>
        <select v-model="nameOrder" class="border rounded-lg px-3 py-2">
          <option value="">Sem ordenar</option>
          <option value="az">A → Z</option>
          <option value="za">Z → A</option>
        </select>
      </label>
    </div>

    <div class="w-full flex flex-wrap justify-center px-4 gap-8">
      <div v-for="(product, idx) in visibleProducts" :key="product.id ?? idx">
        <ProductCard :product="product" />
      </div>

      <div
        v-if="!loadingAll && visibleProducts.length === 0"
        class="opacity-60"
      >
        Nenhum produto encontrado.
      </div>
    </div>

    <div v-if="loadingFirstPage" class="text-center opacity-70">
      Carregando...
    </div>
    <div v-else class="w-full flex justify-center">
      <div v-if="loadingMore" class="text-center opacity-70 my-4">
        Carregando mais...
      </div>
      <div ref="sentinel" class="h-6"></div>
    </div>
  </div>
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

onBeforeUnmount(() => {
  if (observer && sentinel.value) observer.unobserve(sentinel.value);
});
</script>
