const STORAGE_KEY = "luyka_produtos";
const NEXT_ID_KEY = "luyka_produtos_next_id";
const MAX_IMAGE_SIZE = 800;
const MAX_IMAGE_QUALITY = 0.7;
const MAX_BASE64_SIZE = 500 * 1024;

function compressImage(
  file,
  maxWidth = MAX_IMAGE_SIZE,
  quality = MAX_IMAGE_QUALITY
) {
  return new Promise((resolve, reject) => {
    const reader = new FileReader();
    reader.onload = (e) => {
      const img = new Image();
      img.onload = () => {
        const canvas = document.createElement("canvas");
        let width = img.width;
        let height = img.height;

        if (width > maxWidth) {
          height = (height * maxWidth) / width;
          width = maxWidth;
        }

        canvas.width = width;
        canvas.height = height;

        const ctx = canvas.getContext("2d");
        ctx.drawImage(img, 0, 0, width, height);

        canvas.toBlob(
          (blob) => {
            if (!blob) {
              reject(new Error("Erro ao comprimir imagem"));
              return;
            }

            if (blob.size > MAX_BASE64_SIZE) {
              canvas.toBlob(
                (smallerBlob) => {
                  if (!smallerBlob) {
                    reject(new Error("Erro ao comprimir imagem"));
                    return;
                  }
                  const reader2 = new FileReader();
                  reader2.onload = () => resolve(reader2.result);
                  reader2.onerror = reject;
                  reader2.readAsDataURL(smallerBlob);
                },
                "image/png",
                0.5
              );
            } else {
              const reader2 = new FileReader();
              reader2.onload = () => resolve(reader2.result);
              reader2.onerror = reject;
              reader2.readAsDataURL(blob);
            }
          },
          "image/png",
          quality
        );
      };
      img.onerror = reject;
      img.src = e.target.result;
    };
    reader.onerror = reject;
    reader.readAsDataURL(file);
  });
}

export function fileToBase64(file) {
  if (file.type.startsWith("image/")) {
    return compressImage(file);
  }
  return new Promise((resolve, reject) => {
    const reader = new FileReader();
    reader.onload = () => resolve(reader.result);
    reader.onerror = reject;
    reader.readAsDataURL(file);
  });
}

function getNextId() {
  const nextId = localStorage.getItem(NEXT_ID_KEY);
  const id = nextId ? parseInt(nextId, 10) : 1;
  localStorage.setItem(NEXT_ID_KEY, (id + 1).toString());
  return id;
}

function getAllProducts() {
  try {
    const data = localStorage.getItem(STORAGE_KEY);
    return data ? JSON.parse(data) : [];
  } catch (error) {
    console.error("Erro ao ler produtos do localStorage:", error);
    return [];
  }
}

function saveAllProducts(produtos) {
  try {
    const data = JSON.stringify(produtos);
    localStorage.setItem(STORAGE_KEY, data);
  } catch (error) {
    if (error.name === "QuotaExceededError" || error.message?.includes("Quota")) {
      console.warn(
        "Quota do localStorage excedida. Tentando limpar dados antigos..."
      );

      const produtosOrdenados = [...produtos].sort(
        (a, b) =>
          new Date(b.atualizado_em || b.criado_em || 0) -
          new Date(a.atualizado_em || a.criado_em || 0)
      );

      const produtosLimpos = produtosOrdenados.map((p, index) => {
        if (index >= 15) {
          return {
            ...p,
            imagens_url: [],
            imagem_url: null,
          };
        } else if (p.imagens_url && p.imagens_url.length > 1) {
          return {
            ...p,
            imagens_url: [p.imagens_url[0]],
            imagem_url: p.imagens_url[0],
          };
        }
        return p;
      });

      try {
        const dataLimpo = JSON.stringify(produtosLimpos);
        localStorage.setItem(STORAGE_KEY, dataLimpo);
        console.log("Dados limpos salvos com sucesso (estratégia 1)");
        return;
      } catch (retryError) {
        const produtosSemImagens = produtos.map((p) => ({
          ...p,
          imagens_url: [],
          imagem_url: null,
        }));

        try {
          const dataSemImagens = JSON.stringify(produtosSemImagens);
          localStorage.setItem(STORAGE_KEY, dataSemImagens);
          console.log("Dados limpos salvos sem imagens (estratégia 2)");
          throw new Error(
            "Quota do localStorage excedida. As imagens foram removidas automaticamente para liberar espaço. " +
              "Por favor, use um backend para armazenar imagens ou limpe o localStorage manualmente."
          );
        } catch (finalError) {
          let produtosReduzidos = [...produtosOrdenados];
          while (produtosReduzidos.length > 0) {
            try {
              const dataReduzida = JSON.stringify(produtosReduzidos);
              localStorage.setItem(STORAGE_KEY, dataReduzida);
              console.log(`Dados salvos após remover ${produtos.length - produtosReduzidos.length} produtos antigos`);
              throw new Error(
                `O localStorage estava cheio. ${produtos.length - produtosReduzidos.length} produto(s) antigo(s) foram removido(s) automaticamente. ` +
                  "Por favor, use um backend para armazenar dados ou limpe o localStorage manualmente."
              );
            } catch (testError) {
              if (testError.message && !testError.message.includes("O localStorage")) {
                produtosReduzidos = produtosReduzidos.slice(0, -1);
              } else {
                throw testError;
              }
            }
          }

          throw new Error(
            "Não foi possível salvar os dados. O localStorage está completamente cheio. " +
              "Por favor, limpe o localStorage do navegador (F12 → Console → localStorage.clear()) " +
              "ou use um backend para armazenar os dados."
          );
        }
      }
    }
    console.error("Erro ao salvar produtos no localStorage:", error);
    throw error;
  }
}

export function getProdutosFromStorage(params = {}) {
  let produtos = getAllProducts();

  if (params.q) {
    const query = params.q.toLowerCase().trim();
    produtos = produtos.filter(
      (p) =>
        p.nome?.toLowerCase().includes(query) ||
        p.categoria?.toLowerCase().includes(query)
    );
  }

  produtos.sort((a, b) => (b.id || 0) - (a.id || 0));

  if (params.cursor_id) {
    produtos = produtos.filter((p) => (p.id || 0) < params.cursor_id);
  }

  const limit = params.limit || 50;
  produtos = produtos.slice(0, limit);

  return produtos;
}

export async function createProdutoInStorage(data, imageFiles = []) {
  const produtos = getAllProducts();
  const id = getNextId();
  const now = new Date().toISOString();

  const imagensUrl = [];
  for (const file of imageFiles) {
    const base64 = await fileToBase64(file);
    imagensUrl.push(base64);
  }

  const novoProduto = {
    id,
    nome: data.nome || "",
    descricao: data.descricao || "",
    preco: Number(data.preco) || 0,
    estoque: Number(data.estoque) || 0,
    categoria: data.categoria || "",
    imagens_url: imagensUrl,
    imagem_url: imagensUrl[0] || null,
    criado_em: now,
    atualizado_em: now,
  };

  produtos.push(novoProduto);
  saveAllProducts(produtos);

  return novoProduto;
}

export async function updateProdutoInStorage(id, data, newImageFiles = []) {
  const produtos = getAllProducts();
  const index = produtos.findIndex((p) => p.id === id);

  if (index === -1) {
    throw new Error(`Produto com id ${id} não encontrado`);
  }

  const produto = produtos[index];
  const now = new Date().toISOString();

  const novasImagens = [];
  for (const file of newImageFiles) {
    const base64 = await fileToBase64(file);
    novasImagens.push(base64);
  }

  produtos[index] = {
    ...produto,
    nome: data.nome !== undefined ? data.nome : produto.nome,
    descricao:
      data.descricao !== undefined ? data.descricao : produto.descricao,
    preco: data.preco !== undefined ? Number(data.preco) : produto.preco,
    estoque:
      data.estoque !== undefined ? Number(data.estoque) : produto.estoque,
    categoria:
      data.categoria !== undefined ? data.categoria : produto.categoria,
    imagens_url: [...(produto.imagens_url || []), ...novasImagens],
    imagem_url: produto.imagens_url?.[0] || novasImagens[0] || null,
    atualizado_em: now,
  };

  saveAllProducts(produtos);
  return produtos[index];
}

export async function addImagemToProduto(id, file) {
  const produtos = getAllProducts();
  const index = produtos.findIndex((p) => p.id === id);

  if (index === -1) {
    throw new Error(`Produto com id ${id} não encontrado`);
  }

  const produto = produtos[index];
  const base64 = await fileToBase64(file);
  const imagensUrl = [...(produto.imagens_url || []), base64];
  const now = new Date().toISOString();

  produtos[index] = {
    ...produto,
    imagens_url: imagensUrl,
    imagem_url: imagensUrl[0] || null,
    atualizado_em: now,
  };

  saveAllProducts(produtos);
  return produtos[index];
}

export function deleteProdutoFromStorage(id) {
  const produtos = getAllProducts();
  const filtered = produtos.filter((p) => p.id !== id);
  saveAllProducts(filtered);
}

export function deleteImagemFromStorage(produtoId, imagemIndex) {
  const produtos = getAllProducts();
  const index = produtos.findIndex((p) => p.id === produtoId);

  if (index === -1) {
    throw new Error(`Produto com id ${produtoId} não encontrado`);
  }

  const produto = produtos[index];
  const imagensUrl = [...(produto.imagens_url || [])];

  if (imagemIndex < 0 || imagemIndex >= imagensUrl.length) {
    throw new Error(`Índice de imagem inválido: ${imagemIndex}`);
  }

  imagensUrl.splice(imagemIndex, 1);

  produtos[index] = {
    ...produto,
    imagens_url: imagensUrl,
    imagem_url: imagensUrl[0] || null,
    atualizado_em: new Date().toISOString(),
  };

  saveAllProducts(produtos);
  return produtos[index];
}
