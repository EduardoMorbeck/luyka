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
      img: i.img ?? "",
      price: Number(i.price) || 0,
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

export const cartStore = reactive({
  open: false,
  items: loadItemsFromStorage(),

  openCart() {
    this.open = true;
  },
  closeCart() {
    this.open = false;
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
    const existing = this.items.find((i) => i.key === key);

    if (existing) {
      existing.qty += product.qty ?? 1;
    } else {
      this.items.push({
        key,
        id: product.id ?? null,
        title: product.title,
        img: product.img,
        price: priceNumber,
        qty: product.qty ?? 1,
      });
    }
  },

  increment(key) {
    const it = this.items.find((i) => i.key === key);
    if (it) it.qty++;
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
      img: i.img,
      price: i.price,
      qty: i.qty,
    })),
  (items) => saveItemsToStorage(items),
  { deep: true }
);
