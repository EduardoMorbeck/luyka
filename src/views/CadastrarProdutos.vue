<template>
  <div
    class="w-full min-h-screen bg-gradient-to-br from-[#ede5dd] via-white to-[#f5f0ea] relative overflow-hidden py-28"
  >
    <div class="absolute inset-0 opacity-10">
      <div
        class="absolute top-10 left-10 w-32 h-32 bg-[#b9a994] rounded-full blur-3xl"
      ></div>
      <div
        class="absolute bottom-20 right-20 w-40 h-40 bg-[#735e59] rounded-full blur-3xl"
      ></div>
      <div
        class="absolute top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2 w-60 h-60 bg-[#b9a994] rounded-full blur-3xl"
      ></div>
    </div>

    <div class="max-w-4xl mx-auto px-6 lg:px-8 relative z-10">
      <div class="text-center mb-12">
        <h1
          class="text-4xl lg:text-6xl font-bold bg-gradient-to-r from-[#735e59] via-[#b9a994] to-[#735e59] bg-clip-text text-transparent font-['Prata',serif] tracking-wider mb-4 transform transition-all duration-700 hover:scale-105 cursor-pointer"
        >
          CADASTRAR PRODUTOS
        </h1>
      </div>

      <form
        class="grid grid-cols-1 md:grid-cols-5 gap-4 bg-white shadow-xl rounded-2xl p-8 border border-[#ede5dd] mb-10 transform transition-all duration-300 hover:shadow-2xl cursor-pointer"
        @submit.prevent="onCreate"
      >
        <div class="md:col-span-5">
          <label class="block text-sm font-semibold mb-2 text-[#735e59]">
            <i class="fa-solid fa-images mr-2"></i>
            Imagens
            <span
              v-if="createImagesPreview.length > 0"
              class="text-sm text-[#b9a994] font-normal ml-2"
            >
              ({{ createImagesPreview.length }} selecionada{{
                createImagesPreview.length > 1 ? "s" : ""
              }})
            </span>
          </label>
          <div class="flex gap-3">
            <input
              v-if="!limiteImagensAtingido"
              type="file"
              accept="image/*"
              multiple
              ref="createFileInput"
              class="flex-1 hidden"
              @change="onCreateImagesChange"
            />
            <button
              v-if="!limiteImagensAtingido"
              type="button"
              @click="addMoreImages"
              class="w-full px-4 py-3 border-2 border-[#735e59] rounded-xl hover:bg-[#735e59] hover:text-white transition-all duration-300 text-sm font-medium text-[#735e59] group shadow-sm hover:shadow-md transform hover:-translate-y-0.5 cursor-pointer"
            >
              <i
                class="fa-solid fa-plus-circle mr-2 group-hover:rotate-90 transition-transform duration-300"
              ></i>
              Adicionar Imagem
            </button>
            <div
              v-else
              class="w-full px-4 py-3 border-2 border-amber-400 bg-amber-50 rounded-xl text-amber-800 text-sm font-medium"
            >
              <i class="fa-solid fa-circle-info"></i>
              Limite de produtos com imagens atingido (máximo 2). Site ainda não
              possui um banco de dados para armazenar mais produtos com imagens.
            </div>
          </div>
          <div
            v-if="createImagesPreview.length > 0"
            class="mt-4 flex flex-wrap gap-4"
          >
            <div
              v-for="(preview, index) in createImagesPreview"
              :key="index"
              class="relative group transform transition-all duration-300 hover:scale-105 cursor-pointer"
            >
              <div
                class="relative overflow-hidden rounded-xl border-2 border-[#ede5dd] shadow-lg hover:shadow-xl hover:border-[#b9a994] transition-all duration-300 cursor-pointer"
              >
                <img
                  :src="preview"
                  class="h-80 w-80 object-cover flex-shrink-0"
                  alt="Preview da imagem"
                />
              </div>
              <button
                type="button"
                @click="removeCreateImage(index)"
                class="absolute top-2 right-2 bg-red-500 hover:bg-red-600 text-white rounded-full w-8 h-8 flex items-center justify-center opacity-0 group-hover:opacity-100 transition-all duration-300 shadow-lg hover:scale-110 cursor-pointer"
              >
                <i class="fa-solid fa-xmark text-sm"></i>
              </button>
            </div>
          </div>
        </div>

        <div class="md:col-span-2">
          <label class="block text-sm font-semibold mb-2 text-[#735e59]">
            <i class="fa-solid fa-tag mr-2"></i>
            Nome
          </label>
          <input
            v-model="createForm.nome"
            class="w-full border-2 border-[#ede5dd] rounded-xl p-3 focus:border-[#735e59] focus:ring-2 focus:ring-[#735e59]/20 transition-all duration-300 text-[#232121]"
            placeholder="Nome do produto"
            required
          />
        </div>
        <div>
          <label class="block text-sm font-semibold mb-2 text-[#735e59]">
            <i class="fa-solid fa-dollar-sign mr-2"></i>
            Preço
          </label>
          <input
            v-model.number="createForm.preco"
            type="number"
            step="0.01"
            min="0"
            class="w-full border-2 border-[#ede5dd] rounded-xl p-3 focus:border-[#735e59] focus:ring-2 focus:ring-[#735e59]/20 transition-all duration-300 text-[#232121]"
            placeholder="0.00"
            required
          />
        </div>
        <div>
          <label class="block text-sm font-semibold mb-2 text-[#735e59]">
            <i class="fa-solid fa-box mr-2"></i>
            Estoque
          </label>
          <input
            v-model.number="createForm.estoque"
            type="number"
            min="0"
            class="w-full border-2 border-[#ede5dd] rounded-xl p-3 focus:border-[#735e59] focus:ring-2 focus:ring-[#735e59]/20 transition-all duration-300 text-[#232121]"
            placeholder="0"
            required
          />
        </div>
        <div>
          <label class="block text-sm font-semibold mb-2 text-[#735e59]">
            <i class="fa-solid fa-folder mr-2"></i>
            Categoria
          </label>
          <input
            v-model="createForm.categoria"
            @input="
              createForm.categoria = normalizeCategoria(createForm.categoria)
            "
            class="w-full border-2 border-[#ede5dd] rounded-xl p-3 focus:border-[#735e59] focus:ring-2 focus:ring-[#735e59]/20 transition-all duration-300 text-[#232121]"
            placeholder="Categoria"
          />
        </div>
        <div class="md:col-span-5">
          <label class="block text-sm font-semibold mb-2 text-[#735e59]">
            <i class="fa-solid fa-align-left mr-2"></i>
            Descrição
          </label>
          <textarea
            v-model="createForm.descricao"
            rows="3"
            class="w-full border-2 border-[#ede5dd] rounded-xl p-3 focus:border-[#735e59] focus:ring-2 focus:ring-[#735e59]/20 transition-all duration-300 text-[#232121] resize-none"
            placeholder="Descrição do produto"
          ></textarea>
        </div>
        <div class="md:col-span-5 flex justify-end">
          <button
            :disabled="loading"
            class="group relative inline-flex items-center justify-center px-8 py-3 rounded-full bg-gradient-to-r from-[#735e59] to-[#b9a994] text-white font-semibold hover:from-[#5a4a46] hover:to-[#735e59] transition-all duration-300 shadow-lg hover:shadow-xl transform hover:-translate-y-0.5 disabled:opacity-50 disabled:cursor-not-allowed disabled:transform-none cursor-pointer"
          >
            <i
              v-if="!loading"
              class="fa-solid fa-plus-circle mr-2 group-hover:rotate-90 transition-transform duration-300"
            ></i>
            <i v-else class="fa-solid fa-spinner fa-spin mr-2"></i>
            {{ loading ? "Salvando..." : "Adicionar Produto" }}
          </button>
        </div>
      </form>

      <div v-if="produtos.length > 0" class="grid gap-6">
        <div
          v-for="(p, idx) in produtos"
          :key="p.id"
          class="bg-white rounded-2xl shadow-lg p-4 md:p-6 flex flex-col md:flex-row justify-between items-start gap-4 md:gap-6 border border-[#ede5dd] transform transition-all duration-300 hover:shadow-xl hover:border-[#b9a994] animate-fade-in-up cursor-pointer"
          :style="{ animationDelay: `${idx * 100}ms` }"
        >
          <div
            v-if="editId === p.id"
            class="w-full grid grid-cols-1 md:grid-cols-5 gap-6 md:gap-4 bg-gradient-to-br from-[#f5f0ea] to-white shadow-xl rounded-2xl p-4 md:p-8 border-2 border-[#b9a994] -mx-2 md:mx-0"
          >
            <div class="md:col-span-5">
              <label
                class="block text-base md:text-sm font-semibold mb-3 md:mb-2 text-[#735e59]"
              >
                <i class="fa-solid fa-images mr-2"></i>
                Imagens
                <span
                  v-if="editImagesPreview.length > 0"
                  class="text-sm text-[#b9a994] font-normal ml-2"
                >
                  ({{ editImagesPreview.length }} nova{{
                    editImagesPreview.length > 1 ? "s" : ""
                  }})
                </span>
              </label>
              <div class="flex gap-3">
                <input
                  v-if="!limiteImagensAtingido"
                  type="file"
                  accept="image/*"
                  multiple
                  ref="editFileInput"
                  class="flex-1 hidden"
                  @change="onEditImagesChange"
                />
                <button
                  v-if="!limiteImagensAtingido"
                  type="button"
                  @click="addMoreImagesEdit"
                  class="w-full px-4 py-4 md:py-3 border-2 border-[#735e59] rounded-xl hover:bg-[#735e59] active:bg-[#5a4a46] hover:text-white transition-all duration-300 text-base md:text-sm font-medium text-[#735e59] group shadow-sm hover:shadow-md transform hover:-translate-y-0.5 active:translate-y-0 cursor-pointer touch-manipulation min-h-[48px] md:min-h-[44px]"
                >
                  <i
                    class="fa-solid fa-plus-circle mr-2 group-hover:rotate-90 transition-transform duration-300"
                  ></i>
                  Adicionar Imagem
                </button>
                <div
                  v-else
                  class="w-full px-4 py-3 border-2 border-amber-400 bg-amber-50 rounded-xl text-amber-800 text-sm font-medium"
                >
                  <i class="fa-solid fa-circle-info"></i>
                  Limite de produtos com imagens atingido (máximo 2). Site ainda
                  não possui um banco de dados para armazenar mais produtos com
                  imagens.
                </div>
              </div>
              <div v-if="getImagensUrls(p).length > 0" class="mt-4 md:mt-4">
                <p
                  class="text-base md:text-sm font-semibold text-[#735e59] mb-3"
                >
                  <i class="fa-solid fa-images mr-2"></i>
                  Imagens existentes:
                </p>
                <div
                  class="flex flex-wrap gap-3 md:gap-4 mb-4 overflow-x-auto pb-2 md:pb-0"
                >
                  <div
                    v-for="(url, index) in getImagensUrls(p)"
                    :key="index"
                    class="relative group transform transition-all duration-300 hover:scale-105 active:scale-95 cursor-pointer flex-shrink-0"
                  >
                    <div
                      class="relative overflow-hidden rounded-xl border-2 border-[#ede5dd] shadow-lg hover:shadow-xl hover:border-[#b9a994] transition-all duration-300 cursor-pointer"
                    >
                      <img
                        :src="url"
                        class="h-48 w-48 md:h-80 md:w-80 object-cover"
                        alt="Imagem existente"
                      />
                    </div>
                    <button
                      type="button"
                      @click="deleteImagemExistente(p.id, index)"
                      class="absolute top-2 right-2 bg-red-500 hover:bg-red-600 active:bg-red-700 text-white rounded-full w-10 h-10 md:w-8 md:h-8 flex items-center justify-center opacity-100 md:opacity-0 md:group-hover:opacity-100 transition-all duration-300 shadow-lg hover:scale-110 active:scale-95 cursor-pointer touch-manipulation"
                    >
                      <i class="fa-solid fa-xmark text-base md:text-sm"></i>
                    </button>
                  </div>
                </div>
              </div>
              <div v-if="editImagesPreview.length > 0" class="mt-4 md:mt-4">
                <p
                  class="text-base md:text-sm font-semibold text-[#735e59] mb-3"
                >
                  <i class="fa-solid fa-plus-circle mr-2"></i>
                  Novas imagens:
                </p>
                <div
                  class="flex flex-wrap gap-3 md:gap-4 overflow-x-auto pb-2 md:pb-0"
                >
                  <div
                    v-for="(preview, index) in editImagesPreview"
                    :key="index"
                    class="relative group transform transition-all duration-300 hover:scale-105 active:scale-95 cursor-pointer flex-shrink-0"
                  >
                    <div
                      class="relative overflow-hidden rounded-xl border-2 border-[#b9a994] shadow-lg hover:shadow-xl transition-all duration-300"
                    >
                      <img
                        :src="preview"
                        class="h-48 w-48 md:h-80 md:w-80 object-cover"
                        alt="Preview da nova imagem"
                      />
                    </div>
                    <button
                      type="button"
                      @click="removeEditImage(index)"
                      class="absolute top-2 right-2 bg-red-500 hover:bg-red-600 active:bg-red-700 text-white rounded-full w-10 h-10 md:w-8 md:h-8 flex items-center justify-center opacity-100 md:opacity-0 md:group-hover:opacity-100 transition-all duration-300 shadow-lg hover:scale-110 active:scale-95 cursor-pointer touch-manipulation"
                    >
                      <i class="fa-solid fa-xmark text-base md:text-sm"></i>
                    </button>
                  </div>
                </div>
              </div>
            </div>

            <div class="md:col-span-2">
              <label
                class="block text-base md:text-sm font-semibold mb-3 md:mb-2 text-[#735e59]"
              >
                <i class="fa-solid fa-tag mr-2"></i>
                Nome
              </label>
              <input
                v-model="editForm.nome"
                class="w-full border-2 border-[#ede5dd] rounded-xl p-4 md:p-3 text-base md:text-sm focus:border-[#735e59] focus:ring-2 focus:ring-[#735e59]/20 transition-all duration-300 text-[#232121] min-h-[44px]"
                required
              />
            </div>

            <div>
              <label
                class="block text-base md:text-sm font-semibold mb-3 md:mb-2 text-[#735e59]"
              >
                <i class="fa-solid fa-dollar-sign mr-2"></i>
                Preço
              </label>
              <input
                v-model.number="editForm.preco"
                type="number"
                step="0.01"
                min="0"
                class="w-full border-2 border-[#ede5dd] rounded-xl p-4 md:p-3 text-base md:text-sm focus:border-[#735e59] focus:ring-2 focus:ring-[#735e59]/20 transition-all duration-300 text-[#232121] min-h-[44px]"
                required
              />
            </div>

            <div>
              <label
                class="block text-base md:text-sm font-semibold mb-3 md:mb-2 text-[#735e59]"
              >
                <i class="fa-solid fa-box mr-2"></i>
                Estoque
              </label>
              <input
                v-model.number="editForm.estoque"
                type="number"
                min="0"
                class="w-full border-2 border-[#ede5dd] rounded-xl p-4 md:p-3 text-base md:text-sm focus:border-[#735e59] focus:ring-2 focus:ring-[#735e59]/20 transition-all duration-300 text-[#232121] min-h-[44px]"
                required
              />
            </div>

            <div>
              <label
                class="block text-base md:text-sm font-semibold mb-3 md:mb-2 text-[#735e59]"
              >
                <i class="fa-solid fa-folder mr-2"></i>
                Categoria
              </label>
              <input
                v-model="editForm.categoria"
                @input="
                  editForm.categoria = normalizeCategoria(editForm.categoria)
                "
                class="w-full border-2 border-[#ede5dd] rounded-xl p-4 md:p-3 text-base md:text-sm focus:border-[#735e59] focus:ring-2 focus:ring-[#735e59]/20 transition-all duration-300 text-[#232121] min-h-[44px]"
              />
            </div>

            <div class="md:col-span-5">
              <label
                class="block text-base md:text-sm font-semibold mb-3 md:mb-2 text-[#735e59]"
              >
                <i class="fa-solid fa-align-left mr-2"></i>
                Descrição
              </label>
              <textarea
                v-model="editForm.descricao"
                rows="4"
                class="w-full border-2 border-[#ede5dd] rounded-xl p-4 md:p-3 text-base md:text-sm focus:border-[#735e59] focus:ring-2 focus:ring-[#735e59]/20 transition-all duration-300 text-[#232121] resize-none"
              ></textarea>
            </div>

            <div
              class="md:col-span-5 flex flex-col md:flex-row justify-end gap-3 md:gap-3"
            >
              <button
                @click="onSave(p.id)"
                :disabled="loading"
                class="w-full md:w-auto group relative inline-flex items-center justify-center px-8 py-4 md:py-3 rounded-full bg-gradient-to-r from-[#735e59] to-[#b9a994] text-white font-semibold text-base md:text-sm hover:from-[#5a4a46] hover:to-[#735e59] active:from-[#4a3d38] active:to-[#5a4a46] transition-all duration-300 shadow-lg hover:shadow-xl transform hover:-translate-y-0.5 active:translate-y-0 disabled:opacity-50 disabled:cursor-not-allowed disabled:transform-none cursor-pointer touch-manipulation min-h-[48px] md:min-h-[44px]"
              >
                <i
                  v-if="!loading"
                  class="fa-solid fa-check mr-2 group-hover:scale-110 transition-transform duration-300"
                ></i>
                <i v-else class="fa-solid fa-spinner fa-spin mr-2"></i>
                {{ loading ? "Salvando..." : "Salvar" }}
              </button>
              <button
                @click="onCancel()"
                class="w-full md:w-auto px-8 py-4 md:py-3 rounded-full border-2 border-[#b9a994] text-[#735e59] font-semibold text-base md:text-sm hover:bg-[#ede5dd] active:bg-[#e5ddd5] transition-all duration-300 shadow-sm hover:shadow-md transform hover:-translate-y-0.5 active:translate-y-0 cursor-pointer touch-manipulation min-h-[48px] md:min-h-[44px]"
              >
                <i class="fa-solid fa-times mr-2"></i>
                Cancelar
              </button>
            </div>
          </div>

          <div v-else class="flex flex-1 items-start gap-6 flex-wrap">
            <div class="flex flex-col gap-3">
              <div
                v-if="getImagensUrls(p).length > 0"
                class="flex gap-3 overflow-x-auto pb-2"
              >
                <div
                  v-for="(url, index) in getImagensUrls(p)"
                  :key="index"
                  class="relative group"
                >
                  <div
                    class="relative overflow-hidden rounded-xl border-2 border-[#ede5dd] shadow-lg hover:shadow-xl hover:border-[#b9a994] transition-all duration-300 cursor-pointer"
                  >
                    <img
                      :src="url"
                      class="h-80 w-80 object-cover flex-shrink-0"
                      alt="Imagem do produto"
                    />
                  </div>
                </div>
              </div>
              <div
                v-else
                class="h-80 w-80 bg-gradient-to-br from-[#ede5dd] to-[#f5f0ea] rounded-xl border-2 border-[#ede5dd] flex items-center justify-center text-[#b9a994]"
              >
                <div class="text-center">
                  <i class="fa-solid fa-image text-4xl mb-2"></i>
                  <p class="text-sm font-medium">Sem imagem</p>
                </div>
              </div>
            </div>
            <div class="flex flex-col gap-3 flex-1 min-w-[200px]">
              <div
                class="font-bold text-2xl text-[#735e59] font-['Prata',serif]"
              >
                {{ p.nome }}
              </div>
              <div class="flex flex-wrap items-center gap-3 text-sm">
                <span
                  class="px-3 py-1 bg-[#ede5dd] text-[#735e59] rounded-full font-semibold"
                >
                  <i class="fa-solid fa-dollar-sign mr-1"></i>
                  {{ formatPrice(p.preco) }}
                </span>
                <span
                  class="px-3 py-1 bg-[#ede5dd] text-[#735e59] rounded-full font-semibold"
                >
                  <i class="fa-solid fa-box mr-1"></i>
                  {{ p.estoque }} unid.
                </span>
                <span
                  v-if="p.categoria"
                  class="px-3 py-1 bg-[#b9a994] text-white rounded-full font-semibold"
                >
                  <i class="fa-solid fa-folder mr-1"></i>
                  {{ p.categoria }}
                </span>
              </div>
              <div
                class="text-sm text-[#735e59]/80 leading-relaxed"
                v-if="p.descricao"
              >
                {{ p.descricao }}
              </div>
            </div>
          </div>

          <div
            v-if="editId !== p.id"
            class="shrink-0 flex flex-col gap-3 min-w-[140px]"
          >
            <button
              @click="onEdit(p)"
              class="group px-6 py-3 rounded-full border-2 border-[#735e59] text-[#735e59] font-semibold hover:bg-[#735e59] hover:text-white transition-all duration-300 shadow-sm hover:shadow-md transform hover:-translate-y-0.5 cursor-pointer"
            >
              <i
                class="fa-solid fa-pencil mr-2 group-hover:rotate-12 transition-transform duration-300"
              ></i>
              Editar
            </button>
            <button
              @click="onDelete(p.id)"
              class="px-6 py-3 rounded-full bg-red-500 text-white font-semibold hover:bg-red-600 transition-all duration-300 shadow-sm hover:shadow-md transform hover:-translate-y-0.5 cursor-pointer"
            >
              <i class="fa-solid fa-trash mr-2"></i>
              Excluir
            </button>
          </div>
        </div>
      </div>

      <div
        v-else
        class="text-center py-16 bg-white rounded-2xl shadow-lg border border-[#ede5dd]"
      >
        <i class="fa-solid fa-box-open text-6xl text-[#b9a994] mb-4"></i>
        <p class="text-xl text-[#735e59] font-semibold">
          Nenhum produto encontrado.
        </p>
        <p class="text-sm text-[#735e59]/60 mt-2">
          Comece adicionando seu primeiro produto acima
        </p>
      </div>
    </div>

    <!-- Sistema de Notificações -->
    <div class="fixed bottom-6 right-6 z-50 space-y-3">
      <Notification
        v-for="(notification, index) in notifications"
        :key="notification.id"
        :title="notification.title"
        :description="notification.description"
        :type="notification.type"
        :duration="notification.duration || 5000"
        @close="removeNotification(notification.id)"
      />
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from "vue";
import {
  getProdutos,
  createProduto,
  updateProduto,
  deleteProdutoById,
  uploadImagemProduto,
  deleteImagemProduto,
  getImagensProduto,
} from "/src/api.js";
import Notification from "/src/components/Notification.vue";

const produtos = ref([]);
const loading = ref(false);
const notifications = ref([]);
let notificationIdCounter = 0;

const createForm = ref({
  nome: "",
  preco: 0,
  estoque: 0,
  categoria: "",
  descricao: "",
});
const createImagesFiles = ref([]);
const createImagesPreview = ref([]);
const createFileInput = ref(null);

const editId = ref(null);
const editForm = ref({
  nome: "",
  preco: 0,
  estoque: 0,
  categoria: "",
  descricao: "",
});
const editImagesFiles = ref([]);
const editImagesPreview = ref([]);
const editFileInput = ref(null);

function readPreview(files, targetRef) {
  targetRef.value = [];
  if (!files || files.length === 0) return;

  Array.from(files).forEach((file) => {
    const reader = new FileReader();
    reader.onload = (e) => {
      targetRef.value.push(e.target.result);
    };
    reader.readAsDataURL(file);
  });
}

function onCreateImagesChange(e) {
  const files = e.target.files || [];
  if (files.length === 0) return;

  const newFiles = Array.from(files);
  createImagesFiles.value = [...createImagesFiles.value, ...newFiles];

  newFiles.forEach((file) => {
    const reader = new FileReader();
    reader.onload = (e) => {
      createImagesPreview.value.push(e.target.result);
    };
    reader.readAsDataURL(file);
  });

  e.target.value = "";
}

function onEditImagesChange(e) {
  const files = e.target.files || [];
  if (files.length === 0) return;

  const newFiles = Array.from(files);
  editImagesFiles.value = [...editImagesFiles.value, ...newFiles];

  newFiles.forEach((file) => {
    const reader = new FileReader();
    reader.onload = (e) => {
      editImagesPreview.value.push(e.target.result);
    };
    reader.readAsDataURL(file);
  });

  e.target.value = "";
}

function addMoreImages(event) {
  const button = event?.currentTarget || event?.target;
  if (button) {
    const form = button.closest("form");
    const fileInput = form?.querySelector('input[type="file"]');
    if (fileInput && typeof fileInput.click === "function") {
      fileInput.click();
      return;
    }
  }

  const fileInput = createFileInput.value;
  if (fileInput) {
    const input = Array.isArray(fileInput) ? fileInput[0] : fileInput;
    if (input && typeof input.click === "function") {
      input.click();
      return;
    }
  }

  const fallbackInput = document.querySelector(
    'form[class*="grid"]:not([class*="items-end"]) input[type="file"]'
  );
  if (fallbackInput && typeof fallbackInput.click === "function") {
    fallbackInput.click();
  }
}

function addMoreImagesEdit(event) {
  const button = event?.currentTarget || event?.target;
  if (button) {
    const form = button.closest("form, .grid");
    const fileInput = form?.querySelector('input[type="file"]');
    if (fileInput && typeof fileInput.click === "function") {
      fileInput.click();
    }
  } else {
    const fileInput = editFileInput.value;
    if (fileInput) {
      const input = Array.isArray(fileInput) ? fileInput[0] : fileInput;
      if (input && typeof input.click === "function") {
        input.click();
      }
    }
  }
}

function removeCreateImage(index) {
  createImagesPreview.value.splice(index, 1);
  createImagesFiles.value.splice(index, 1);
}

function removeEditImage(index) {
  editImagesPreview.value.splice(index, 1);
  editImagesFiles.value.splice(index, 1);
}

function deleteImagemExistente(produtoId, imagemIndex) {
  if (!confirm("Tem certeza que deseja excluir esta imagem?")) return;

  deleteImagemProduto(produtoId, imagemIndex)
    .then(() => {
      fetchProdutos();
      showNotification(
        "Imagem excluída",
        "A imagem foi excluída com sucesso.",
        "success"
      );
    })
    .catch((err) => {
      console.error("Erro ao excluir imagem:", err);
      if (err.message && err.message.includes("Quota")) {
        showNotification("Erro ao excluir imagem", err.message, "error", 7000);
      } else {
        showNotification(
          "Erro ao excluir imagem",
          "Ocorreu um erro ao tentar excluir a imagem. Tente novamente.",
          "error"
        );
      }
    });
}

function getImagensUrls(produto) {
  if (produto.imagens_url && produto.imagens_url.length > 0) {
    return produto.imagens_url;
  }
  if (produto.imagem_path && produto.imagem_path.length > 0) {
    return Array.isArray(produto.imagem_path)
      ? produto.imagem_path
      : [produto.imagem_path];
  }
  return [];
}

const produtosComImagens = computed(() => {
  return produtos.value.filter((p) => {
    const imagens = getImagensUrls(p);
    return imagens.length > 0;
  }).length;
});

const limiteImagensAtingido = computed(() => {
  return produtosComImagens.value >= 2;
});

function normalizeCategoria(value) {
  if (!value) return "";
  return value.replace(/\s+/g, "-").replace(/\//g, "-");
}

function formatPrice(price) {
  return new Intl.NumberFormat("pt-BR", {
    style: "currency",
    currency: "BRL",
  }).format(Number(price ?? 0));
}

function showNotification(title, description, type = "error", duration = 5000) {
  const id = ++notificationIdCounter;
  notifications.value.push({
    id,
    title,
    description,
    type,
    duration,
  });
}

function removeNotification(id) {
  const index = notifications.value.findIndex((n) => n.id === id);
  if (index > -1) {
    notifications.value.splice(index, 1);
  }
}

function fetchProdutos() {
  return getProdutos()
    .then((res) => {
      produtos.value = res;
    })
    .catch((err) => {
      console.error("Erro ao buscar produtos:", err);
    });
}

function onCreate() {
  loading.value = true;
  createProduto({ ...createForm.value })
    .then((response) => {
      if (createImagesFiles.value.length > 0) {
        const uploadPromises = createImagesFiles.value.map((file) =>
          uploadImagemProduto(response.id, file)
        );
        return Promise.all(uploadPromises);
      }
      return Promise.resolve();
    })
    .then(() => {
      createForm.value = {
        nome: "",
        preco: 0,
        estoque: 0,
        categoria: "",
        descricao: "",
      };

      createImagesFiles.value = [];
      createImagesPreview.value = [];

      showNotification(
        "Produto criado",
        "O produto foi adicionado com sucesso!",
        "success"
      );

      return fetchProdutos();
    })
    .catch((err) => {
      console.error("Erro ao criar produto:", err);
      let titulo = "Erro ao criar produto";
      let descricao = "Verifique os dados e tente novamente.";

      if (
        err.message &&
        (err.message.includes("QuotaExceededError") ||
          err.message.includes("Quota") ||
          err.message.includes("localStorage está cheio"))
      ) {
        titulo = "⚠️ Armazenamento Local Cheio";
        descricao =
          "O navegador não tem mais espaço para armazenar dados.\n\n" +
          "Soluções:\n" +
          "1. Exclua produtos antigos ou suas imagens\n" +
          "2. Limpe o localStorage do navegador:\n" +
          "   - Pressione F12 → Console\n" +
          "   - Digite: localStorage.clear()\n" +
          "   - Pressione Enter\n" +
          "3. Use um backend para armazenar imagens\n\n" +
          "Nota: As imagens foram comprimidas automaticamente, mas o espaço ainda é insuficiente.";
      } else if (err.message) {
        descricao = err.message;
      }

      showNotification(titulo, descricao, "error", 8000);
    })
    .finally(() => {
      loading.value = false;
    });
}

function onEdit(p) {
  editId.value = p.id;
  editForm.value = {
    nome: p.nome,
    preco: Number(p.preco),
    estoque: p.estoque,
    categoria: p.categoria || "",
    descricao: p.descricao || "",
  };
  editImagesFiles.value = [];
  editImagesPreview.value = [];
}

function onCancel() {
  editId.value = null;
}

function onSave(id) {
  loading.value = true;
  updateProduto(id, { ...editForm.value })
    .then((response) => {
      if (editImagesFiles.value.length > 0) {
        const uploadPromises = editImagesFiles.value.map((file) =>
          uploadImagemProduto(id, file)
        );
        return Promise.all(uploadPromises);
      }
      return Promise.resolve();
    })
    .then(() => {
      editId.value = null;
      showNotification(
        "Produto atualizado",
        "As alterações foram salvas com sucesso!",
        "success"
      );
      return fetchProdutos();
    })
    .catch((err) => {
      console.error("Erro ao atualizar produto:", err);
      let titulo = "Erro ao atualizar produto";
      let descricao = "Verifique os dados e tente novamente.";

      if (
        err.message &&
        (err.message.includes("QuotaExceededError") ||
          err.message.includes("Quota") ||
          err.message.includes("localStorage está cheio"))
      ) {
        titulo = "⚠️ Armazenamento Local Cheio";
        descricao =
          "O navegador não tem mais espaço para armazenar dados.\n\n" +
          "Soluções:\n" +
          "1. Exclua produtos antigos ou suas imagens\n" +
          "2. Limpe o localStorage do navegador:\n" +
          "   - Pressione F12 → Console\n" +
          "   - Digite: localStorage.clear()\n" +
          "   - Pressione Enter\n" +
          "3. Use um backend para armazenar imagens\n\n" +
          "Nota: Os dados do produto foram salvos, mas as imagens podem não ter sido adicionadas.";
      } else if (err.message) {
        descricao = err.message;
      }

      showNotification(titulo, descricao, "error", 8000);
    })
    .finally(() => {
      loading.value = false;
    });
}

function onDelete(id) {
  if (!confirm("Tem certeza que deseja excluir este produto?")) return;
  deleteProdutoById(id)
    .then(() => {
      fetchProdutos();
      showNotification(
        "Produto excluído",
        "O produto foi removido com sucesso.",
        "success"
      );
    })
    .catch((err) => {
      console.error("Erro ao excluir produto:", err);
      showNotification(
        "Erro ao excluir produto",
        "Ocorreu um erro ao tentar excluir o produto. Tente novamente.",
        "error"
      );
    });
}

onMounted(() => {
  fetchProdutos();
});
</script>

<style scoped>
@keyframes fade-in-up {
  from {
    opacity: 0;
    transform: translateY(30px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.animate-fade-in-up {
  animation: fade-in-up 0.8s ease-out forwards;
}

@keyframes pulse-soft {
  0%,
  100% {
    opacity: 1;
  }
  50% {
    opacity: 0.7;
  }
}

.animate-pulse {
  animation: pulse-soft 2s ease-in-out infinite;
}

.overflow-x-auto::-webkit-scrollbar {
  height: 8px;
}

.overflow-x-auto::-webkit-scrollbar-track {
  background: #ede5dd;
  border-radius: 10px;
}

.overflow-x-auto::-webkit-scrollbar-thumb {
  background: #b9a994;
  border-radius: 10px;
}

.overflow-x-auto::-webkit-scrollbar-thumb:hover {
  background: #735e59;
  cursor: pointer;
}

@media (max-width: 768px) {
  input[type="file"] {
    font-size: 16px !important;
  }

  .overflow-x-auto {
    -webkit-overflow-scrolling: touch;
    scroll-snap-type: x proximity;
  }

  button {
    -webkit-tap-highlight-color: rgba(115, 94, 89, 0.2);
  }

  button,
  input,
  textarea {
    -webkit-user-select: none;
    user-select: none;
  }

  input[type="text"],
  input[type="number"],
  textarea {
    -webkit-user-select: text;
    user-select: text;
  }
}

.touch-manipulation {
  touch-action: manipulation;
  -webkit-tap-highlight-color: transparent;
}

@media (max-width: 768px) {
  .flex.flex-wrap.gap-3 img,
  .flex.flex-wrap.gap-4 img {
    scroll-snap-align: start;
  }
}
</style>
