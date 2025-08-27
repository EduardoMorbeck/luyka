import axios from "axios";

export const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL || "http://localhost:8000",
});

export function getProdutos(params) {
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

export function uploadImagemProduto(id, file) {
  const fd = new FormData();
  fd.append("arquivo", file);

  return api
    .post(`/produtos/${id}/imagem`, fd, {
      headers: { "Content-Type": "multipart/form-data" },
    })
    .then((r) => r.data);
}
