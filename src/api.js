import axios from "axios";

const baseURL = import.meta.env.PROD
  ? "/api" // prod: usa o mesmo domínio
  : import.meta.env.VITE_API_URL || "/api"; // dev: proxy do Vite resolve

export const api = axios.create({ baseURL, withCredentials: true });

// -------- Produtos (CRUD) --------
export function getProdutos(params) {
  // suporta paginação/filtro se quiser: { q, limit, offset }
  return api.get("/produtos/", { params }).then((r) => r.data);
}

export function createProduto(data) {
  return api.post("/produtos/", data).then((r) => r.data);
}

export function updateProduto(id, data) {
  return api.put(`/produtos/${id}`, data).then((r) => r.data);
}

export function deleteProdutoById(id) {
  return api.delete(`/produtos/${id}`);
}

// -------- Imagens --------
// Envia a imagem do produto via multipart/form-data
export function uploadImagemProduto(id, file) {
  const fd = new FormData();
  fd.append("arquivo", file); // o nome do campo precisa ser "arquivo" (igual no FastAPI)

  return api
    .post(`/produtos/${id}/imagem`, fd, {
      headers: { "Content-Type": "multipart/form-data" },
    })
    .then((r) => r.data); // retorna ProdutoOut já com imagem_url atualizada
}
