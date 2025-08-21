<template>
  <div class="flex flex-col relative">
    <button
      class="cursor-pointer"
      @click="cartStore.openCart()"
      aria-label="Abrir carrinho"
    >
      <i class="fa-solid fa-cart-shopping text-dark text-2xl"></i>
    </button>

    <span class="text-xs"
      >R$ {{ cartStore.subtotal.toFixed(2).replace(".", ",") }}</span
    >

    <div
      v-if="cartStore.items.length > 0"
      class="absolute bottom-8 left-9 flex bg-white rounded-full px-1.5 py-0.5 text-xs"
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
        class="fixed inset-y-0 p-4 right-0 z-[70] w-full max-w-md bg-white shadow-2xl flex flex-col"
        role="dialog"
        aria-modal="true"
      >
        <header class="flex items-center justify-end">
          <button
            class="p-2"
            @click="cartStore.closeCart()"
            aria-label="Fechar"
          >
            <div
              class="flex items-center justify-center cursor-pointer py-2.5 px-3 rounded-full bg-gray-100 hover:bg-gray-200"
            >
              <i class="fa-solid fa-xmark text-xl"></i>
            </div>
          </button>
        </header>

        <div
          class="flex items-center justify-between border-b border-dark pt-8"
        >
          <div class="w-1/2">PRODUTOS</div>
          <div class="w-1/2 flex justify-end">SUBTOTAL</div>
        </div>

        <div class="overflow-y-auto grow pt-8">
          <template v-if="cartStore.items.length > 0">
            <div
              v-for="item in cartStore.items"
              :key="item.key"
              class="flex gap-4 mb-4 border-b pb-4"
            >
              <img
                v-if="item.img"
                :src="item.img"
                :alt="item.title"
                class="w-16 h-16 object-cover rounded"
              />

              <div class="flex-1">
                <div class="flex items-start justify-between gap-2">
                  <h3 class="font-medium leading-snug">{{ item.title }}</h3>
                </div>

                <div class="mt-2 flex gap-3">
                  <div
                    class="inline-flex items-center border border-dark rounded-full"
                  >
                    <button
                      class="flex items-center justify-center cursor-pointer py-2.5 px-3 rounded-full hover:bg-gray-200"
                      @click.stop="cartStore.decrement(item.key)"
                      aria-label="Diminuir quantidade"
                      title="Diminuir"
                    >
                      <i class="fa-solid fa-minus"></i>
                    </button>
                    <span class="px-3 select-none min-w-6 text-center">{{
                      item.qty
                    }}</span>
                    <button
                      class="flex items-center justify-center cursor-pointer py-2.5 px-3 rounded-full hover:bg-gray-200"
                      @click.stop="cartStore.increment(item.key)"
                      aria-label="Aumentar quantidade"
                      title="Aumentar"
                    >
                      <i class="fa-solid fa-plus"></i>
                    </button>
                  </div>
                </div>
              </div>

              <div class="flex items-start gap-2">
                <div class="text-right font-medium py-1">
                  R$
                  {{
                    (Number(item.price) * Number(item.qty))
                      .toFixed(2)
                      .replace(".", ",")
                  }}
                </div>

                <button
                  class="px-2 py-1 rounded-full hover:bg-gray-100 cursor-pointer"
                  @click.stop="cartStore.removeItem(item.key)"
                  aria-label="Remover produto"
                  title="Remover"
                >
                  <i class="fa-solid fa-trash"></i>
                </button>
              </div>
            </div>

            <div class="flex justify-between text-xl pt-4 font-bold">
              <span>Total</span>
              <span
                >R$ {{ cartStore.subtotal.toFixed(2).replace(".", ",") }}</span
              >
            </div>
          </template>

          <p v-else class="text-sm text-gray-500">
            O carrinho de compras está vazio.
          </p>
        </div>

        <div v-if="cartStore.items.length > 0" class="flex justify-center">
          <a
            href="/entrega"
            class="w-full text-center px-10 py-4 text-xl bg-btn text-dark font-medium rounded-full border-2 border-dark cursor-pointer"
          >
            Iniciar compra
          </a>
        </div>

        <div class="flex justify-center">
          <div
            @click="cartStore.closeCart()"
            class="px-10 py-4 mt-4 text-xl text-dark cursor-pointer hover:underline"
          >
            Ver mais produtos
          </div>
        </div>
      </section>
    </Transition>
  </Teleport>
</template>

<script setup>
import { watch, onMounted, onBeforeUnmount } from "vue";
import { cartStore } from "../store/cartStore";

function onKey(e) {
  if (e.key === "Escape") cartStore.closeCart();
}

watch(
  () => cartStore.open,
  (v) => {
    document.body.style.overflow = v ? "hidden" : "";
  }
);

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
