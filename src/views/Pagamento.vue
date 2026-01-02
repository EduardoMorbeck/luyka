<template>
  <div
    class="min-h-screen bg-gradient-to-br from-[#ede5dd] via-white to-[#b9a994] py-28 px-4"
  >
    <div class="max-w-7xl mx-auto">
      <div class="text-center mb-6 sm:mb-8 md:mb-12">
        <div
          class="inline-flex items-center gap-1 sm:gap-2 text-xs sm:text-sm text-[#423734] mb-2 sm:mb-3 flex-wrap justify-center"
        >
          <span
            @click="voltarParaCarrinho"
            class="hover:text-[#735e59] cursor-pointer transition-colors"
            >Carrinho</span
          >
          <svg
            class="w-4 h-4"
            fill="none"
            stroke="currentColor"
            viewBox="0 0 24 24"
          >
            <path
              stroke-linecap="round"
              stroke-linejoin="round"
              stroke-width="2"
              d="M9 5l7 7-7 7"
            ></path>
          </svg>
          <span
            @click="voltarParaEntrega"
            class="text-[#735e59] font-medium hover:text-[#b9a994] cursor-pointer transition-colors"
            >Entrega</span
          >
          <svg
            class="w-4 h-4"
            fill="none"
            stroke="currentColor"
            viewBox="0 0 24 24"
          >
            <path
              stroke-linecap="round"
              stroke-linejoin="round"
              stroke-width="2"
              d="M9 5l7 7-7 7"
            ></path>
          </svg>
          <span class="text-[#735e59] font-medium">Pagamento</span>
        </div>
        <h1
          class="text-2xl sm:text-3xl md:text-4xl font-bold bg-gradient-to-r from-[#735e59] to-[#b9a994] bg-clip-text text-transparent"
        >
          Finalizar Compra
        </h1>
        <p class="text-[#423734] mt-2 text-sm sm:text-base">
          Complete seu pedido de forma segura e rápida
        </p>
      </div>

      <div class="grid grid-cols-1 lg:grid-cols-3 gap-4 sm:gap-6 md:gap-8">
        <div class="lg:col-span-2 space-y-4 sm:space-y-6">
          <section
            class="bg-white rounded-xl sm:rounded-2xl shadow-lg border border-[#ede5dd] p-4 sm:p-6 md:p-8 hover:shadow-xl transition-all duration-300 cursor-pointer"
          >
            <header class="mb-4 sm:mb-6 flex items-center gap-2 sm:gap-3">
              <div
                class="w-8 h-8 sm:w-10 sm:h-10 bg-[#ede5dd] rounded-full flex items-center justify-center flex-shrink-0"
              >
                <svg
                  class="w-4 h-4 sm:w-5 sm:h-5 text-[#735e59]"
                  fill="none"
                  stroke="currentColor"
                  viewBox="0 0 24 24"
                >
                  <path
                    stroke-linecap="round"
                    stroke-linejoin="round"
                    stroke-width="2"
                    d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z"
                  ></path>
                  <path
                    stroke-linecap="round"
                    stroke-linejoin="round"
                    stroke-width="2"
                    d="M15 11a3 3 0 11-6 0 3 3 0 016 0z"
                  ></path>
                </svg>
              </div>
              <div>
                <h2 class="text-lg sm:text-xl font-bold text-[#232121]">
                  Dados para Entrega
                </h2>
                <p class="text-[#423734] text-sm sm:text-base">
                  Confira se está tudo correto antes de finalizar
                </p>
              </div>
            </header>

            <div
              class="grid grid-cols-1 sm:grid-cols-2 gap-3 sm:gap-4 md:gap-6"
            >
              <div class="space-y-1.5 sm:space-y-2">
                <span
                  class="text-xs sm:text-sm font-medium text-[#423734] uppercase tracking-wide"
                  >Nome</span
                >
                <div
                  class="text-base sm:text-lg font-semibold text-[#232121] bg-[#ede5dd] px-3 sm:px-4 py-2 sm:py-3 rounded-lg"
                >
                  {{ entrega.nome || "—" }}
                </div>
              </div>
              <div class="space-y-1.5 sm:space-y-2">
                <span
                  class="text-xs sm:text-sm font-medium text-[#423734] uppercase tracking-wide"
                  >Sobrenome</span
                >
                <div
                  class="text-base sm:text-lg font-semibold text-[#232121] bg-[#ede5dd] px-3 sm:px-4 py-2 sm:py-3 rounded-lg"
                >
                  {{ entrega.sobrenome || "—" }}
                </div>
              </div>
              <div class="space-y-1.5 sm:space-y-2">
                <span
                  class="text-xs sm:text-sm font-medium text-[#423734] uppercase tracking-wide"
                  >Telefone</span
                >
                <div
                  class="text-base sm:text-lg font-semibold text-[#232121] bg-[#ede5dd] px-3 sm:px-4 py-2 sm:py-3 rounded-lg"
                >
                  {{ entrega.telefone || "—" }}
                </div>
              </div>
              <div class="space-y-1.5 sm:space-y-2">
                <span
                  class="text-xs sm:text-sm font-medium text-[#423734] uppercase tracking-wide"
                  >CPF/CNPJ</span
                >
                <div
                  class="text-base sm:text-lg font-semibold text-[#232121] bg-[#ede5dd] px-3 sm:px-4 py-2 sm:py-3 rounded-lg"
                >
                  {{ entrega.cpfCnpj || "—" }}
                </div>
              </div>
              <div class="sm:col-span-2 space-y-1.5 sm:space-y-2">
                <span
                  class="text-xs sm:text-sm font-medium text-[#423734] uppercase tracking-wide"
                  >Endereço Completo</span
                >
                <div
                  class="text-base sm:text-lg font-semibold text-[#232121] bg-[#ede5dd] px-3 sm:px-4 py-2 sm:py-3 rounded-lg leading-relaxed"
                >
                  {{ entrega.rua || "" }} {{ entrega.numero || "" }}
                  <span v-if="entrega.complemento" class="text-[#423734]"
                    >, {{ entrega.complemento }}</span
                  >
                  <br />
                  <span class="text-[#735e59]">{{ entrega.bairro || "" }}</span>
                  -
                  <span class="text-[#b9a994]">{{ entrega.cidade || "" }}</span
                  >/
                  <span class="text-[#735e59]">{{ entrega.estado || "" }}</span>
                  <br />
                  <span class="text-[#423734]"
                    >CEP {{ entrega.cep || "" }}</span
                  >
                </div>
              </div>
              <div
                v-if="shipping > 0"
                class="sm:col-span-2 space-y-1.5 sm:space-y-2"
              >
                <span
                  class="text-xs sm:text-sm font-medium text-[#423734] uppercase tracking-wide"
                  >Forma de Envio</span
                >
                <div
                  class="bg-gradient-to-r from-[#ede5dd] to-[#b9a994] border border-[#b9a994] px-3 sm:px-4 py-2 sm:py-3 rounded-lg"
                >
                  <div class="flex items-center justify-between gap-2">
                    <span
                      class="font-semibold text-[#735e59] text-sm sm:text-base"
                      >{{ shippingMethod?.name || "—" }}</span
                    >
                    <span
                      class="text-base sm:text-lg font-bold text-[#735e59] whitespace-nowrap"
                      >{{ formatBRL(shipping) }}</span
                    >
                  </div>
                  <span
                    v-if="shippingMethod?.estimatedDate"
                    class="text-xs sm:text-sm text-[#735e59] block mt-1"
                  >
                    🚚 Entrega até dia {{ shippingMethod.estimatedDate }}
                  </span>
                </div>
              </div>
              <div
                class="sm:col-span-2 space-y-1.5 sm:space-y-2"
                v-if="entrega.obs"
              >
                <span
                  class="text-xs sm:text-sm font-medium text-[#423734] uppercase tracking-wide"
                  >Observações</span
                >
                <div
                  class="text-base sm:text-lg font-semibold text-[#232121] bg-[#ede5dd] border border-[#b9a994] px-3 sm:px-4 py-2 sm:py-3 rounded-lg"
                >
                  {{ entrega.obs }}
                </div>
              </div>
            </div>
          </section>

          <section
            class="bg-white rounded-xl sm:rounded-2xl shadow-lg border border-[#ede5dd] p-4 sm:p-6 md:p-8 hover:shadow-xl transition-all duration-300 cursor-pointer"
          >
            <header class="mb-4 sm:mb-6 flex items-center gap-2 sm:gap-3">
              <div
                class="w-8 h-8 sm:w-10 sm:h-10 bg-[#ede5dd] rounded-full flex items-center justify-center flex-shrink-0"
              >
                <svg
                  class="w-4 h-4 sm:w-5 sm:h-5 text-[#735e59]"
                  fill="none"
                  stroke="currentColor"
                  viewBox="0 0 24 24"
                >
                  <path
                    stroke-linecap="round"
                    stroke-linejoin="round"
                    stroke-width="2"
                    d="M3 10h18M7 15h1m4 0h1m-7 4h12a3 3 0 003-3V8a3 3 0 00-3-3H6a3 3 0 00-3 3v8a3 3 0 003 3z"
                  ></path>
                </svg>
              </div>
              <div>
                <h2 class="text-lg sm:text-xl font-bold text-[#232121]">
                  Forma de Pagamento
                </h2>
                <p class="text-[#423734] text-sm sm:text-base">
                  Pagamento seguro via Pix
                </p>
              </div>
            </header>

            <div class="space-y-4 sm:space-y-6">
              <div
                class="bg-gradient-to-r from-[#ede5dd] to-[#b9a994] border-2 border-[#b9a994] rounded-lg sm:rounded-xl p-4 sm:p-6"
              >
                <div class="flex items-start gap-3 sm:gap-4">
                  <div
                    class="w-10 h-10 sm:w-12 sm:h-12 bg-[#735e59] rounded-full flex items-center justify-center flex-shrink-0"
                  >
                    <svg
                      class="w-5 h-5 sm:w-6 sm:h-6 text-white"
                      fill="none"
                      stroke="currentColor"
                      viewBox="0 0 24 24"
                    >
                      <path
                        stroke-linecap="round"
                        stroke-linejoin="round"
                        stroke-width="2"
                        d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"
                      ></path>
                    </svg>
                  </div>
                  <div class="flex-1 min-w-0">
                    <div
                      class="flex items-center gap-2 mb-1.5 sm:mb-2 flex-wrap"
                    >
                      <h3 class="text-base sm:text-lg font-bold text-[#735e59]">
                        Pix
                      </h3>
                      <span
                        class="px-2 py-0.5 sm:py-1 bg-[#ede5dd] text-[#735e59] text-xs font-medium rounded-full"
                        >Recomendado</span
                      >
                    </div>
                    <p class="text-[#735e59] text-sm sm:text-base">
                      O código Pix será gerado automaticamente ao finalizar o
                      pedido.
                    </p>
                  </div>
                </div>
              </div>

              <div
                v-if="pixData"
                class="bg-gradient-to-br from-[#ede5dd] via-[#b9a994] to-[#ede5dd] border-2 border-[#b9a994] rounded-xl sm:rounded-2xl p-4 sm:p-6 md:p-8 animate-fade-in"
              >
                <div class="text-center mb-4 sm:mb-6">
                  <div
                    class="w-12 h-12 sm:w-16 sm:h-16 bg-[#735e59] rounded-full flex items-center justify-center mx-auto mb-3 sm:mb-4"
                  >
                    <svg
                      class="w-6 h-6 sm:w-8 sm:h-8 text-white"
                      fill="none"
                      stroke="currentColor"
                      viewBox="0 0 24 24"
                    >
                      <path
                        stroke-linecap="round"
                        stroke-linejoin="round"
                        stroke-width="2"
                        d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"
                      ></path>
                    </svg>
                  </div>
                  <h3
                    class="text-xl sm:text-2xl font-bold text-[#735e59] mb-1.5 sm:mb-2"
                  >
                    Código Pix Gerado com Sucesso!
                  </h3>
                  <p class="text-[#735e59] text-base sm:text-lg">
                    Escaneie ou copie o código para pagar
                  </p>
                </div>

                <div
                  class="bg-white rounded-lg sm:rounded-xl p-4 sm:p-6 mb-4 sm:mb-6 shadow-sm"
                >
                  <div
                    class="grid grid-cols-1 sm:grid-cols-3 gap-3 sm:gap-4 text-xs sm:text-sm"
                  >
                    <div
                      class="text-center p-2.5 sm:p-3 bg-[#ede5dd] rounded-lg"
                    >
                      <span
                        class="block text-[#423734] text-xs uppercase font-medium mb-1"
                        >Nome</span
                      >
                      <span
                        class="font-semibold text-[#232121] text-xs sm:text-sm break-words"
                        >{{ pixData.nome }}</span
                      >
                    </div>
                    <div
                      class="text-center p-2.5 sm:p-3 bg-[#ede5dd] rounded-lg"
                    >
                      <span
                        class="block text-[#423734] text-xs uppercase font-medium mb-1"
                        >CNPJ</span
                      >
                      <span
                        class="font-semibold text-[#232121] text-xs sm:text-sm break-words"
                        >{{ pixData.cnpj }}</span
                      >
                    </div>
                    <div
                      class="text-center p-2.5 sm:p-3 bg-[#ede5dd] rounded-lg"
                    >
                      <span
                        class="block text-[#735e59] text-xs uppercase font-medium mb-1"
                        >Valor</span
                      >
                      <span
                        class="font-bold text-[#735e59] text-base sm:text-lg"
                        >{{ formatBRL(pixData.valor) }}</span
                      >
                    </div>
                  </div>
                </div>

                <div class="space-y-4 sm:space-y-6">
                  <div class="text-center">
                    <label
                      class="block text-xs sm:text-sm font-semibold text-[#232121] mb-2 sm:mb-3"
                    >
                      📱 QR Code Pix
                    </label>
                    <div
                      class="inline-block p-4 sm:p-6 bg-white rounded-xl sm:rounded-2xl shadow-lg border-2 border-[#b9a994]"
                    >
                      <img
                        v-if="pixData?.qr_code"
                        :src="pixData.qr_code"
                        :alt="'QR Code Pix para ' + formatBRL(pixData.valor)"
                        class="w-48 h-48 sm:w-56 sm:h-56 mx-auto"
                      />
                    </div>
                    <p class="text-xs sm:text-sm text-[#423734] mt-2 sm:mt-3">
                      Escaneie com o app do seu banco
                    </p>
                  </div>

                  <div>
                    <label
                      class="block text-xs sm:text-sm font-semibold text-[#232121] mb-2 sm:mb-3"
                    >
                      🔑 Código Pix
                    </label>
                    <div class="flex flex-col sm:flex-row gap-2 sm:gap-3">
                      <input
                        type="text"
                        :value="pixCode"
                        readonly
                        class="flex-1 px-3 sm:px-4 py-2.5 sm:py-3 border-2 border-[#ede5dd] rounded-lg sm:rounded-xl bg-[#ede5dd] text-xs sm:text-sm font-mono focus:border-[#735e59] focus:ring-2 focus:ring-[#ede5dd] transition-all"
                      />
                      <button
                        type="button"
                        @click="copiarCodigoPix"
                        class="px-4 sm:px-6 py-2.5 sm:py-3 bg-gradient-to-r from-[#735e59] to-[#b9a994] text-white font-semibold rounded-lg sm:rounded-xl hover:from-[#b9a994] hover:to-[#735e59] focus:outline-none focus:ring-4 focus:ring-[#ede5dd] transition-all duration-200 transform hover:scale-105 cursor-pointer text-sm sm:text-base"
                      >
                        <svg
                          class="w-4 h-4 inline sm:mr-2"
                          fill="none"
                          stroke="currentColor"
                          viewBox="0 0 24 24"
                        >
                          <path
                            stroke-linecap="round"
                            stroke-linejoin="round"
                            stroke-width="2"
                            d="M8 16H6a2 2 0 01-2-2V6a2 2 0 012-2h8a2 2 0 012 2v2m-6 12h8a2 2 0 002-2v-8a2 2 0 00-2-2h-8a2 2 0 00-2 2v8a2 2 0 002 2z"
                          ></path>
                        </svg>
                        <span class="hidden sm:inline">Copiar</span>
                        <span class="sm:hidden">Copiar Código</span>
                      </button>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </section>

          <section
            class="bg-white rounded-xl sm:rounded-2xl shadow-lg border border-[#ede5dd] p-4 sm:p-6 md:p-8 hover:shadow-xl transition-all duration-300 cursor-pointer"
          >
            <div
              class="flex flex-col lg:flex-row items-center justify-between gap-4 sm:gap-6"
            >
              <div class="text-center lg:text-left">
                <div
                  class="flex items-center gap-2 mb-1.5 sm:mb-2 justify-center lg:justify-start"
                >
                  <svg
                    class="w-4 h-4 sm:w-5 sm:h-5 text-[#735e59]"
                    fill="none"
                    stroke="currentColor"
                    viewBox="0 0 24 24"
                  >
                    <path
                      stroke-linecap="round"
                      stroke-linejoin="round"
                      stroke-width="2"
                      d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z"
                    ></path>
                  </svg>
                  <span class="text-xs sm:text-sm font-medium text-[#735e59]"
                    >Pagamento 100% Seguro</span
                  >
                </div>
                <p class="text-[#423734] text-xs sm:text-sm">
                  Seus dados são protegidos e criptografados
                </p>
              </div>
              <button
                class="w-full lg:w-auto px-6 sm:px-12 py-3 sm:py-4 text-base sm:text-lg md:text-xl bg-gradient-to-r from-[#735e59] to-[#b9a994] text-white font-bold rounded-xl sm:rounded-2xl shadow-lg hover:from-[#b9a994] hover:to-[#735e59] focus:outline-none focus:ring-4 focus:ring-[#ede5dd] disabled:opacity-50 disabled:cursor-not-allowed disabled:transform-none transform hover:scale-105 transition-all duration-200 cursor-pointer"
                :disabled="isDisabled || isLoading"
                @click="finalizarPedido"
              >
                <div v-if="isLoading" class="flex items-center gap-2">
                  <svg
                    class="animate-spin w-5 h-5"
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
                  Processando...
                </div>
                <div v-else class="flex items-center gap-2">
                  <svg
                    class="w-5 h-5"
                    fill="none"
                    stroke="currentColor"
                    viewBox="0 0 24 24"
                  >
                    <path
                      stroke-linecap="round"
                      stroke-linejoin="round"
                      stroke-width="2"
                      d="M5 13l4 4L19 7"
                    ></path>
                  </svg>
                  Finalizar Pedido
                </div>
              </button>
            </div>
          </section>
        </div>

        <aside class="space-y-4 sm:space-y-6">
          <section
            class="bg-white rounded-xl sm:rounded-2xl shadow-lg border border-[#ede5dd] p-4 sm:p-6 hover:shadow-xl transition-all duration-300"
          >
            <header class="mb-4 sm:mb-6 flex items-center gap-2 sm:gap-3">
              <div
                class="w-8 h-8 sm:w-10 sm:h-10 bg-[#ede5dd] rounded-full flex items-center justify-center flex-shrink-0"
              >
                <svg
                  class="w-4 h-4 sm:w-5 sm:h-5 text-[#735e59]"
                  fill="none"
                  stroke="currentColor"
                  viewBox="0 0 24 24"
                >
                  <path
                    stroke-linecap="round"
                    stroke-linejoin="round"
                    stroke-width="2"
                    d="M9 5H7a2 2 0 00-2 2v10a2 2 0 002 2h8a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2"
                  ></path>
                </svg>
              </div>
              <div>
                <h2 class="text-lg sm:text-xl font-bold text-[#232121]">
                  Resumo do Pedido
                </h2>
                <p class="text-[#423734] text-sm sm:text-base">
                  {{ cartStore.items?.length || 0 }} item(s)
                </p>
              </div>
            </header>

            <div class="space-y-3 sm:space-y-4 mb-4 sm:mb-6">
              <div
                v-for="item in cartStore.items"
                :key="item.key"
                class="flex items-center gap-2 sm:gap-4 p-2.5 sm:p-3 bg-[#ede5dd] rounded-lg sm:rounded-xl hover:bg-[#b9a994] transition-colors cursor-pointer"
              >
                <img
                  v-if="item.img"
                  :src="item.img"
                  :alt="item.title"
                  class="w-12 h-12 sm:w-16 sm:h-16 rounded-lg object-cover border border-[#b9a994] flex-shrink-0"
                />
                <div class="flex-1 min-w-0">
                  <h3
                    class="font-semibold text-[#232121] truncate text-sm sm:text-base"
                  >
                    {{ item.title }}
                  </h3>
                  <div class="flex items-center justify-between mt-1 gap-2">
                    <span class="text-xs sm:text-sm text-[#423734]"
                      >{{ formatBRL(Number(item.price)) }} ×
                      {{ item.qty }}</span
                    >
                    <span
                      class="font-bold text-[#232121] text-sm sm:text-base"
                      >{{
                        formatBRL(Number(item.price) * Number(item.qty))
                      }}</span
                    >
                  </div>
                </div>
              </div>
            </div>

            <div
              class="space-y-2 sm:space-y-3 text-xs sm:text-sm border-t border-[#ede5dd] pt-3 sm:pt-4"
            >
              <div class="flex justify-between items-center">
                <span class="text-[#423734]">Subtotal</span>
                <span class="font-medium text-[#232121]">{{
                  formatBRL(itemsTotal)
                }}</span>
              </div>
              <div
                v-if="shipping > 0"
                class="flex justify-between items-center"
              >
                <span class="text-[#423734]">Frete</span>
                <span class="font-medium text-[#232121]">{{
                  formatBRL(shipping)
                }}</span>
              </div>
              <div
                v-if="discount > 0"
                class="flex justify-between items-center"
              >
                <span class="text-[#735e59]">Desconto</span>
                <span class="font-medium text-[#735e59]"
                  >-{{ formatBRL(discount) }}</span
                >
              </div>
              <div
                class="pt-2 sm:pt-3 border-t border-[#ede5dd] flex justify-between items-center text-base sm:text-lg font-bold"
              >
                <span class="text-[#232121]">Total</span>
                <span
                  class="text-xl sm:text-2xl bg-gradient-to-r from-[#735e59] to-[#b9a994] bg-clip-text text-transparent"
                >
                  {{ formatBRL(grandTotal) }}
                </span>
              </div>

              <div
                v-if="itemsTotal >= GIFT_THRESHOLD"
                class="mt-3 sm:mt-4 p-3 sm:p-4 bg-gradient-to-r from-[#ede5dd] to-[#b9a994] border border-[#b9a994] rounded-lg sm:rounded-xl text-center"
              >
                <div class="text-xl sm:text-2xl mb-1.5 sm:mb-2">🎁</div>
                <p class="text-xs sm:text-sm font-semibold text-[#735e59]">
                  Parabéns! Você ganhará um presente especial nesta compra!
                </p>
              </div>
            </div>
          </section>

          <section
            class="bg-gradient-to-br from-[#ede5dd] to-[#b9a994] border border-[#b9a994] rounded-xl sm:rounded-2xl p-4 sm:p-6"
          >
            <h3
              class="font-bold text-[#735e59] mb-3 sm:mb-4 flex items-center gap-2 text-base sm:text-lg"
            >
              <svg
                class="w-4 h-4 sm:w-5 sm:h-5"
                fill="none"
                stroke="currentColor"
                viewBox="0 0 24 24"
              >
                <path
                  stroke-linecap="round"
                  stroke-linejoin="round"
                  stroke-width="2"
                  d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z"
                ></path>
              </svg>
              Garantias da Loja
            </h3>
            <ul
              class="space-y-2 sm:space-y-3 text-xs sm:text-sm text-[#735e59]"
            >
              <li class="flex items-start gap-2">
                <span class="text-[#735e59] mt-0.5">✅</span>
                <span>7 dias para trocas/devoluções</span>
              </li>
              <li class="flex items-start gap-2">
                <span class="text-[#735e59] mt-0.5">🔒</span>
                <span>Ambiente 100% seguro e criptografado</span>
              </li>
              <li class="flex items-start gap-2">
                <span class="text-[#735e59] mt-0.5">💬</span>
                <span>Suporte humano para qualquer dúvida</span>
              </li>
              <li class="flex items-start gap-2">
                <span class="text-[#735e59] mt-0.5">🚚</span>
                <span>Entrega rápida e rastreada</span>
              </li>
            </ul>
          </section>
        </aside>
      </div>
    </div>
  </div>
</template>

<script setup>
import { reactive, ref, onMounted, computed } from "vue";
import { useRouter } from "vue-router";
import { cartStore } from "../store/cartStore";

const router = useRouter();

const GIFT_THRESHOLD = 299;

const entrega = reactive({});
const pixCode = ref("");
const isLoading = ref(false);
const pixData = ref(null);

onMounted(() => {
  const salvo = localStorage.getItem("formEntrega");
  if (salvo) Object.assign(entrega, JSON.parse(salvo));
});

const formatBRL = (v) =>
  new Intl.NumberFormat("pt-BR", { style: "currency", currency: "BRL" }).format(
    Number.isFinite(v) ? v : 0
  );

const itemsTotal = computed(() => cartStore.subtotal || 0);

const shipping = computed(() => {
  return cartStore.shippingSelected?.price || 0;
});

const shippingMethod = computed(() => cartStore.shippingSelected);

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
  const hasValidCity = entrega?.cidade && entrega.cidade.trim().length > 0;
  return !(hasItems && hasAddress && hasValidCity);
});

const voltarParaCarrinho = () => {
  cartStore.openCart();
  router.push("/");
};

const voltarParaEntrega = () => {
  router.push("/entrega");
};

const copiarCodigoPix = async () => {
  if (!pixCode.value) return;
  try {
    await navigator.clipboard.writeText(pixCode.value);
    alert("Código Pix copiado para a área de transferência!");
  } catch (error) {
    console.error("Erro ao copiar código:", error);
    alert("Erro ao copiar código. Tente novamente.");
  }
};

const finalizarPedido = async () => {
  try {
    isLoading.value = true;

    await new Promise((resolve) => setTimeout(resolve, 1500));
    const cnpjFake = "12.345.678/0001-90";
    const pixCodeFake = `00020126580014BR.GOV.BCB.PIX0136${Math.random()
      .toString(36)
      .substring(2, 15)
      .toUpperCase()}5204000053039865802BR5913LUYKA LOJA LTDA6009SAO PAULO62070503***6304${Math.random()
      .toString(36)
      .substring(2, 6)
      .toUpperCase()}`;

    const qrCodeUrl = `https://api.qrserver.com/v1/create-qr-code/?size=224x224&data=${encodeURIComponent(
      pixCodeFake
    )}`;

    const response = {
      success: true,
      pix_code: pixCodeFake,
      cnpj: cnpjFake,
      nome: "LUYKA LOJA LTDA",
      valor: grandTotal.value,
      qr_code: qrCodeUrl,
    };

    pixCode.value = response.pix_code;
    pixData.value = response;

    console.log("Pedido finalizado com sucesso! (Dados demonstrativos)", {
      entrega,
      items: cartStore.items,
      total: grandTotal.value,
      pixCode: response.pix_code,
      cnpj: response.cnpj,
    });

    cartStore.clear();
  } catch (error) {
    console.error("Erro ao finalizar pedido:", error);
    alert("Erro ao finalizar pedido. Tente novamente.");
  } finally {
    isLoading.value = false;
  }
};
</script>

<style scoped></style>
