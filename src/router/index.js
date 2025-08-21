import { createRouter, createWebHistory } from "vue-router";

import Home from "../views/Home.vue";
import TrocasDevolucoes from "../views/TrocasDevolucoes.vue";
import Cuidados from "../views/Cuidados.vue";
import Produtos from "../views/Produtos.vue";
import Entrega from "../views/Entrega.vue";
import Pagamento from "../views/Pagamento.vue";
import CadastrarProdutos from "../views/CadastrarProdutos.vue";

const routes = [
  { path: "/", component: Home },
  {
    path: "/trocas-devolucoes",
    component: TrocasDevolucoes,
  },
  {
    path: "/cuidados",
    component: Cuidados,
  },
  {
    path: "/produtos",
    component: Produtos,
  },
  {
    path: "/entrega",
    component: Entrega,
  },
  {
    path: "/pagamento",
    component: Pagamento,
  },
  {
    path: "/cadastrar-produtos",
    component: CadastrarProdutos,
  },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;
