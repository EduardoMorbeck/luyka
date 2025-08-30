<template>
  <div class="w-full flex flex-col py-28 gap-10 max-w-4xl mx-auto">
    <h1 class="font-bold text-center text-4xl mb-4 tracking-wide">
      Cadastrar Produtos
    </h1>

    <!-- Form criar -->
    <form
      class="grid grid-cols-1 md:grid-cols-5 gap-4 bg-white shadow rounded-lg p-6"
      @submit.prevent="onCreate"
    >
      <div class="md:col-span-5">
        <label class="block text-sm font-medium mb-1">
          Imagens
          <span
            v-if="createImagesPreview.length > 0"
            class="text-sm text-gray-500 font-normal"
          >
            ({{ createImagesPreview.length }} selecionada{{
              createImagesPreview.length > 1 ? "s" : ""
            }})
          </span>
        </label>
        <div class="flex gap-3">
          <input
            type="file"
            accept="image/*"
            multiple
            class="flex-1 hidden border rounded p-3 cursor-pointer hover:bg-gray-100 transition"
            @change="onCreateImagesChange"
          />
          <button
            type="button"
            @click="addMoreImages"
            class="w-full px-4 py-3 border border-gray-300 rounded hover:bg-gray-50 transition text-sm font-medium"
          >
            + Adicionar Imagem
          </button>
        </div>
        <div
          v-if="createImagesPreview.length > 0"
          class="mt-3 flex flex-wrap gap-3"
        >
          <div
            v-for="(preview, index) in createImagesPreview"
            :key="index"
            class="relative group"
          >
            <img
              :src="preview"
              class="h-80 w-80 rounded-lg object-cover border shadow flex-shrink-0"
              alt="Preview da imagem"
            />
            <button
              type="button"
              @click="removeCreateImage(index)"
              class="absolute top-1 right-1 bg-red-500 text-white rounded-full w-6 h-6 flex items-center justify-center opacity-0 group-hover:opacity-100 transition-opacity"
            >
              ×
            </button>
          </div>
        </div>
      </div>

      <div class="md:col-span-2">
        <label class="block text-sm font-medium mb-1">Nome</label>
        <input
          v-model="createForm.nome"
          class="w-full border rounded p-3"
          required
        />
      </div>
      <div>
        <label class="block text-sm font-medium mb-1">Preço</label>
        <input
          v-model.number="createForm.preco"
          type="number"
          step="0.01"
          min="0"
          class="w-full border rounded p-3"
          required
        />
      </div>
      <div>
        <label class="block text-sm font-medium mb-1">Estoque</label>
        <input
          v-model.number="createForm.estoque"
          type="number"
          min="0"
          class="w-full border rounded p-3"
          required
        />
      </div>
      <div>
        <label class="block text-sm font-medium mb-1">Categoria</label>
        <input
          v-model="createForm.categoria"
          class="w-full border rounded p-3"
        />
      </div>
      <div class="md:col-span-5">
        <label class="block text-sm font-medium mb-1">Descrição</label>
        <textarea
          v-model="createForm.descricao"
          rows="3"
          class="w-full border rounded p-3"
        ></textarea>
      </div>
      <div class="md:col-span-5 flex justify-end">
        <button
          :disabled="loading"
          class="cursor-pointer px-6 py-3 rounded bg-black text-white font-medium hover:bg-gray-800 transition"
        >
          {{ loading ? "Salvando..." : "Adicionar" }}
        </button>
      </div>
    </form>

    <!-- Lista -->
    <ul v-if="produtos.length > 0" class="grid gap-6">
      <li
        v-for="p in produtos"
        :key="p.id"
        class="bg-white rounded-lg shadow p-6 flex justify-between items-start gap-6"
      >
        <!-- Modo edição (igual ao layout de criação) -->
        <div
          v-if="editId === p.id"
          class="grid grid-cols-1 md:grid-cols-5 gap-4 bg-white shadow rounded-lg p-6 items-end"
        >
          <div class="md:col-span-5">
            <label class="block text-sm font-medium mb-1">
              Imagens
              <span
                v-if="editImagesPreview.length > 0"
                class="text-sm text-gray-500 font-normal"
              >
                ({{ editImagesPreview.length }} nova{{
                  editImagesPreview.length > 1 ? "s" : ""
                }})
              </span>
            </label>
            <div class="flex gap-3">
              <input
                type="file"
                accept="image/*"
                multiple
                class="flex-1 border rounded p-3 cursor-pointer hover:bg-gray-100 transition"
                @change="onEditImagesChange"
              />
              <!-- <button
                type="button"
                @click="addMoreImagesEdit"
                class="px-4 py-3 border border-gray-300 rounded hover:bg-gray-50 transition text-sm font-medium"
              >
                + Adicionar Mais
              </button> -->
            </div>
            <!-- Preview das imagens existentes -->
            <div v-if="getImagensUrls(p).length > 0" class="mt-3">
              <p class="text-sm text-gray-600 mb-2">Imagens existentes:</p>
              <div class="flex flex-wrap gap-3 mb-3">
                <div
                  v-for="(url, index) in getImagensUrls(p)"
                  :key="index"
                  class="relative group"
                >
                  <img
                    :src="url"
                    class="h-80 w-80 rounded-lg object-cover border shadow flex-shrink-0"
                    alt="Imagem existente"
                  />
                  <button
                    type="button"
                    @click="deleteImagemExistente(p.id, index)"
                    class="absolute top-1 right-1 bg-red-500 text-white rounded-full w-6 h-6 flex items-center justify-center opacity-0 group-hover:opacity-100 transition-opacity"
                  >
                    ×
                  </button>
                </div>
              </div>
            </div>
            <!-- Preview das novas imagens -->
            <div v-if="editImagesPreview.length > 0" class="mt-3">
              <p class="text-sm text-gray-600 mb-2">Novas imagens:</p>
              <div class="flex flex-wrap gap-3">
                <div
                  v-for="(preview, index) in editImagesPreview"
                  :key="index"
                  class="relative group"
                >
                  <img
                    :src="preview"
                    class="h-80 w-80 object-cover rounded-lg border shadow"
                    alt="Preview da nova imagem"
                  />
                  <button
                    type="button"
                    @click="removeEditImage(index)"
                    class="absolute top-1 right-1 bg-red-500 text-white rounded-full w-6 h-6 flex items-center justify-center opacity-0 group-hover:opacity-100 transition-opacity"
                  >
                    ×
                  </button>
                </div>
              </div>
            </div>
          </div>

          <div class="md:col-span-2">
            <label class="block text-sm font-medium mb-1">Nome</label>
            <input
              v-model="editForm.nome"
              class="w-full border rounded p-3"
              required
            />
          </div>

          <div>
            <label class="block text-sm font-medium mb-1">Preço</label>
            <input
              v-model.number="editForm.preco"
              type="number"
              step="0.01"
              min="0"
              class="w-full border rounded p-3"
              required
            />
          </div>

          <div>
            <label class="block text-sm font-medium mb-1">Estoque</label>
            <input
              v-model.number="editForm.estoque"
              type="number"
              min="0"
              class="w-full border rounded p-3"
              required
            />
          </div>

          <div>
            <label class="block text-sm font-medium mb-1">Categoria</label>
            <input
              v-model="editForm.categoria"
              class="w-full border rounded p-3"
            />
          </div>

          <div class="md:col-span-5">
            <label class="block text-sm font-medium mb-1">Descrição</label>
            <textarea
              v-model="editForm.descricao"
              rows="3"
              class="w-full border rounded p-3"
            ></textarea>
          </div>

          <div class="md:col-span-5 flex justify-end gap-3">
            <button
              @click="onSave(p.id)"
              :disabled="loading"
              class="cursor-pointer px-6 py-3 rounded bg-black text-white font-medium hover:bg-gray-800 transition"
            >
              {{ loading ? "Salvando..." : "Salvar" }}
            </button>
            <button
              @click="onCancel()"
              class="cursor-pointer px-6 py-3 rounded border hover:bg-gray-100 transition"
            >
              Cancelar
            </button>
          </div>
        </div>

        <!-- Modo leitura -->
        <div v-else class="flex flex-1 items-start gap-6">
          <div class="flex flex-col gap-3">
            <div
              v-if="getImagensUrls(p).length > 0"
              class="flex gap-2 overflow-x-auto"
            >
              <img
                v-for="(url, index) in getImagensUrls(p)"
                :key="index"
                :src="url"
                class="h-80 w-80 rounded-lg object-cover border shadow flex-shrink-0"
                alt="Imagem do produto"
              />
            </div>
            <div
              v-else
              class="h-80 w-80 bg-gray-200 rounded-lg border flex items-center justify-center text-gray-400"
            >
              Sem imagem
            </div>
          </div>
          <div class="flex flex-col gap-2">
            <div class="font-semibold text-lg">{{ p.nome }}</div>
            <div class="text-sm text-gray-600">
              R$ {{ Number(p.preco).toFixed(2) }} • {{ p.estoque }} unid. •
              {{ p.categoria || "sem categoria" }}
            </div>
            <div class="text-sm text-gray-700" v-if="p.descricao">
              {{ p.descricao }}
            </div>
          </div>
        </div>

        <div v-if="editId !== p.id" class="shrink-0 flex flex-col gap-2">
          <button
            @click="onEdit(p)"
            class="cursor-pointer px-4 py-2 rounded border hover:bg-gray-100 transition"
          >
            Editar
          </button>
          <button
            @click="onDelete(p.id)"
            class="cursor-pointer px-4 py-2 rounded bg-red-600 text-white hover:bg-red-700 transition"
          >
            Excluir
          </button>
        </div>
      </li>
    </ul>

    <p v-else class="text-center text-gray-500">Nenhum produto encontrado.</p>
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue";
import {
  getProdutos,
  createProduto,
  updateProduto,
  deleteProdutoById,
  uploadImagemProduto,
  deleteImagemProduto,
  getImagensProduto,
} from "/src/api.js";

const produtos = ref([]);
const loading = ref(false);

// criação
const createForm = ref({
  nome: "",
  preco: 0,
  estoque: 0,
  categoria: "",
  descricao: "",
});
const createImagesFiles = ref([]);
const createImagesPreview = ref([]);

// edição
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

// previews
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

// cria: change handler
function onCreateImagesChange(e) {
  const files = e.target.files || [];
  if (files.length === 0) return;

  // Adiciona as novas imagens às existentes
  const newFiles = Array.from(files);
  createImagesFiles.value = [...createImagesFiles.value, ...newFiles];

  // Gera preview apenas para as novas imagens
  newFiles.forEach((file) => {
    const reader = new FileReader();
    reader.onload = (e) => {
      createImagesPreview.value.push(e.target.result);
    };
    reader.readAsDataURL(file);
  });

  // Limpa o input para permitir selecionar a mesma imagem novamente
  e.target.value = "";
}

// edita: change handler
function onEditImagesChange(e) {
  const files = e.target.files || [];
  if (files.length === 0) return;

  // Adiciona as novas imagens às existentes
  const newFiles = Array.from(files);
  editImagesFiles.value = [...editImagesFiles.value, ...newFiles];

  // Gera preview apenas para as novas imagens
  newFiles.forEach((file) => {
    const reader = new FileReader();
    reader.onload = (e) => {
      editImagesPreview.value.push(e.target.result);
    };
    reader.readAsDataURL(file);
  });

  // Limpa o input para permitir selecionar a mesma imagem novamente
  e.target.value = "";
}

// Função para adicionar mais imagens na criação
function addMoreImages() {
  // Simula um clique no input de arquivo de criação
  const fileInput = document.querySelector(
    'form[class*="grid"]:not([class*="items-end"]) input[type="file"]'
  );
  if (fileInput) {
    fileInput.click();
  }
}

// Função para adicionar mais imagens na edição
function addMoreImagesEdit() {
  // Simula um clique no input de arquivo de edição
  const fileInput = document.querySelector(
    'form[class*="items-end"] input[type="file"]'
  );
  if (fileInput) {
    fileInput.click();
  }
}

// Remove imagem do preview de criação
function removeCreateImage(index) {
  createImagesPreview.value.splice(index, 1);
  createImagesFiles.value.splice(index, 1);
}

// Remove imagem do preview de edição
function removeEditImage(index) {
  editImagesPreview.value.splice(index, 1);
  editImagesFiles.value.splice(index, 1);
}

// Delete imagem existente
function deleteImagemExistente(produtoId, imagemIndex) {
  if (!confirm("Tem certeza que deseja excluir esta imagem?")) return;

  deleteImagemProduto(produtoId, imagemIndex)
    .then(() => fetchProdutos())
    .catch((err) => console.error("Erro ao excluir imagem:", err));
}

// Helper para obter URLs das imagens do produto
function getImagensUrls(produto) {
  if (produto.imagens_url && produto.imagens_url.length > 0) {
    return produto.imagens_url;
  }
  // Fallback para produtos antigos que podem não ter imagens_url
  if (produto.imagem_path && produto.imagem_path.length > 0) {
    return produto.imagem_path.map((path) => thumb(path));
  }
  return [];
}

// thumbnail helper (Supabase Image Transformations)
function thumb(path) {
  if (!path) return "";
  // Como o backend já retorna as URLs completas, apenas retornamos o path
  // Esta função é mantida para compatibilidade com produtos antigos
  return path;
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
      // Upload de múltiplas imagens
      if (createImagesFiles.value.length > 0) {
        const uploadPromises = createImagesFiles.value.map((file) =>
          uploadImagemProduto(response.id, file)
        );
        return Promise.all(uploadPromises);
      }
      return Promise.resolve();
    })
    .then(() => {
      // Limpa o formulário após sucesso
      createForm.value = {
        nome: "",
        preco: 0,
        estoque: 0,
        categoria: "",
        descricao: "",
      };

      // Limpa as imagens selecionadas
      createImagesFiles.value = [];
      createImagesPreview.value = [];

      // Recarrega a lista de produtos
      return fetchProdutos();
    })
    .catch((err) => {
      console.error("Erro ao criar produto:", err);
      alert("Erro ao criar produto. Verifique os dados e tente novamente.");
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
      // Upload de múltiplas imagens
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
      return fetchProdutos();
    })
    .catch((err) => console.error("Erro ao atualizar produto:", err))
    .finally(() => {
      loading.value = false;
    });
}

function onDelete(id) {
  if (!confirm("Tem certeza que deseja excluir este produto?")) return;
  deleteProdutoById(id)
    .then(() => fetchProdutos())
    .catch((err) => console.error("Erro ao excluir produto:", err));
}

onMounted(() => {
  fetchProdutos();
});
</script>
