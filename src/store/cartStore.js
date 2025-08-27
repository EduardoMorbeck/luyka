import { reactive, watch } from "vue";

const STORAGE_KEY = "cart:items:v1";

function loadItemsFromStorage() {
  try {
    const raw = localStorage.getItem(STORAGE_KEY);
    if (!raw) return [];
    const arr = JSON.parse(raw);
    if (!Array.isArray(arr)) return [];
    return arr.map((i) => ({
      key: i.key ?? i.id ?? i.title,
      id: i.id ?? null,
      title: i.title ?? "",
      description: i.description ?? "",
      category: i.category ?? "",
      img: i.img ?? "",
      price: Number(i.price) || 0,
      stok: Number(i.stok) || 0, // estoque disponível
      qty: Number(i.qty) || 1,
    }));
  } catch {
    return [];
  }
}

function saveItemsToStorage(items) {
  try {
    localStorage.setItem(STORAGE_KEY, JSON.stringify(items));
  } catch {}
}

let errorTimer = null;

export const cartStore = reactive({
  open: false,
  items: loadItemsFromStorage(),
  error: null, // mensagem de erro visível na UI

  openCart() {
    this.open = true;
  },
  closeCart() {
    this.open = false;
  },

  setError(message, ms = 3500) {
    this.error = message;
    if (errorTimer) clearTimeout(errorTimer);
    errorTimer = setTimeout(() => {
      this.error = null;
    }, ms);
  },

  _keyOf(p) {
    return p.id ?? p.title;
  },

  /**
   * Adiciona item respeitando o estoque (stok).
   * Retorna { ok: boolean, message?: string }
   */
  addItem(product) {
    const priceNumber =
      typeof product.price === "string"
        ? Number(product.price.replace(/\./g, "").replace(",", "."))
        : Number(product.price) || 0;

    const key = this._keyOf(product);
    const incomingQty = Number(product.qty ?? 1);

    // estoque informado no payload ou existente no carrinho
    const stokIncoming = Number(product.stok ?? 0);

    const existing = this.items.find((i) => i.key === key);
    const currentQty = existing ? Number(existing.qty) : 0;
    const currentStok = existing ? Number(existing.stok) : stokIncoming;

    // Se não temos informação de estoque, consideramos 0 (bloqueia compra)
    const effectiveStok = Number.isFinite(currentStok) ? currentStok : 0;

    // Quantidade após adicionar
    const finalQty = currentQty + incomingQty;

    if (effectiveStok <= 0) {
      const msg = "Produto esgotado no momento.";
      this.setError(msg);
      return { ok: false, message: msg };
    }

    if (finalQty > effectiveStok) {
      const disponivel = Math.max(effectiveStok - currentQty, 0);
      const msg =
        disponivel > 0
          ? `Quantidade indisponível. Restam apenas ${disponivel} unidade(s).`
          : "Você já atingiu o limite do estoque para este produto.";
      this.setError(msg);
      return { ok: false, message: msg };
    }

    if (existing) {
      existing.qty = finalQty;
      // garante que estoque e preço estejam sincronizados
      if (stokIncoming) existing.stok = Number(stokIncoming);
      if (priceNumber) existing.price = priceNumber;
    } else {
      this.items.push({
        key,
        id: product.id ?? null,
        title: product.title ?? "",
        description: product.description ?? "",
        category: product.category ?? "",
        img: product.img ?? "",
        price: priceNumber,
        stok: effectiveStok, // salva estoque no item
        qty: incomingQty,
      });
    }

    return { ok: true };
  },

  increment(key) {
    const it = this.items.find((i) => i.key === key);
    if (!it) return;

    const stok = Number(it.stok ?? 0);
    const next = Number(it.qty) + 1;

    if (stok <= 0) {
      this.setError("Produto esgotado no momento.");
      return;
    }
    if (next > stok) {
      this.setError(
        `Quantidade indisponível. Estoque máximo: ${stok} unidade(s).`
      );
      return;
    }

    it.qty = next;
  },

  decrement(key) {
    const it = this.items.find((i) => i.key === key);
    if (!it) return;
    if (it.qty > 1) it.qty--;
    else this.removeItem(key);
  },

  removeItem(key) {
    const idx = this.items.findIndex((i) => i.key === key);
    if (idx > -1) this.items.splice(idx, 1);
    if (this.items.length === 0) {
      try {
        localStorage.removeItem(STORAGE_KEY);
      } catch {}
    }
  },

  clear() {
    this.items.splice(0);
    try {
      localStorage.removeItem(STORAGE_KEY);
    } catch {}
  },

  get count() {
    return this.items.reduce((acc, i) => acc + i.qty, 0);
  },
  get subtotal() {
    return this.items.reduce((acc, i) => acc + i.qty * i.price, 0);
  },
});

watch(
  () =>
    cartStore.items.map((i) => ({
      key: i.key,
      id: i.id,
      title: i.title,
      description: i.description,
      category: i.category,
      img: i.img,
      price: i.price,
      stok: i.stok,
      qty: i.qty,
    })),
  (items) => saveItemsToStorage(items),
  { deep: true }
);
