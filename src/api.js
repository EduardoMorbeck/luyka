import axios from "axios";
import {
  getProdutosFromStorage,
  createProdutoInStorage,
  updateProdutoInStorage,
  deleteProdutoFromStorage,
  deleteImagemFromStorage,
  addImagemToProduto,
} from "./utils/localStorageProducts";

export const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL || "http://localhost:8000",
});

export function calcularFrete(data) {
  return api.post("/frete/", data).then((r) => r.data);
}

export function getProdutos(params) {
  return Promise.resolve(getProdutosFromStorage(params));
}

export function createProduto(data) {
  return createProdutoInStorage(data, []);
}

export function updateProduto(id, data) {
  return updateProdutoInStorage(id, data, []);
}

export function deleteProdutoById(id) {
  deleteProdutoFromStorage(id);
  return Promise.resolve();
}

export function uploadImagemProduto(id, file) {
  return addImagemToProduto(id, file);
}

export function deleteImagemProduto(id, imagemIndex) {
  deleteImagemFromStorage(id, imagemIndex);
  return Promise.resolve({ success: true });
}

export function getImagensProduto(id) {
  const produtos = getProdutosFromStorage();
  const produto = produtos.find((p) => p.id === id);
  return Promise.resolve(produto?.imagens_url || []);
}

export function gerarPix(data) {
  return api.post("/pagamento/gerar-pix", data).then((r) => r.data);
}
