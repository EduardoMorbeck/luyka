<template>
  <div class="flex flex-col relative">
    <button
      class="cursor-pointer group"
      @click="cartStore.openCart()"
      aria-label="Abrir carrinho"
    >
      <i
        class="fa-solid fa-cart-shopping text-[#232121] text-2xl group-hover:text-[#735e59] transition-colors"
      ></i>
    </button>

    <span class="text-xs text-[#423734] font-medium"
      >R$ {{ cartStore.subtotal.toFixed(2).replace(".", ",") }}</span
    >

    <div
      v-if="cartStore.items.length > 0"
      class="absolute bottom-8 left-9 flex bg-gradient-to-r from-[#735e59] to-[#735e59] text-white rounded-full px-2 py-1 text-xs font-semibold shadow-lg"
    >
      {{ cartStore.count }}
    </div>
  </div>

  <Teleport to="body">
    <Transition name="fade">
      <div
        v-if="cartStore.open"
        class="fixed inset-0 z-[60] backdrop-blur-xs"
        @click="cartStore.closeCart()"
        aria-hidden="true"
      />
    </Transition>

    <Transition name="slide-in-right">
      <section
        v-if="cartStore.open"
        class="fixed inset-y-0 right-0 z-[70] w-full max-w-lg bg-gradient-to-br from-[#ede5dd] via-white to-[#b9a994] shadow-2xl flex flex-col overflow-y-auto max-h-screen"
        role="dialog"
        aria-modal="true"
      >
        <header class="p-6 pb-4">
          <div class="flex items-center justify-between">
            <div class="flex items-center gap-3">
              <div
                class="w-10 h-10 bg-white rounded-full flex items-center justify-center shadow-md"
              >
                <i class="fa-solid fa-cart-shopping text-[#735e59] text-lg"></i>
              </div>
              <div>
                <h1 class="text-xl font-bold text-[#232121]">Seu Carrinho</h1>
                <p class="text-sm text-[#423734]">
                  {{ cartStore.items.length }} item(s)
                </p>
              </div>
            </div>
            <button
              class="p-2 hover:bg-white hover:bg-opacity-20 rounded-full transition-colors cursor-pointer"
              @click="cartStore.closeCart()"
              aria-label="Fechar carrinho"
            >
              <i
                class="fa-solid fa-xmark text-[#232121] text-xl hover:text-[#735e59]"
              ></i>
            </button>
          </div>
        </header>

        <section
          class="bg-white mx-4 rounded-2xl shadow-lg border border-[#ede5dd] mb-4"
        >
          <header class="p-4 border-b border-[#ede5dd]">
            <div class="flex items-center gap-3">
              <div
                class="w-8 h-8 bg-[#ede5dd] rounded-full flex items-center justify-center"
              >
                <i class="fa-solid fa-box text-[#735e59] text-sm"></i>
              </div>
              <h2 class="text-lg font-bold text-[#232121]">Produtos</h2>
            </div>
          </header>

          <div class="p-4 overflow-y-auto max-h-96">
            <template v-if="cartStore.items.length > 0">
              <div
                v-for="item in cartStore.items"
                :key="item.key"
                class="bg-[#ede5dd] rounded-xl p-4 mb-3 last:mb-0 hover:bg-[#b9a994] hover:bg-opacity-30 transition-all duration-200 cursor-pointer"
              >
                <div class="flex gap-4">
                  <img
                    v-if="item.img"
                    :src="item.img"
                    :alt="item.title"
                    class="w-16 h-16 object-cover rounded-lg border-2 border-white shadow-sm"
                  />

                  <div class="flex-1">
                    <div class="flex items-start justify-between gap-2 mb-2">
                      <h3 class="font-semibold text-[#232121] leading-tight">
                        {{ item.title }}
                      </h3>
                      <button
                        class="p-1 px-2 hover:bg-white hover:bg-opacity-50 rounded-full transition-colors cursor-pointer"
                        @click.stop="cartStore.removeItem(item.key)"
                        aria-label="Remover produto"
                        title="Remover"
                      >
                        <i class="fa-solid fa-trash text-[#735e59] text-sm"></i>
                      </button>
                    </div>

                    <div class="mb-3">
                      <span
                        v-if="Number(item.stok) > 0"
                        class="text-xs text-[#423734]"
                      >
                        Estoque: {{ item.stok }} • Restam
                        {{ Math.max(Number(item.stok) - Number(item.qty), 0) }}
                      </span>
                      <span v-else class="text-xs text-red-600 font-medium">
                        Esgotado
                      </span>
                    </div>

                    <div class="flex items-center justify-between">
                      <div
                        class="inline-flex items-center bg-white border-2 border-[#b9a994] rounded-full shadow-sm"
                      >
                        <button
                          class="flex items-center justify-center w-8 h-8 hover:bg-[#ede5dd] rounded-full transition-colors cursor-pointer"
                          @click.stop="cartStore.decrement(item.key)"
                          aria-label="Diminuir quantidade"
                          title="Diminuir"
                        >
                          <i
                            class="fa-solid fa-minus text-[#735e59] text-xs"
                          ></i>
                        </button>
                        <span
                          class="px-3 select-none min-w-8 text-center font-semibold text-[#232121]"
                          >{{ item.qty }}</span
                        >
                        <button
                          :disabled="
                            Number(item.stok) === 0 ||
                            Number(item.qty) >= Number(item.stok)
                          "
                          class="flex items-center justify-center w-8 h-8 hover:bg-[#ede5dd] rounded-full transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
                          @click.stop="cartStore.increment(item.key)"
                          aria-label="Aumentar quantidade"
                          :title="
                            Number(item.qty) >= Number(item.stok)
                              ? `Estoque máximo: ${item.stok}`
                              : 'Aumentar'
                          "
                        >
                          <i
                            class="fa-solid fa-plus text-[#735e59] text-xs"
                          ></i>
                        </button>
                      </div>

                      <div class="text-right">
                        <div class="font-bold text-[#735e59] text-lg">
                          R$
                          {{
                            (Number(item.price) * Number(item.qty))
                              .toFixed(2)
                              .replace(".", ",")
                          }}
                        </div>
                        <div class="text-xs text-[#423734]">
                          {{ formatBRL(Number(item.price)) }} × {{ item.qty }}
                        </div>
                      </div>
                    </div>

                    <div
                      v-if="Number(item.qty) >= Number(item.stok)"
                      class="mt-2 text-xs text-red-600 bg-red-50 p-2 rounded-lg"
                    >
                      ⚠️ Você atingiu o limite de estoque para este produto.
                    </div>
                  </div>
                </div>
              </div>
            </template>

            <div v-else class="text-center py-8">
              <div
                class="w-16 h-16 bg-[#ede5dd] rounded-full flex items-center justify-center mx-auto mb-4"
              >
                <i
                  class="fa-solid fa-cart-shopping text-[#b9a994] text-2xl"
                ></i>
              </div>
              <p class="text-[#423734] font-medium">O carrinho está vazio</p>
              <p class="text-sm text-[#b9a994] mt-1">
                Adicione produtos para começar suas compras
              </p>
            </div>
          </div>
        </section>

        <section
          v-if="cartStore.items.length > 0"
          class="bg-white mx-4 rounded-2xl shadow-lg border border-[#ede5dd] mb-4"
        >
          <header class="p-4 border-b border-[#ede5dd]">
            <div class="flex items-center gap-3">
              <div
                class="w-8 h-8 bg-[#ede5dd] rounded-full flex items-center justify-center"
              >
                <i class="fa-solid fa-gift text-[#735e59] text-sm"></i>
              </div>
              <div>
                <h2 class="text-lg font-bold text-[#232121]">
                  Presente Especial
                </h2>
                <p class="text-xs text-[#423734]">
                  A partir de R$
                  {{ GIFT_THRESHOLD.toFixed(2).replace(".", ",") }}
                </p>
              </div>
            </div>
          </header>

          <div class="p-4" role="status" aria-live="polite">
            <div class="flex items-center justify-between text-sm mb-3">
              <span class="text-[#423734]">Progresso para o brinde</span>
              <span class="font-semibold text-[#735e59]"
                >{{ progressPercent }}%</span
              >
            </div>

            <div
              class="w-full h-4 bg-[#ede5dd] rounded-full overflow-hidden mb-3"
            >
              <div
                class="h-4 rounded-full transition-[width] duration-500 ease-out"
                :class="
                  eligible
                    ? 'bg-gradient-to-r from-green-500 to-green-600'
                    : 'bg-gradient-to-r from-[#735e59] to-[#b9a994]'
                "
                :style="{ width: progressBarWidth }"
              />
            </div>

            <div
              v-if="eligible"
              class="bg-gradient-to-r from-green-50 to-green-100 border border-green-200 rounded-xl p-4 text-center"
            >
              <div class="text-2xl mb-2">🎁</div>
              <p class="text-sm font-semibold text-green-700">
                Parabéns! Você ganhará um presente especial nesta compra!
              </p>
            </div>
            <div
              v-else
              class="bg-gradient-to-r from-[#ede5dd] to-[#b9a994] bg-opacity-50 rounded-xl p-4 text-center"
            >
              <p class="text-sm text-[#735e59]">
                Faltam apenas
                <span class="font-bold text-[#232121]">
                  R$ {{ remainingToGift.toFixed(2).replace(".", ",") }}
                </span>
                para ganhar um presente!
              </p>
            </div>
          </div>
        </section>

        <section
          v-if="cartStore.items.length > 0"
          class="bg-white mx-4 rounded-2xl shadow-lg border border-[#ede5dd] mb-4"
        >
          <header class="p-4 border-b border-[#ede5dd]">
            <div class="flex items-center gap-3">
              <div
                class="w-8 h-8 bg-[#ede5dd] rounded-full flex items-center justify-center"
              >
                <i class="fa-solid fa-truck text-[#735e59] text-sm"></i>
              </div>
              <div>
                <h2 class="text-lg font-bold text-[#232121]">Calcular Frete</h2>
                <p class="text-xs text-[#423734]">
                  Informe seu CEP para conhecer os valores
                </p>
              </div>
            </div>
          </header>

          <div class="p-4">
            <div class="flex gap-3 items-start mb-4">
              <div class="flex-1">
                <input
                  id="cep"
                  v-model="cep"
                  type="text"
                  inputmode="numeric"
                  autocomplete="postal-code"
                  placeholder="Seu CEP (ex: 01001-000)"
                  class="w-full border-2 border-[#ede5dd] rounded-xl px-4 py-3 bg-white text-[#232121] placeholder-[#b9a994] focus:border-[#735e59] focus:ring-2 focus:ring-[#ede5dd] transition-all"
                  :class="{
                    'border-red-500 focus:border-red-500 focus:ring-red-200':
                      cepInvalid,
                  }"
                  maxlength="9"
                  aria-label="Informe seu CEP"
                  :aria-invalid="cepInvalid ? 'true' : 'false'"
                  @input="maskCep"
                  @keyup.enter="onCalcularFrete"
                />
                <p
                  v-if="cepInvalid"
                  class="mt-2 text-xs text-red-600 flex items-center gap-1"
                >
                  <i class="fa-solid fa-exclamation-triangle"></i>
                  CEP inválido. Use 8 dígitos (ex: 01001-000).
                </p>
              </div>

              <button
                class="px-6 py-3 bg-gradient-to-r from-[#735e59] to-[#b9a994] text-white font-semibold rounded-xl hover:from-[#b9a994] hover:to-[#735e59] focus:outline-none focus:ring-4 focus:ring-[#ede5dd] transition-all duration-200 transform hover:scale-105 disabled:opacity-50 disabled:cursor-not-allowed disabled:transform-none cursor-pointer"
                @click="onCalcularFrete"
                :disabled="isCalculating || cepDigits.length !== 8"
                aria-label="Calcular frete"
                :title="
                  cepDigits.length !== 8
                    ? 'Informe um CEP válido (8 dígitos)'
                    : 'Calcular frete'
                "
              >
                <div v-if="isCalculating" class="flex items-center gap-2">
                  <svg
                    class="animate-spin w-4 h-4"
                    fill="none"
                    viewBox="0 0 24 24"
                  >
                    <circle
                      class="opacity-25"
                      cx="12"
                      cy="12"
                      r="10"
                      stroke="currentColor"
                      stroke-width="4"
                    ></circle>
                    <path
                      class="opacity-75"
                      fill="currentColor"
                      d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"
                    ></path>
                  </svg>
                  Calculando...
                </div>
                <div v-else>Calcular</div>
              </button>
            </div>

            <div
              v-if="freteError"
              class="p-4 bg-red-50 border border-red-200 rounded-xl text-red-600 flex items-center gap-2 mb-4"
              role="alert"
            >
              <i class="fa-solid fa-exclamation-circle"></i>
              {{ freteError }}
            </div>

            <div v-if="shippingOptions.length" class="space-y-3">
              <h3
                class="text-sm font-semibold text-[#232121] flex items-center gap-2"
              >
                <i class="fa-solid fa-shipping-fast text-[#735e59]"></i>
                Formas de Envio Disponíveis
              </h3>

              <div
                class="space-y-3"
                role="radiogroup"
                aria-label="Formas de envio"
              >
                <label
                  v-for="opt in shippingOptions"
                  :key="opt.id"
                  class="flex items-start gap-4 p-4 rounded-xl bg-[#ede5dd] border-2 cursor-pointer transition-all duration-200"
                  :class="{
                    'border-[#735e59]':
                      cartStore.shippingSelected?.id === opt.id,
                    'border-transparent hover:border-[#b9a994]':
                      cartStore.shippingSelected?.id !== opt.id,
                  }"
                >
                  <input
                    type="radio"
                    class="mt-1 w-4 h-4 text-[#735e59] border-[#b9a994] focus:ring-[#ede5dd]"
                    name="shipping"
                    :value="opt.id"
                    :checked="cartStore.shippingSelected?.id === opt.id"
                    :aria-label="`Selecionar ${opt.name}`"
                    @change="cartStore.setShippingSelected(opt)"
                  />
                  <div class="flex-1">
                    <div class="flex items-center justify-between mb-2">
                      <span class="font-semibold text-[#232121] text-lg">{{
                        opt.name
                      }}</span>
                      <span class="font-bold text-[#735e59] text-xl">{{
                        formatBRL(opt.price)
                      }}</span>
                    </div>
                    <div class="flex items-center gap-2 text-[#423734]">
                      <i class="fa-solid fa-clock text-[#735e59] text-sm"></i>
                      <span class="text-sm"
                        >Entrega até dia {{ opt.estimatedDate }}</span
                      >
                    </div>
                  </div>
                </label>
              </div>

              <p class="sr-only" aria-live="polite">
                {{
                  cartStore.shippingSelected
                    ? "Forma de envio selecionada"
                    : "Nenhuma forma de envio selecionada"
                }}
              </p>

              <div
                class="text-xs text-[#423734] italic flex items-center gap-1"
              >
                <i class="fa-solid fa-info-circle text-[#b9a994]"></i>
                O prazo de entrega não contabiliza feriados.
              </div>
            </div>
          </div>
        </section>

        <section
          v-if="cartStore.items.length > 0"
          class="bg-white mx-4 rounded-2xl shadow-lg border border-[#ede5dd] mb-4"
        >
          <header class="p-4 border-b border-[#ede5dd]">
            <div class="flex items-center gap-3">
              <div
                class="w-8 h-8 bg-[#ede5dd] rounded-full flex items-center justify-center"
              >
                <i class="fa-solid fa-calculator text-[#735e59] text-sm"></i>
              </div>
              <h2 class="text-lg font-bold text-[#232121]">Resumo do Pedido</h2>
            </div>
          </header>

          <div class="p-4" role="status" aria-live="polite">
            <div class="space-y-3 text-sm">
              <div class="flex items-center justify-between">
                <span class="text-[#423734]">Subtotal (sem frete)</span>
                <span class="font-semibold text-[#232121]">{{
                  formatBRL(cartStore.subtotal)
                }}</span>
              </div>
              <div
                v-if="shippingPrice > 0"
                class="flex items-center justify-between"
              >
                <span class="text-[#423734]"
                  >Frete ({{ shippingSelected?.name || "—" }})</span
                >
                <span class="font-semibold text-[#232121]">{{
                  formatBRL(shippingPrice)
                }}</span>
              </div>
              <div
                class="pt-3 border-t border-[#ede5dd] flex items-center justify-between text-lg font-bold"
              >
                <span class="text-[#232121]">Total</span>
                <span
                  class="text-2xl bg-gradient-to-r from-[#735e59] to-[#b9a994] bg-clip-text text-transparent"
                >
                  {{ formatBRL(totalWithFreight) }}
                </span>
              </div>
            </div>
          </div>
        </section>

        <div class="p-4 space-y-3">
          <div v-if="cartStore.items.length > 0" class="w-full">
            <a
              href="/entrega"
              class="w-full text-center px-8 py-4 text-xl bg-gradient-to-r from-[#735e59] to-[#b9a994] text-white font-bold rounded-2xl shadow-lg hover:from-[#b9a994] hover:to-[#735e59] focus:outline-none focus:ring-4 focus:ring-[#ede5dd] transform hover:scale-105 transition-all duration-200 flex items-center justify-center gap-3 cursor-pointer"
            >
              <i class="fa-solid fa-arrow-right"></i>
              Iniciar Compra
            </a>
          </div>

          <button
            @click="cartStore.closeCart()"
            class="w-full px-8 py-3 text-lg text-[#735e59] hover:text-[#232121] font-semibold hover:bg-white hover:bg-opacity-50 rounded-xl transition-all duration-200 flex items-center justify-center gap-2 cursor-pointer"
          >
            <i class="fa-solid fa-shopping-bag"></i>
            Continuar Comprando
          </button>
        </div>
      </section>
    </Transition>
  </Teleport>
</template>

<script setup>
import { ref, computed, watch, onMounted, onBeforeUnmount } from "vue";
import { cartStore } from "../store/cartStore";
import { calcularFrete } from "/src/api.js";

const produto = {
  from_postal_code: "95088325",
  to_postal_code: "",
  height: 5,
  width: 12,
  length: 16,
  weight: 0.3,
};

const cep = ref("");
const isCalculating = ref(false);
const freteResp = ref([]);
const freteError = ref("");

const formatBRL = (n) =>
  (Number(n) || 0).toLocaleString("pt-BR", {
    style: "currency",
    currency: "BRL",
  });

function toNumberFlexible(input) {
  if (typeof input === "number") return input;
  let s = String(input || "").trim();

  s = s.replace(/[^\d.,-]/g, "");
  if (!s) return 0;

  const hasComma = s.includes(",");
  const hasDot = s.includes(".");

  if (hasComma && hasDot) {
    const lastSepIdx = Math.max(s.lastIndexOf(","), s.lastIndexOf("."));
    const intPart = s.slice(0, lastSepIdx).replace(/[.,]/g, "");
    const fracPart = s.slice(lastSepIdx + 1);
    s = `${intPart}.${fracPart}`;
  } else if (hasComma && !hasDot) {
    s = s.replace(/\./g, "");
    s = s.replace(",", ".");
  } else {
    s = s.replace(/,/g, "");
  }

  const n = Number(s);
  return isNaN(n) ? 0 : n;
}

const cepDigits = computed(() => cep.value.replace(/\D/g, ""));
const cepInvalid = computed(
  () => cepDigits.value.length > 0 && cepDigits.value.length !== 8
);

function maskCep() {
  const digits = cep.value.replace(/\D/g, "").slice(0, 8);
  if (digits.length <= 5) {
    cep.value = digits;
  } else {
    cep.value = `${digits.slice(0, 5)}-${digits.slice(5)}`;
  }
}

onMounted(() => {
  if (cartStore.cep) {
    cep.value = cartStore.cep;
  }
  if (cartStore.shippingOptions.length > 0) {
    freteResp.value = cartStore.shippingOptions;
  }
});

async function onCalcularFrete() {
  freteError.value = "";
  cartStore.setShippingSelected(null);

  const digits = cepDigits.value;
  if (digits.length !== 8) {
    freteError.value = "CEP inválido. Use 8 dígitos (ex: 01001000).";
    return;
  }

  cartStore.setCep(cep.value);

  produto.to_postal_code = digits;

  try {
    isCalculating.value = true;
    const resp = await calcularFrete(produto);
    freteResp.value = Array.isArray(resp) ? resp : [];

    cartStore.setShippingOptions(freteResp.value);
  } catch (err) {
    console.error("Erro ao calcular frete:", err);
    freteError.value = "Não foi possível calcular o frete. Tente novamente.";
    freteResp.value = [];
    cartStore.setShippingOptions([]);
  } finally {
    isCalculating.value = false;
  }
}

const shippingOptions = computed(() => {
  if (!Array.isArray(freteResp.value)) return [];
  return freteResp.value
    .filter((f) => f && (f.name === "SEDEX" || f.name === "PAC"))
    .map((f, idx) => {
      const priceNum = toNumberFlexible(f.price);

      const date = new Date();
      date.setDate(date.getDate() + Number(f.delivery_time || 0));
      const estimatedDate = date.toLocaleDateString("pt-BR", {
        day: "2-digit",
        month: "2-digit",
      });

      return {
        id: f.id ?? `${f.name}-${idx}`,
        name: f.name,
        price: priceNum,
        delivery_time: f.delivery_time,
        estimatedDate,
        error: !!f.error,
      };
    })
    .filter((f) => !f.error);
});

const shippingSelected = computed(() => cartStore.shippingSelected);
const shippingPrice = computed(() =>
  shippingSelected.value ? shippingSelected.value.price : 0
);

const GIFT_THRESHOLD = 200;
const progressPercent = computed(() => {
  const p = Math.min(
    100,
    Math.round((cartStore.subtotal / GIFT_THRESHOLD) * 100)
  );
  return isNaN(p) ? 0 : p;
});
const eligible = computed(() => cartStore.subtotal >= GIFT_THRESHOLD);
const remainingToGift = computed(() =>
  Math.max(0, GIFT_THRESHOLD - cartStore.subtotal)
);
const progressBarWidth = computed(() => `${progressPercent.value}%`);

const totalWithFreight = computed(() => {
  const total =
    Number(cartStore.subtotal || 0) + Number(shippingPrice.value || 0);
  return isNaN(total) ? 0 : total;
});

function onKey(e) {
  if (e.key === "Escape") cartStore.closeCart();
}

watch(
  () => cartStore.open,
  (v) => {
    document.body.style.overflow = v ? "hidden" : "";
  }
);

watch(cepDigits, (d) => {
  if (d.length !== 8) {
    cartStore.setShippingSelected(null);
  }
});

onMounted(() => window.addEventListener("keydown", onKey));
onBeforeUnmount(() => {
  window.removeEventListener("keydown", onKey);
  document.body.style.overflow = "";
});
</script>

<style scoped>
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.2s ease;
}
.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}

.slide-in-right-enter-active,
.slide-in-right-leave-active {
  transition: transform 0.25s ease;
}
.slide-in-right-enter-from,
.slide-in-right-leave-to {
  transform: translateX(100%);
}
</style>
