# Luyka

Loja virtual em formato single-page application (SPA) com frontend em Vue 3 e backend em FastAPI. Inclui catálogo de produtos, cadastro de produtos (com upload de imagens), informações de entrega, pagamento via PIX e páginas institucionais (cuidados, trocas e devoluções).

## Tecnologias

### Frontend

- **Vue 3** (Composition API / `<script setup>`)
- **Vite 7**
- **Vue Router**
- **Tailwind CSS 4**
- **Axios**

### Backend

- **FastAPI**
- **SQLAlchemy** + **PostgreSQL** (Supabase)
- **Supabase** (banco de dados e armazenamento de imagens)
- **JWT** (autenticação para área administrativa)
- **PIX** (geração de QR Code via `python-brcode` / `qrcode`)

## Estrutura do projeto

```
luyka/
├── src/                    # Frontend Vue
│   ├── api.js              # Cliente HTTP e funções de API
│   ├── components/         # Componentes reutilizáveis
│   ├── views/              # Páginas (rotas)
│   ├── router/             # Configuração do Vue Router
│   ├── store/              # Estado (ex.: carrinho)
│   └── utils/              # Utilitários (ex.: produtos em localStorage)
├── backend/
│   └── app/
│       ├── main.py         # App FastAPI e CORS
│       ├── routers/        # auth, products, frete, pagamento
│       ├── middleware/     # rate limit
│       ├── services/       # upload de imagens (Supabase Storage)
│       ├── db.py           # Conexão SQLAlchemy
│       ├── models.py       # Modelo Produto
│       ├── schemas.py      # Schemas Pydantic
│       └── auth.py         # JWT e hash de senha
├── requirements.txt       # Dependências Python
└── package.json           # Dependências Node
```

## Pré-requisitos

- **Node.js** (recomendado LTS) e **npm**
- **Python 3.10+**
- Conta no **Supabase** (banco PostgreSQL e Storage para imagens)

## Configuração

### 1. Clone e dependências

```bash
git clone https://github.com/SEU_USUARIO/luyka.git
cd luyka
npm install
```

### 2. Variáveis de ambiente

Na raiz do projeto, crie um arquivo `.env` (não versionado) com:

**Backend (obrigatórias para API e banco):**

| Variável                    | Descrição                                                         |
| --------------------------- | ----------------------------------------------------------------- |
| `SUPABASE_URL`              | URL do projeto Supabase                                           |
| `SUPABASE_ANON_KEY`         | Chave anônima (ou service role, conforme uso)                     |
| `SUPABASE_SERVICE_ROLE_KEY` | Chave service role (para operações privilegiadas)                 |
| `SUPABASE_DB_URL`           | URL de conexão PostgreSQL (ex.: `postgresql+psycopg://...`)       |
| `SUPABASE_BUCKET`           | Nome do bucket para imagens dos produtos (ex.: `produtos-images`) |
| `SUPABASE_PUBLIC`           | `true` ou `false` se o bucket é público                           |
| `ALLOWED_ORIGINS`           | Origens CORS separadas por vírgula (ex.: `http://localhost:5173`) |

**Autenticação (admin):**  
O login da área “Cadastrar Produtos” usa usuário e senha definidos por variáveis de ambiente no backend (ver `backend/app/auth.py`). Configure-as conforme a implementação (ex.: `ADMIN_USERNAME`, `ADMIN_PASSWORD_HASH`).

**Frontend (opcional):**

| Variável       | Descrição                                        |
| -------------- | ------------------------------------------------ |
| `VITE_API_URL` | URL da API (ex.: `http://localhost:8000` em dev) |

Se não definir `VITE_API_URL`, o frontend usa `http://localhost:8000`.

### 3. Backend (Python)

```bash
cd backend
python -m venv venv
# Windows:
venv\Scripts\activate
# Linux/macOS:
# source venv/bin/activate
pip install -r ../requirements.txt
cd ..
uvicorn backend.app.main:app --reload
```

A API ficará em `http://localhost:8000`. Documentação interativa: `http://localhost:8000/docs`.

### 4. Frontend (Vue)

Em outro terminal, na raiz do projeto:

```bash
npm run dev
```

O site ficará em `http://localhost:5173`.

### 5. Rodar frontend e backend juntos

```bash
npm run fullstack
```

Usa `concurrently` para subir `npm run dev` e `npm run backend` ao mesmo tempo.

## Scripts disponíveis

| Comando             | Descrição                                      |
| ------------------- | ---------------------------------------------- |
| `npm run dev`       | Sobe o frontend (Vite) em modo desenvolvimento |
| `npm run build`     | Build de produção do frontend                  |
| `npm run preview`   | Preview do build de produção                   |
| `npm run backend`   | Sobe a API FastAPI com uvicorn em modo reload  |
| `npm run fullstack` | Sobe frontend e backend em paralelo            |

## Funcionalidades principais

- **Home:** hero, benefícios, categorias e listagem de produtos.
- **Produtos:** listagem, busca/filtro e detalhes.
- **Cadastrar Produtos:** tela protegida por login para criar/editar produtos e enviar imagens (Supabase Storage).
- **Entrega:** informações de frete e prazos (API de frete no backend).
- **Pagamento:** geração de PIX (QR Code) via backend.
- **Cuidados** e **Trocas e Devoluções:** páginas institucionais.
- **Carrinho:** gerenciado no frontend (store + localStorage quando aplicável).

## Banco de dados

O backend usa **PostgreSQL** no Supabase. O modelo principal é `Produto` (nome, descrição, preço, estoque, categoria, imagens). As migrações ou criação das tabelas devem ser feitas no Supabase (SQL ou ferramentas do projeto) conforme os modelos em `backend/app/models.py`.

## Link para acessar o site hospedado no onrender

https://luyka.onrender.com/
