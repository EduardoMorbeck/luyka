import { reactive, watch } from "vue";

const STORAGE_KEY = "cart:data:v1"; // troquei nome para deixar claro que guarda mais do que items

function loadFromStorage() {
  try {
    const raw = localStorage.getItem(STORAGE_KEY);
    if (!raw)
      return {
        items: [],
        cep: "",
        shippingSelected: null,
        shippingOptions: [],
      };
    const obj = JSON.parse(raw);

    // garante que tem estrutura mínima
    if (typeof obj !== "object" || obj === null)
      return {
        items: [],
        cep: "",
        shippingSelected: null,
        shippingOptions: [],
      };

    // normaliza itens
    const items = Array.isArray(obj.items)
      ? obj.items.map((i) => ({
          key: i.key ?? i.id ?? i.title,
          id: i.id ?? null,
          title: i.title ?? "",
          description: i.description ?? "",
          category: i.category ?? "",
          img: i.img ?? "",
          price: Number(i.price) || 0,
          stok: Number(i.stok) || 0,
          qty: Number(i.qty) || 1,
        }))
      : [];

    return {
      items,
      cep: obj.cep ?? "",
      shippingSelected: obj.shippingSelected ?? null,
      shippingOptions: Array.isArray(obj.shippingOptions)
        ? obj.shippingOptions
        : [],
    };
  } catch {
    return {
      items: [],
      cep: "",
      shippingSelected: null,
      shippingOptions: [],
    };
  }
}

function saveToStorage(state) {
  try {
    localStorage.setItem(
      STORAGE_KEY,
      JSON.stringify({
        items: state.items,
        cep: state.cep,
        shippingSelected: state.shippingSelected,
        shippingOptions: state.shippingOptions,
      })
    );
  } catch {}
}

let errorTimer = null;

const initial = loadFromStorage();

export const cartStore = reactive({
  open: false,
  items: initial.items,
  error: null,
  cep: initial.cep,
  shippingSelected: initial.shippingSelected,
  shippingOptions: initial.shippingOptions,

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

  addItem(product) {
    const priceNumber =
      typeof product.price === "string"
        ? Number(product.price.replace(/\./g, "").replace(",", "."))
        : Number(product.price) || 0;

    const key = this._keyOf(product);
    const incomingQty = Number(product.qty ?? 1);
    const stokIncoming = Number(product.stok ?? 0);

    const existing = this.items.find((i) => i.key === key);
    const currentQty = existing ? Number(existing.qty) : 0;
    const currentStok = existing ? Number(existing.stok) : stokIncoming;

    const effectiveStok = Number.isFinite(currentStok) ? currentStok : 0;
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
      if (stokIncoming) existing.stok = Number(stokIncoming);
      if (priceNumber) existing.price = priceNumber;
    } else {
      this.items.unshift({
        key,
        id: product.id ?? null,
        title: product.title ?? "",
        description: product.description ?? "",
        category: product.category ?? "",
        img: product.img ?? "",
        price: priceNumber,
        stok: effectiveStok,
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
      this.shippingSelected = null;
      this.shippingOptions = [];
      try {
        localStorage.removeItem(STORAGE_KEY);
      } catch {}
    }
  },

  clear() {
    this.items.splice(0);
    this.shippingSelected = null;
    this.cep = "";
    this.shippingOptions = [];
    try {
      localStorage.removeItem(STORAGE_KEY);
    } catch {}
  },

  // Setter para CEP
  setCep(cep) {
    this.cep = cep;
  },

  // Setter para objeto shipping completo
  setShippingSelected(shipping) {
    this.shippingSelected = shipping;
  },

  // Setter para opções de frete
  setShippingOptions(options) {
    this.shippingOptions = options;
  },

  get count() {
    return this.items.reduce((acc, i) => acc + i.qty, 0);
  },
  get subtotal() {
    return this.items.reduce((acc, i) => acc + i.qty * i.price, 0);
  },
});

// 🔄 salva sempre que items, cep, shippingSelected ou shippingOptions mudar
watch(
  () => ({
    items: cartStore.items.map((i) => ({
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
    cep: cartStore.cep,
    shippingSelected: cartStore.shippingSelected,
    shippingOptions: cartStore.shippingOptions,
  }),
  (state) => saveToStorage(state),
  { deep: true }
);
