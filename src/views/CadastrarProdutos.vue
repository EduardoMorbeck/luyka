<template>
  <div class="w-full flex flex-col py-28 gap-8 max-w-3xl mx-auto">
    <h1 class="font-bold text-center text-3xl mb-2">CADASTRAR PRODUTOS</h1>

    <!-- Form criar -->
    <form
      class="grid grid-cols-1 md:grid-cols-5 gap-2 items-end"
      @submit.prevent="onCreate"
    >
      <div class="md:col-span-2">
        <label class="block text-sm mb-1">Nome</label>
        <input
          v-model="createForm.nome"
          class="w-full border rounded p-2"
          required
        />
      </div>
      <div>
        <label class="block text-sm mb-1">Preço</label>
        <input
          v-model.number="createForm.preco"
          type="number"
          step="0.01"
          min="0"
          class="w-full border rounded p-2"
          required
        />
      </div>
      <div>
        <label class="block text-sm mb-1">Estoque</label>
        <input
          v-model.number="createForm.estoque"
          type="number"
          min="0"
          class="w-full border rounded p-2"
          required
        />
      </div>
      <div>
        <label class="block text-sm mb-1">Categoria</label>
        <input
          v-model="createForm.categoria"
          class="w-full border rounded p-2"
        />
      </div>
      <div class="md:col-span-5">
        <label class="block text-sm mb-1">Descrição</label>
        <textarea
          v-model="createForm.descricao"
          rows="2"
          class="w-full border rounded p-2"
        ></textarea>
      </div>
      <div class="md:col-span-5 flex justify-end">
        <button
          :disabled="loading"
          class="px-4 py-2 rounded bg-black text-white"
        >
          {{ loading ? "Salvando..." : "Adicionar" }}
        </button>
      </div>
    </form>

    <hr class="my-4" />

    <!-- Lista -->
    <ul v-if="produtos.length > 0" class="divide-y">
      <li v-for="p in produtos" :key="p.id" class="py-4">
        <!-- Modo edição -->
        <div
          v-if="editId === p.id"
          class="grid grid-cols-1 md:grid-cols-6 gap-2"
        >
          <input
            v-model="editForm.nome"
            class="border rounded p-2 md:col-span-2"
          />
          <input
            v-model.number="editForm.preco"
            type="number"
            step="0.01"
            min="0"
            class="border rounded p-2"
          />
          <input
            v-model.number="editForm.estoque"
            type="number"
            min="0"
            class="border rounded p-2"
          />
          <input v-model="editForm.categoria" class="border rounded p-2" />
          <div class="md:col-span-6">
            <textarea
              v-model="editForm.descricao"
              rows="2"
              class="w-full border rounded p-2"
            ></textarea>
          </div>
          <div class="flex gap-2 md:col-span-6 justify-end">
            <button
              @click="onSave(p.id)"
              :disabled="loading"
              class="px-3 py-2 rounded bg-emerald-600 text-white"
            >
              {{ loading ? "Salvando..." : "Salvar" }}
            </button>
            <button @click="onCancel()" class="px-3 py-2 rounded border">
              Cancelar
            </button>
          </div>
        </div>

        <!-- Modo leitura -->
        <div v-else class="flex items-start justify-between gap-4">
          <div>
            <div class="font-semibold">{{ p.nome }}</div>
            <div class="text-sm text-gray-600">
              R$ {{ Number(p.preco).toFixed(2) }} • {{ p.estoque }} unid. •
              {{ p.categoria || "sem categoria" }}
            </div>
            <div class="text-sm mt-1 text-gray-700" v-if="p.descricao">
              {{ p.descricao }}
            </div>
          </div>
          <div class="shrink-0 flex gap-2">
            <button @click="onEdit(p)" class="px-3 py-2 rounded border">
              Editar
            </button>
            <button
              @click="onDelete(p.id)"
              class="px-3 py-2 rounded bg-red-600 text-white"
            >
              Excluir
            </button>
          </div>
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

// edição
const editId = ref(null);
const editForm = ref({
  nome: "",
  preco: 0,
  estoque: 0,
  categoria: "",
  descricao: "",
});

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
    .then(() => {
      // limpa form e recarrega
      createForm.value = {
        nome: "",
        preco: 0,
        estoque: 0,
        categoria: "",
        descricao: "",
      };
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
}

function onCancel() {
  editId.value = null;
}

function onSave(id) {
  loading.value = true;
  updateProduto(id, { ...editForm.value })
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
