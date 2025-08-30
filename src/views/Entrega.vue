<template>
  <div
    class="min-h-screen bg-gradient-to-br from-[#ede5dd] via-white to-[#b9a994] py-28 px-4"
  >
    <div class="max-w-4xl mx-auto">
      <!-- Header com título e breadcrumb -->
      <div class="text-center mb-12">
        <div class="inline-flex items-center gap-2 text-sm text-[#423734] mb-3">
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
          <span class="text-[#735e59] font-medium">Entrega</span>
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
            @click="irParaPagamento"
            :class="[
              'transition-colors',
              todosObrigatoriosPreenchidos
                ? 'text-[#735e59] hover:text-[#b9a994] cursor-pointer font-medium'
                : 'text-[#b9a994] cursor-not-allowed opacity-60',
            ]"
          >
            Pagamento
          </span>
        </div>
        <h1
          class="text-4xl font-bold bg-gradient-to-r from-[#735e59] to-[#b9a994] bg-clip-text text-transparent"
        >
          Dados de Entrega
        </h1>
        <p class="text-[#423734] mt-2">
          Preencha suas informações para receber seu pedido
        </p>
      </div>

      <form @submit.prevent="submitForm" class="space-y-8">
        <!-- Seção de Endereço -->
        <section
          class="bg-white rounded-2xl shadow-lg border border-[#ede5dd] p-8 hover:shadow-xl transition-all duration-300"
        >
          <header class="mb-6 flex items-center gap-3">
            <div
              class="w-10 h-10 bg-[#ede5dd] rounded-full flex items-center justify-center"
            >
              <svg
                class="w-5 h-5 text-[#735e59]"
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
              <h2 class="text-xl font-bold text-[#232121]">
                Endereço de Entrega
              </h2>
              <p class="text-[#423734]">
                Informe onde deseja receber seu pedido
              </p>
            </div>
          </header>

          <div class="space-y-6">
            <!-- CEP e Busca -->
            <div class="space-y-3">
              <label
                class="block text-sm font-medium text-[#423734] uppercase tracking-wide"
              >
                CEP *
              </label>
              <div class="flex gap-3">
                <input
                  v-model="form.cep"
                  @input="onCepInput"
                  @keypress="searchCep"
                  placeholder="00000-000"
                  class="flex-1 px-4 py-3 border-2 border-[#ede5dd] rounded-xl bg-white text-[#232121] placeholder-[#b9a994] focus:border-[#735e59] focus:ring-2 focus:ring-[#ede5dd] transition-all"
                  :class="{
                    'border-red-500 focus:border-red-500 focus:ring-red-200':
                      cepErro,
                  }"
                  inputmode="numeric"
                  autocomplete="on"
                />
                <button
                  @click="searchCep"
                  type="button"
                  class="px-6 py-3 bg-gradient-to-r from-[#735e59] to-[#b9a994] text-white font-semibold rounded-xl hover:from-[#b9a994] hover:to-[#735e59] focus:outline-none focus:ring-4 focus:ring-[#ede5dd] transition-all duration-200 transform hover:scale-105"
                >
                  <svg
                    class="w-4 h-4 inline mr-2"
                    fill="none"
                    stroke="currentColor"
                    viewBox="0 0 24 24"
                  >
                    <path
                      stroke-linecap="round"
                      stroke-linejoin="round"
                      stroke-width="2"
                      d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"
                    ></path>
                  </svg>
                  Buscar
                </button>
              </div>
              <div class="text-sm">
                <span
                  v-if="cepLoading"
                  class="text-[#735e59] italic flex items-center gap-2"
                >
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
                  Buscando endereço...
                </span>
                <span
                  v-else-if="cepErro"
                  class="text-red-500 flex items-center gap-2"
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
                      d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"
                    ></path>
                  </svg>
                  {{ cepErro }}
                </span>
              </div>
            </div>

            <!-- Rua e Número -->
            <div class="grid grid-cols-1 sm:grid-cols-3 gap-4">
              <div class="sm:col-span-2">
                <label
                  class="block text-sm font-medium text-[#423734] uppercase tracking-wide mb-2"
                >
                  Rua *
                </label>
                <input
                  v-model="form.rua"
                  placeholder="Nome da rua"
                  class="w-full px-4 py-3 border-2 border-[#ede5dd] rounded-xl bg-white text-[#232121] placeholder-[#b9a994] focus:border-[#735e59] focus:ring-2 focus:ring-[#ede5dd] transition-all"
                  :class="{
                    'border-red-500 focus:border-red-500 focus:ring-red-200':
                      inputsErro && !form.rua,
                  }"
                />
              </div>
              <div>
                <label
                  class="block text-sm font-medium text-[#423734] uppercase tracking-wide mb-2"
                >
                  Número *
                </label>
                <input
                  v-model="form.numero"
                  placeholder="Nº"
                  class="w-full px-4 py-3 border-2 border-[#ede5dd] rounded-xl bg-white text-[#232121] placeholder-[#b9a994] focus:border-[#735e59] focus:ring-2 focus:ring-[#ede5dd] transition-all"
                  :class="{
                    'border-red-500 focus:border-red-500 focus:ring-red-200':
                      inputsErro && !form.numero,
                  }"
                />
              </div>
            </div>

            <!-- Complemento -->
            <div>
              <label
                class="block text-sm font-medium text-[#423734] uppercase tracking-wide mb-2"
              >
                Complemento
              </label>
              <input
                v-model="form.complemento"
                placeholder="Apartamento, bloco, etc. (opcional)"
                class="w-full px-4 py-3 border-2 border-[#ede5dd] rounded-xl bg-white text-[#232121] placeholder-[#b9a994] focus:border-[#735e59] focus:ring-2 focus:ring-[#ede5dd] transition-all"
              />
            </div>

            <!-- Bairro -->
            <div>
              <label
                class="block text-sm font-medium text-[#423734] uppercase tracking-wide mb-2"
              >
                Bairro *
              </label>
              <input
                v-model="form.bairro"
                placeholder="Nome do bairro"
                class="w-full px-4 py-3 border-2 border-[#ede5dd] rounded-xl bg-white text-[#232121] placeholder-[#b9a994] focus:border-[#735e59] focus:ring-2 focus:ring-[#ede5dd] transition-all"
                :class="{
                  'border-red-500 focus:border-red-500 focus:ring-red-200':
                    inputsErro && !form.bairro,
                }"
              />
            </div>

            <!-- Cidade e Estado -->
            <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
              <div>
                <label
                  class="block text-sm font-medium text-[#423734] uppercase tracking-wide mb-2"
                >
                  Cidade *
                </label>
                <input
                  v-model="form.cidade"
                  placeholder="Nome da cidade"
                  class="w-full px-4 py-3 border-2 border-[#ede5dd] rounded-xl bg-white text-[#232121] placeholder-[#b9a994] focus:border-[#735e59] focus:ring-2 focus:ring-[#ede5dd] transition-all"
                  :class="{
                    'border-red-500 focus:border-red-500 focus:ring-red-200':
                      inputsErro && !form.cidade,
                  }"
                />
              </div>
              <div>
                <label
                  class="block text-sm font-medium text-[#423734] uppercase tracking-wide mb-2"
                >
                  Estado *
                </label>
                <input
                  v-model="form.estado"
                  placeholder="UF"
                  class="w-full px-4 py-3 border-2 border-[#ede5dd] rounded-xl bg-white text-[#232121] placeholder-[#b9a994] focus:border-[#735e59] focus:ring-2 focus:ring-[#ede5dd] transition-all"
                  :class="{
                    'border-red-500 focus:border-red-500 focus:ring-red-200':
                      inputsErro && !form.estado,
                  }"
                />
              </div>
            </div>

            <!-- Observações -->
            <div>
              <label
                class="block text-sm font-medium text-[#423734] uppercase tracking-wide mb-2"
              >
                Observações
              </label>
              <textarea
                v-model="form.obs"
                placeholder="Instruções especiais para entrega (opcional)"
                rows="3"
                class="w-full px-4 py-3 border-2 border-[#ede5dd] rounded-xl bg-white text-[#232121] placeholder-[#b9a994] focus:border-[#735e59] focus:ring-2 focus:ring-[#ede5dd] transition-all resize-none"
              ></textarea>
            </div>
          </div>
        </section>

        <!-- Seção de Cálculo de Frete -->
        <section
          class="bg-white rounded-2xl shadow-lg border border-[#ede5dd] p-8 hover:shadow-xl transition-all duration-300"
        >
          <header class="mb-6 flex items-center gap-3">
            <div
              class="w-10 h-10 bg-[#ede5dd] rounded-full flex items-center justify-center"
            >
              <svg
                class="w-5 h-5 text-[#735e59]"
                fill="none"
                stroke="currentColor"
                viewBox="0 0 24 24"
              >
                <path
                  stroke-linecap="round"
                  stroke-linejoin="round"
                  stroke-width="2"
                  d="M20 7l-8-4-8 4m16 0l-8 4m8-4v10l-8 4m0-10L4 7m8 4v10M4 7v10l8 4"
                ></path>
              </svg>
            </div>
            <div>
              <h2 class="text-xl font-bold text-[#232121]">Cálculo de Frete</h2>
              <p class="text-[#423734]">
                Escolha a forma de envio para seu pedido
              </p>
            </div>
          </header>

          <div class="space-y-6">
            <p
              v-if="freteError"
              class="p-4 bg-red-50 border border-red-200 rounded-xl text-red-600 flex items-center gap-2"
              role="alert"
            >
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
                  d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"
                ></path>
              </svg>
              {{ freteError }}
            </p>

            <!-- Formas de Envio -->
            <fieldset v-if="shippingOptions.length" class="space-y-4">
              <legend class="text-lg font-semibold text-[#232121] mb-4">
                Formas de Envio Disponíveis
              </legend>

              <div
                class="space-y-3"
                role="radiogroup"
                aria-label="Formas de envio"
              >
                <label
                  v-for="opt in shippingOptions"
                  :key="opt.id"
                  class="flex items-start gap-4 p-4 rounded-xl bg-[#ede5dd] border-2 border-transparent hover:border-[#b9a994] cursor-pointer transition-all duration-200"
                  :class="{
                    'border-[#735e59] bg-[#b9a994] bg-opacity-20':
                      cartStore.shippingSelected?.id === opt.id,
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
                          d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z"
                        ></path>
                      </svg>
                      <span class="text-sm"
                        >Entrega até dia {{ opt.estimatedDate }}</span
                      >
                    </div>
                  </div>
                </label>
              </div>

              <p class="text-xs text-[#423734] italic">
                ⚠️ O prazo de entrega não contabiliza feriados.
              </p>
            </fieldset>

            <!-- Resumo de Valores -->
            <div
              v-if="cartStore.items.length > 0"
              class="bg-gradient-to-r from-[#ede5dd] to-[#b9a994] rounded-xl p-6"
              role="status"
              aria-live="polite"
            >
              <h3 class="font-bold text-[#735e59] mb-4 text-lg">
                Resumo do Pedido
              </h3>
              <div class="space-y-3 text-sm">
                <div class="flex items-center justify-between">
                  <span class="text-[#423734]">Subtotal (sem frete)</span>
                  <span class="font-semibold text-[#232121]">{{
                    formatBRL(cartStore.subtotal)
                  }}</span>
                </div>
                <div
                  class="flex items-center justify-between"
                  v-if="shippingPrice > 0"
                >
                  <span class="text-[#423734]"
                    >Frete ({{ shippingSelected?.name || "—" }})</span
                  >
                  <span class="font-semibold text-[#232121]">{{
                    formatBRL(shippingPrice)
                  }}</span>
                </div>
                <div
                  class="pt-3 border-t border-[#b9a994] flex items-center justify-between text-lg font-bold"
                >
                  <span class="text-[#735e59]">Total</span>
                  <span class="text-2xl text-[#735e59]">{{
                    formatBRL(totalWithFreight)
                  }}</span>
                </div>
              </div>
            </div>
          </div>
        </section>

        <!-- Seção de Dados Pessoais -->
        <section
          class="bg-white rounded-2xl shadow-lg border border-[#ede5dd] p-8 hover:shadow-xl transition-all duration-300"
        >
          <header class="mb-6 flex items-center gap-3">
            <div
              class="w-10 h-10 bg-[#ede5dd] rounded-full flex items-center justify-center"
            >
              <svg
                class="w-5 h-5 text-[#735e59]"
                fill="none"
                stroke="currentColor"
                viewBox="0 0 24 24"
              >
                <path
                  stroke-linecap="round"
                  stroke-linejoin="round"
                  stroke-width="2"
                  d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z"
                ></path>
              </svg>
            </div>
            <div>
              <h2 class="text-xl font-bold text-[#232121]">
                Dados para Entrega
              </h2>
              <p class="text-[#423734]">Informações de contato para entrega</p>
            </div>
          </header>

          <div class="space-y-6">
            <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
              <div>
                <label
                  class="block text-sm font-medium text-[#423734] uppercase tracking-wide mb-2"
                >
                  Nome *
                </label>
                <input
                  v-model="form.nome"
                  placeholder="Seu nome"
                  class="w-full px-4 py-3 border-2 border-[#ede5dd] rounded-xl bg-white text-[#232121] placeholder-[#b9a994] focus:border-[#735e59] focus:ring-2 focus:ring-[#ede5dd] transition-all"
                  :class="{
                    'border-red-500 focus:border-red-500 focus:ring-red-200':
                      inputsErro && !form.nome,
                  }"
                  autocomplete="on"
                />
              </div>
              <div>
                <label
                  class="block text-sm font-medium text-[#423734] uppercase tracking-wide mb-2"
                >
                  Sobrenome
                </label>
                <input
                  v-model="form.sobrenome"
                  placeholder="Seu sobrenome"
                  class="w-full px-4 py-3 border-2 border-[#ede5dd] rounded-xl bg-white text-[#232121] placeholder-[#b9a994] focus:border-[#735e59] focus:ring-2 focus:ring-[#ede5dd] transition-all"
                  autocomplete="on"
                />
              </div>
            </div>

            <div>
              <label
                class="block text-sm font-medium text-[#423734] uppercase tracking-wide mb-2"
              >
                Telefone com DDD *
              </label>
              <input
                v-model="form.telefone"
                @input="onTelefoneInput"
                @blur="validarTelefone"
                placeholder="(00) 00000-0000"
                class="w-full px-4 py-3 border-2 border-[#ede5dd] rounded-xl bg-white text-[#232121] placeholder-[#b9a994] focus:border-[#735e59] focus:ring-2 focus:ring-[#ede5dd] transition-all"
                :class="{
                  'border-red-500 focus:border-red-500 focus:ring-red-200':
                    telefoneErro,
                }"
                inputmode="tel"
                autocomplete="on"
                maxlength="15"
              />
              <div
                v-if="telefoneErro"
                class="text-red-500 text-sm mt-2 flex items-center gap-2"
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
                    d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"
                  ></path>
                </svg>
                {{ telefoneErro }}
              </div>
            </div>
          </div>
        </section>

        <!-- Seção de Dados Fiscais -->
        <section
          class="bg-white rounded-2xl shadow-lg border border-[#ede5dd] p-8 hover:shadow-xl transition-all duration-300"
        >
          <header class="mb-6 flex items-center gap-3">
            <div
              class="w-10 h-10 bg-[#ede5dd] rounded-full flex items-center justify-center"
            >
              <svg
                class="w-5 h-5 text-[#735e59]"
                fill="none"
                stroke="currentColor"
                viewBox="0 0 24 24"
              >
                <path
                  stroke-linecap="round"
                  stroke-linejoin="round"
                  stroke-width="2"
                  d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"
                ></path>
              </svg>
            </div>
            <div>
              <h2 class="text-xl font-bold text-[#232121]">
                Dados para Nota Fiscal
              </h2>
              <p class="text-[#423734]">CPF ou CNPJ para emissão da nota</p>
            </div>
          </header>

          <div>
            <label
              class="block text-sm font-medium text-[#423734] uppercase tracking-wide mb-2"
            >
              CPF/CNPJ *
            </label>
            <input
              v-model="form.cpfCnpj"
              @input="onCpfCnpjInput"
              @blur="validarCpfCnpj"
              placeholder="000.000.000-00 ou 00.000.000/0000-00"
              class="w-full px-4 py-3 border-2 border-[#ede5dd] rounded-xl bg-white text-[#232121] placeholder-[#b9a994] focus:border-[#735e59] focus:ring-2 focus:ring-[#ede5dd] transition-all"
              :class="{
                'border-red-500 focus:border-red-500 focus:ring-red-200':
                  cpfCnpjErro,
              }"
              inputmode="numeric"
              autocomplete="on"
              maxlength="18"
            />
            <div
              v-if="cpfCnpjErro"
              class="text-red-500 text-sm mt-2 flex items-center gap-2"
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
                  d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"
                ></path>
              </svg>
              {{ cpfCnpjErro }}
            </div>
          </div>
        </section>

        <!-- Botão de Submissão -->
        <section
          class="bg-white rounded-2xl shadow-lg border border-[#ede5dd] p-8 hover:shadow-xl transition-all duration-300"
        >
          <div class="text-center">
            <button
              type="submit"
              class="w-full px-12 py-4 text-xl bg-gradient-to-r from-[#735e59] to-[#b9a994] text-white font-bold rounded-2xl shadow-lg hover:from-[#b9a994] hover:to-[#735e59] focus:outline-none focus:ring-4 focus:ring-[#ede5dd] transform hover:scale-105 transition-all duration-200"
            >
              <div class="flex items-center justify-center gap-3">
                <svg
                  class="w-6 h-6"
                  fill="none"
                  stroke="currentColor"
                  viewBox="0 0 24 24"
                >
                  <path
                    stroke-linecap="round"
                    stroke-linejoin="round"
                    stroke-width="2"
                    d="M13 7l5 5m0 0l-5 5m5-5H6"
                  ></path>
                </svg>
                Ir para Pagamento
              </div>
            </button>

            <div
              v-if="mensagemErro"
              class="mt-4 p-4 bg-red-50 border border-red-200 rounded-xl text-red-600 flex items-center gap-2 justify-center"
            >
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
                  d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"
                ></path>
              </svg>
              {{ mensagemErro }}
            </div>
          </div>
        </section>
      </form>
    </div>
  </div>
</template>

<script setup>
import { reactive, ref, computed, onMounted } from "vue";
import { useRouter } from "vue-router";
import { cartStore } from "../store/cartStore";
import { calcularFrete } from "../api.js";

onMounted(() => {
  const salvo = localStorage.getItem("formEntrega");
  if (salvo) {
    const dados = JSON.parse(salvo);
    Object.assign(form, dados);

    // Se temos um CEP salvo, busca o endereço automaticamente
    if (dados.cep && dados.cep.replace(/\D/g, "").length === 8) {
      // Aguarda um pouco para garantir que o form foi preenchido
      setTimeout(() => {
        searchCep();
      }, 100);
    }
  }

  // Carrega o CEP do cartStore se existir
  if (cartStore.cep) {
    form.cep = cartStore.cep;
    // Se o CEP do cartStore tem 8 dígitos, busca o endereço
    if (cartStore.cep.replace(/\D/g, "").length === 8) {
      setTimeout(() => {
        searchCep();
      }, 100);
    }
  }

  // Se já temos opções de frete salvas, usamos elas
  if (cartStore.shippingOptions.length > 0) {
    freteResp.value = cartStore.shippingOptions;
  }
});

const router = useRouter();

const form = reactive({
  nome: "",
  sobrenome: "",
  telefone: "",
  cep: "",
  rua: "",
  numero: "",
  complemento: "",
  bairro: "",
  cidade: "",
  estado: "",
  cpfCnpj: "",
  obs: "",
});

// Variáveis para cálculo de frete
const isCalculating = ref(false);
const freteResp = ref([]);
const freteError = ref("");

// Dados do produto para cálculo de frete
const produto = {
  from_postal_code: "95088325",
  to_postal_code: "",
  height: 5,
  width: 12,
  length: 16,
  weight: 0.3,
};

// Helpers
const formatBRL = (n) =>
  (Number(n) || 0).toLocaleString("pt-BR", {
    style: "currency",
    currency: "BRL",
  });

// Converte string de preço com . ou , (em qualquer combinação) para Number
function toNumberFlexible(input) {
  if (typeof input === "number") return input;
  let s = String(input || "").trim();

  // remove símbolos e espaços (R$, $, etc.)
  s = s.replace(/[^\d.,-]/g, "");
  if (!s) return 0;

  const hasComma = s.includes(",");
  const hasDot = s.includes(".");

  if (hasComma && hasDot) {
    // Assume que o último separador (direita) é o decimal
    const lastSepIdx = Math.max(s.lastIndexOf(","), s.lastIndexOf("."));
    const intPart = s.slice(0, lastSepIdx).replace(/[.,]/g, "");
    const fracPart = s.slice(lastSepIdx + 1);
    s = `${intPart}.${fracPart}`;
  } else if (hasComma && !hasDot) {
    // Vírgula como decimal
    s = s.replace(/\./g, ""); // milhares (se houver)
    s = s.replace(",", ".");
  } else {
    // Ponto como decimal; remove vírgulas de milhares
    s = s.replace(/,/g, "");
  }

  const n = Number(s);
  return isNaN(n) ? 0 : n;
}

// Cálculo de frete
async function onCalcularFrete() {
  freteError.value = "";
  cartStore.setShippingSelected(null); // limpa seleção ao recalcular

  const digits = form.cep.replace(/\D/g, "");
  if (digits.length !== 8) {
    freteError.value = "CEP inválido. Use 8 dígitos (ex: 01001000).";
    return;
  }

  // Salva o CEP no store
  cartStore.setCep(form.cep);

  produto.to_postal_code = digits;

  try {
    isCalculating.value = true;
    const resp = await calcularFrete(produto);
    freteResp.value = Array.isArray(resp) ? resp : [];

    // Salva as opções de frete no store
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

// Normaliza as formas de envio (filtra SEDEX/PAC e cria IDs estáveis)
const shippingOptions = computed(() => {
  if (!Array.isArray(freteResp.value)) return [];
  return freteResp.value
    .filter((f) => f && (f.name === "SEDEX" || f.name === "PAC"))
    .map((f, idx) => {
      const priceNum = toNumberFlexible(f.price);

      // Calcula data prevista
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
        delivery_time: f.delivery_time, // número em dias
        estimatedDate, // string formatada
        error: !!f.error,
      };
    })
    .filter((f) => !f.error);
});

// Objeto/valor do frete selecionado
const shippingSelected = computed(() => cartStore.shippingSelected);
const shippingPrice = computed(() =>
  shippingSelected.value ? shippingSelected.value.price : 0
);

// Total com frete
const totalWithFreight = computed(() => {
  const total =
    Number(cartStore.subtotal || 0) + Number(shippingPrice.value || 0);
  return isNaN(total) ? 0 : total;
});

function limparNumero(valor) {
  return (valor || "").replace(/\D/g, "");
}

function isCpfCnpjValido(valor) {
  const num = limparNumero(valor);
  if (num.length === 11) return isCPFValido(num);
  if (num.length === 14) return isCNPJValido(num);
  return false;
}

function isCPFValido(cpf) {
  const n = limparNumero(cpf);
  if (n.length !== 11) return false;
  if (/^(\d)\1{10}$/.test(n)) return false;

  let soma = 0;
  for (let i = 0; i < 9; i++) soma += Number(n[i]) * (10 - i);
  let resto = soma % 11;
  const dv1 = resto < 2 ? 0 : 11 - resto;
  if (dv1 !== Number(n[9])) return false;

  soma = 0;
  for (let i = 0; i < 10; i++) soma += Number(n[i]) * (11 - i);
  resto = soma % 11;
  const dv2 = resto < 2 ? 0 : 11 - resto;

  return dv2 === Number(n[10]);
}

function isCNPJValido(cnpj) {
  const n = limparNumero(cnpj);
  if (n.length !== 14) return false;
  if (/^(\d)\1{13}$/.test(n)) return false;

  const pesos1 = [5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2];
  const pesos2 = [6, 5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2];

  const calcDV = (base, pesos) => {
    const soma = base
      .split("")
      .reduce((acc, dig, i) => acc + Number(dig) * pesos[i], 0);
    const resto = soma % 11;
    return resto < 2 ? 0 : 11 - resto;
  };

  const dv1 = calcDV(n.slice(0, 12), pesos1);
  if (dv1 !== Number(n[12])) return false;

  const dv2 = calcDV(n.slice(0, 13), pesos2);
  return dv2 === Number(n[13]);
}

function isTelefoneValido(telefone) {
  const telLimpo = limparNumero(telefone);
  return /^(\d{10}|\d{11})$/.test(telLimpo);
}

function aplicarMascaraTelefone(valor) {
  const d = limparNumero(valor).slice(0, 11);
  if (d.length === 0) return "";
  if (d.length <= 2) return `(${d}`;
  if (d.length <= 6) return `(${d.slice(0, 2)}) ${d.slice(2)}`;
  if (d.length <= 10)
    return `(${d.slice(0, 2)}) ${d.slice(2, 6)}-${d.slice(6)}`;
  return `(${d.slice(0, 2)}) ${d.slice(2, 7)}-${d.slice(7)}`;
}

function onTelefoneInput(e) {
  form.telefone = aplicarMascaraTelefone(e.target.value);
  mensagemErro.value = "";
}

function aplicarMascaraCpf(cpf) {
  const d = limparNumero(cpf).slice(0, 11);
  if (d.length <= 3) return d;
  if (d.length <= 6) return `${d.slice(0, 3)}.${d.slice(3)}`;
  if (d.length <= 9) return `${d.slice(0, 3)}.${d.slice(3, 6)}.${d.slice(6)}`;
  return `${d.slice(0, 3)}.${d.slice(3, 6)}.${d.slice(6, 9)}-${d.slice(9)}`;
}

function aplicarMascaraCnpj(cnpj) {
  const d = limparNumero(cnpj).slice(0, 14);
  if (d.length <= 2) return d;
  if (d.length <= 5) return `${d.slice(0, 2)}.${d.slice(2)}`;
  if (d.length <= 8) return `${d.slice(0, 2)}.${d.slice(2, 5)}.${d.slice(5)}`;
  if (d.length <= 12)
    return `${d.slice(0, 2)}.${d.slice(2, 5)}.${d.slice(5, 8)}/${d.slice(8)}`;
  return `${d.slice(0, 2)}.${d.slice(2, 5)}.${d.slice(5, 8)}/${d.slice(
    8,
    12
  )}-${d.slice(12)}`;
}

function aplicarMascaraCpfCnpj(valor) {
  const d = limparNumero(valor);
  return d.length <= 11 ? aplicarMascaraCpf(d) : aplicarMascaraCnpj(d);
}

function onCpfCnpjInput(e) {
  form.cpfCnpj = aplicarMascaraCpfCnpj(e.target.value);
  mensagemErro.value = "";
}

const mensagemErro = ref("");
const cepErro = ref("");
const cepLoading = ref(false);
const inputsErro = ref(false);

function limparCep(valor) {
  return (valor || "").replace(/\D/g, "");
}

function aplicarMascaraCep(valor) {
  const digits = limparCep(valor).slice(0, 8);
  if (digits.length <= 5) return digits;
  return `${digits.slice(0, 5)}-${digits.slice(5)}`;
}

function isCepValido(cepLimpo) {
  return /^\d{8}$/.test(cepLimpo);
}

function onCepInput(e) {
  form.cep = aplicarMascaraCep(e.target.value);
  cepErro.value = "";

  // Chama automaticamente o cálculo de frete quando o CEP tem 8 dígitos
  const digits = form.cep.replace(/\D/g, "");
  if (digits.length === 8) {
    onCalcularFrete();
  }
}

async function searchCep() {
  const cepLimpo = limparCep(form.cep);

  if (!cepLimpo) {
    cepErro.value = "Informe o CEP.";
    return;
  }
  if (!isCepValido(cepLimpo)) {
    cepErro.value = "CEP inválido. Use o formato 99999-999.";
    return;
  }

  cepErro.value = "";
  cepLoading.value = true;

  try {
    const resp = await fetch(`https://viacep.com.br/ws/${cepLimpo}/json/`);
    if (!resp.ok) throw new Error("Falha ao consultar CEP");
    const data = await resp.json();

    if (data.erro) {
      cepErro.value = "CEP não encontrado.";
      return;
    }

    form.rua = data.logradouro || form.rua;
    form.bairro = data.bairro || form.bairro;
    form.cidade = data.localidade || form.cidade;
    form.estado = data.uf || form.estado;
  } catch (e) {
    cepErro.value = "Não foi possível buscar o endereço. Tente novamente.";
  } finally {
    cepLoading.value = false;
  }
}

const telefoneErro = ref("");

function validarTelefone() {
  if (!isTelefoneValido(form.telefone)) {
    telefoneErro.value = "Telefone inválido. Use DDD + número.";
  } else {
    telefoneErro.value = "";
  }
}

const cpfCnpjErro = ref("");

function validarCpfCnpj() {
  if (!isCpfCnpjValido(form.cpfCnpj)) {
    cpfCnpjErro.value = "CPF ou CNPJ inválido.";
  } else {
    cpfCnpjErro.value = "";
  }
}

function voltarParaCarrinho() {
  // Volta para a página inicial e abre o carrinho
  cartStore.openCart();
  router.push("/");
}

// Computed para verificar se todos os campos obrigatórios estão preenchidos
const todosObrigatoriosPreenchidos = computed(() => {
  const camposObrigatorios = [
    "nome",
    "telefone",
    "cep",
    "rua",
    "numero",
    "bairro",
    "cidade",
    "estado",
    "cpfCnpj",
  ];

  // Verifica se todos os campos obrigatórios estão preenchidos
  const todosCamposPreenchidos = camposObrigatorios.every(
    (campo) => String(form[campo] || "").trim().length > 0
  );

  // Verifica se CEP é válido
  const cepLimpo = limparCep(form.cep);
  const cepValido = isCepValido(cepLimpo);

  // Verifica se telefone é válido
  const telefoneValido = isTelefoneValido(form.telefone);

  // Verifica se CPF/CNPJ é válido
  const cpfCnpjValido = isCpfCnpjValido(form.cpfCnpj);

  return todosCamposPreenchidos && cepValido && telefoneValido && cpfCnpjValido;
});

function irParaPagamento() {
  if (!todosObrigatoriosPreenchidos.value) {
    mensagemErro.value =
      "Por favor, preencha todos os campos obrigatórios antes de continuar";
    inputsErro.value = true;
    return;
  }

  // Salva os dados antes de ir para pagamento
  localStorage.setItem("formEntrega", JSON.stringify(form));
  router.push("/pagamento");
}

function submitForm() {
  const camposObrigatorios = [
    "nome",
    "telefone",
    "cep",
    "rua",
    "numero",
    "bairro",
    "cidade",
    "estado",
    "cpfCnpj",
  ];

  const cepLimpo = limparCep(form.cep);
  if (!isCepValido(cepLimpo)) {
    cepErro.value = "CEP inválido. Use o formato 99999-999.";
  }

  const campoVazio = camposObrigatorios.find(
    (campo) => !String(form[campo] || "").trim()
  );

  if (!isTelefoneValido(form.telefone)) {
    telefoneErro.value = "Telefone inválido. Use DDD + número.";
  }

  if (!isCpfCnpjValido(form.cpfCnpj)) {
    cpfCnpjErro.value = "CPF ou CNPJ inválido.";
  }

  if (campoVazio) {
    mensagemErro.value = "Por favor, preencha todos os campos obrigatórios*";
  }

  if (
    !isTelefoneValido(form.telefone) ||
    !isCpfCnpjValido(form.cpfCnpj) ||
    campoVazio ||
    !isCepValido(cepLimpo)
  ) {
    inputsErro.value = true;
    return;
  }

  mensagemErro.value = "";

  localStorage.setItem("formEntrega", JSON.stringify(form));

  router.push("/pagamento");
}
</script>
