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
        <label class="block text-sm font-medium mb-1">Imagem</label>
        <input
          type="file"
          accept="image/*"
          class="w-full border rounded p-3 cursor-pointer hover:bg-gray-100 transition"
          @change="onCreateImageChange"
        />
        <div v-if="createImagePreview" class="mt-3">
          <img
            :src="createImagePreview"
            class="h-96 w-96 object-cover rounded-lg border shadow"
            alt="Preview da imagem"
          />
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
            <label class="block text-sm font-medium mb-1">Imagem</label>
            <input
              type="file"
              accept="image/*"
              class="w-full border rounded p-3 cursor-pointer hover:bg-gray-100 transition"
              @change="onEditImageChange"
            />
            <div v-if="editImagePreview || p.imagem_url" class="mt-3">
              <img
                :src="editImagePreview || thumb(p.imagem_url)"
                class="h-96 w-96 object-cover rounded-lg border shadow"
                alt="Preview da imagem"
              />
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
          <img
            v-if="p.imagem_url"
            :src="thumb(p.imagem_url)"
            class="h-96 w-96 rounded-lg object-cover border shadow"
            alt="Imagem do produto"
          />
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
const createImageFile = ref(null);
const createImagePreview = ref(null);

// edição
const editId = ref(null);
const editForm = ref({
  nome: "",
  preco: 0,
  estoque: 0,
  categoria: "",
  descricao: "",
});
const editImageFile = ref(null);
const editImagePreview = ref(null);

// previews
function readPreview(file, targetRef) {
  if (!file) {
    targetRef.value = null;
    return;
  }
  const reader = new FileReader();
  reader.onload = (e) => {
    targetRef.value = e.target.result;
  };
  reader.readAsDataURL(file);
}

// cria: change handler
function onCreateImageChange(e) {
  const file = e.target.files?.[0] || null;
  createImageFile.value = file;
  readPreview(file, createImagePreview);
}

// edita: change handler
function onEditImageChange(e) {
  const file = e.target.files?.[0] || null;
  editImageFile.value = file;
  readPreview(file, editImagePreview);
}

// thumbnail helper (Supabase Image Transformations)
function thumb(url) {
  if (!url) return "";
  const sep = url.includes("?") ? "&" : "?";
  return `${url}${sep}width=160&height=160&resize=cover&quality=80`;
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
      if (createImageFile.value) {
        uploadImagemProduto(response.id, createImageFile.value);
      }

      createForm.value = {
        nome: "",
        preco: 0,
        estoque: 0,
        categoria: "",
        descricao: "",
      };

      createImageFile.value = null;
      createImagePreview.value = null;

      return fetchProdutos();
    })
    .catch((err) => console.error("Erro ao criar produto:", err))
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
  editImageFile.value = null;
  editImagePreview.value = null;
}

function onCancel() {
  editId.value = null;
}

function onSave(id) {
  loading.value = true;
  updateProduto(id, { ...editForm.value })
    .then((response) => {
      if (editImageFile.value) {
        uploadImagemProduto(id, editImageFile.value);
      }
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
