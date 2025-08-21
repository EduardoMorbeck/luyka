import axios from "axios";

export const api = axios.create({
  baseURL: "http://localhost:8000",
});

export function getProdutos() {
  return api.get("/produtos/").then((r) => r.data);
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
