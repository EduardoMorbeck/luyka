<template>
  <div class="w-full flex flex-col justify-center items-center py-28 gap-10">
    <h1 class="font-bold text-3xl mb-8">Pagamento</h1>

    <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
      <div class="md:col-span-2 space-y-6">
        <section class="bg-white rounded-xl shadow-sm border p-5">
          <header class="mb-4">
            <h2 class="text-lg font-semibold">Dados para entrega</h2>
            <p class="text-sm text-gray-500">
              Confira se está tudo correto antes de finalizar.
            </p>
          </header>

          <div class="grid grid-cols-1 sm:grid-cols-2 gap-3 text-sm">
            <div>
              <span class="text-gray-500">Nome</span>
              <div class="font-medium">{{ entrega.nome || "—" }}</div>
            </div>
            <div>
              <span class="text-gray-500">Sobrenome</span>
              <div class="font-medium">{{ entrega.sobrenome || "—" }}</div>
            </div>
            <div>
              <span class="text-gray-500">Telefone</span>
              <div class="font-medium">{{ entrega.telefone || "—" }}</div>
            </div>
            <div>
              <span class="text-gray-500">CPF/CNPJ</span>
              <div class="font-medium">{{ entrega.cpfCnpj || "—" }}</div>
            </div>
            <div class="sm:col-span-2">
              <span class="text-gray-500">Endereço</span>
              <div class="font-medium">
                {{ entrega.rua || "" }} {{ entrega.numero || ""
                }}<span v-if="entrega.complemento"
                  >, {{ entrega.complemento }}</span
                ><br />
                {{ entrega.bairro || "" }} - {{ entrega.cidade || "" }}/{{
                  entrega.estado || ""
                }}
                • CEP {{ entrega.cep || "" }}
              </div>
            </div>
            <div class="sm:col-span-2" v-if="entrega.obs">
              <span class="text-gray-500">Observações</span>
              <div class="font-medium">{{ entrega.obs }}</div>
            </div>
          </div>
        </section>

        <section class="bg-white rounded-xl shadow-sm border p-5">
          <header class="mb-4">
            <h2 class="text-lg font-semibold">Forma de pagamento</h2>
          </header>

          <div class="space-y-4">
            <div class="flex items-start gap-3">
              <div class="mt-1 h-2.5 w-2.5 rounded-full bg-green-500"></div>
              <div>
                <div class="font-medium">Pix</div>
                <p class="text-sm text-gray-500">
                  Gere o código Pix do pedido para pagar escaneando o QR Code ou
                  usando “Copiar e Colar”.
                </p>
              </div>
            </div>

            <div class="rounded-lg border p-4">
              <div class="grid grid-cols-1 sm:grid-cols-3 gap-4">
                <div class="sm:col-span-2 space-y-2 text-sm">
                  <div class="flex justify-between">
                    <span class="text-gray-500">Nome</span>
                    <span class="font-medium">{{ entrega.nome || "—" }}</span>
                  </div>
                  <div class="flex justify-between">
                    <span class="text-gray-500">Sobrenome</span>
                    <span class="font-medium">{{
                      entrega.sobrenome || "—"
                    }}</span>
                  </div>
                  <div class="flex justify-between">
                    <span class="text-gray-500">CPF/CNPJ</span>
                    <span class="font-medium">{{
                      entrega.cpfCnpj || "—"
                    }}</span>
                  </div>
                </div>

                <div class="flex items-center justify-center">
                  <div
                    class="aspect-square w-32 border rounded-lg grid place-items-center text-xs text-gray-500"
                  >
                    QR Code
                  </div>
                </div>
              </div>

              <div class="mt-4 flex flex-wrap gap-3">
                <button
                  type="button"
                  class="text-center px-6 py-2 bg-btn text-dark font-medium rounded border-2 border-dark cursor-pointer mt-8"
                  @click="gerarPix"
                >
                  Gerar QR Pix
                </button>
                <button
                  type="button"
                  class="text-center px-6 py-2 bg-btn text-dark font-medium rounded border-2 border-dark cursor-pointer mt-8"
                  @click="copiarCodigoPix"
                >
                  Copiar código Pix
                </button>
              </div>

              <p
                v-if="pixCode"
                class="mt-3 text-xs break-all bg-gray-50 border rounded p-2"
              >
                {{ pixCode }}
              </p>
            </div>
          </div>
        </section>

        <section class="bg-white rounded-xl shadow-sm border p-5">
          <div class="flex items-start justify-between gap-4">
            <div class="text-sm text-gray-600">
              <div class="font-medium text-gray-900">Pagamento seguro</div>
              Seus dados são protegidos e criptografados.
            </div>
            <button
              class="text-center px-10 py-4 text-xl bg-btn text-dark font-medium rounded-full border-2 border-dark cursor-pointer mt-8"
              :disabled="isDisabled"
              @click="finalizarPedido"
            >
              Fazer pedido
            </button>
          </div>
        </section>
      </div>

      <aside class="space-y-6">
        <section class="bg-white rounded-xl shadow-sm border p-5">
          <header class="mb-4">
            <h2 class="text-lg font-semibold">Resumo do pedido</h2>
          </header>

          <ul class="divide-y">
            <li
              v-for="item in cartStore.items"
              :key="item.key"
              class="py-3 flex items-center gap-4"
            >
              <img
                v-if="item.img"
                :src="item.img"
                :alt="item.title"
                class="w-14 h-14 rounded object-cover"
              />
              <div class="flex-1">
                <div class="flex justify-between gap-3">
                  <p class="font-medium leading-tight">
                    {{ item.title }}
                  </p>
                  <span class="text-sm text-gray-500">× {{ item.qty }}</span>
                </div>
                <div class="text-sm text-gray-500">
                  {{ formatBRL(Number(item.price)) }} un.
                </div>
              </div>
              <div class="text-right font-medium">
                {{ formatBRL(Number(item.price) * Number(item.qty)) }}
              </div>
            </li>
          </ul>

          <dl class="mt-4 space-y-2 text-sm" aria-live="polite">
            <div class="flex justify-between">
              <dt class="text-gray-600">Subtotal</dt>
              <dd class="font-medium">{{ formatBRL(itemsTotal) }}</dd>
            </div>
            <div class="flex justify-between">
              <dt class="text-gray-600">Entrega</dt>
              <dd class="font-medium">{{ formatBRL(shipping) }}</dd>
            </div>
            <div v-if="discount > 0" class="flex justify-between">
              <dt class="text-gray-600">Desconto</dt>
              <dd class="font-medium text-green-600">
                -{{ formatBRL(discount) }}
              </dd>
            </div>
            <div
              class="pt-3 border-t flex justify-between text-base font-semibold"
            >
              <dt>Total</dt>
              <dd>{{ formatBRL(grandTotal) }}</dd>
            </div>
          </dl>
        </section>

        <section
          class="bg-white rounded-xl shadow-sm border p-5 text-sm text-gray-600"
        >
          <ul class="space-y-2">
            <li>✅ 7 dias para trocas/devoluções (conforme política).</li>
            <li>🔒 Ambiente seguro e criptografado.</li>
            <li>💬 Suporte humano para qualquer dúvida.</li>
          </ul>
        </section>
      </aside>
    </div>
  </div>
</template>

<script setup>
import { reactive, ref, onMounted, computed } from "vue";
import { cartStore } from "../store/cartStore";

const entrega = reactive({});
const pixCode = ref("");

onMounted(() => {
  const salvo = localStorage.getItem("formEntrega");
  if (salvo) Object.assign(entrega, JSON.parse(salvo));
});

const formatBRL = (v) =>
  new Intl.NumberFormat("pt-BR", { style: "currency", currency: "BRL" }).format(
    Number.isFinite(v) ? v : 0
  );

const itemsTotal = computed(() =>
  (cartStore.items || []).reduce(
    (acc, it) => acc + Number(it.price || 0) * Number(it.qty || 0),
    0
  )
);

const shipping = computed(() => 0);
const discount = computed(() => 0);
const grandTotal = computed(
  () => itemsTotal.value + shipping.value - discount.value
);

const isDisabled = computed(() => {
  const hasItems = (cartStore.items || []).length > 0;
  const hasAddress = Boolean(
    entrega?.nome &&
      entrega?.sobrenome &&
      entrega?.cep &&
      entrega?.rua &&
      entrega?.cidade &&
      entrega?.estado
  );
  return !(hasItems && hasAddress);
});

const gerarPix = () => {
  pixCode.value = `00020126420014BR.GOV.BCB.PIX0114+5551999999995204000053039865802BR5920${(
    entrega.nome || "CLIENTE"
  ).toUpperCase()}6009PORTO ALEG62070503***6304ABCD`;
};

const copiarCodigoPix = async () => {
  if (!pixCode.value) return;
  try {
    await navigator.clipboard.writeText(pixCode.value);
  } catch (e) {
    console.error(e);
  }
};

const finalizarPedido = () => {
  console.log("Finalizando pedido…", {
    entrega,
    items: cartStore.items,
    total: grandTotal.value,
  });
};
</script>

<style scoped></style>
