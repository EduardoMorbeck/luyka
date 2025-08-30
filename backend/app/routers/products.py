from fastapi import APIRouter, Depends, HTTPException, Query, UploadFile, File
from sqlalchemy.orm import Session
from typing import List, Optional
from pydantic import TypeAdapter
from ..db import get_db
from .. import models, schemas
from ..services.images import upload_image, signed_url, delete_image
import json

router = APIRouter(prefix="/produtos", tags=["Produtos"])

@router.get("/", response_model=List[schemas.ProdutoOut])
def list_produtos(
    q: Optional[str] = Query(None, description="Busca por nome/categoria"),
    limit: int = Query(50, ge=1, le=200),
    cursor_id: Optional[int] = Query(None),
    db: Session = Depends(get_db),
):
    query = db.query(models.Produto)

    if q:
        like = f"%{q}%"
        query = query.filter(
            (models.Produto.nome.ilike(like)) | (models.Produto.categoria.ilike(like))
        )

    if cursor_id:
        query = query.filter(models.Produto.id < cursor_id)

    itens = query.order_by(models.Produto.id.desc()).limit(limit).all()

    adapter = TypeAdapter(List[schemas.ProdutoOut])
    outs = adapter.validate_python(itens)

    for o, p in zip(outs, itens):
        imagem_path = getattr(p, "imagem_path", None)
        if imagem_path:
            # Se imagem_path for uma lista, pega o primeiro item para imagem_url principal
            if isinstance(imagem_path, list) and len(imagem_path) > 0:
                o.imagem_url = signed_url(imagem_path[0])
                # Gera URLs para todas as imagens
                o.imagens_url = [signed_url(path) for path in imagem_path]
            else:
                o.imagem_url = signed_url(imagem_path)
                o.imagens_url = [signed_url(imagem_path)]
        else:
            o.imagem_url = None
            o.imagens_url = []

    return outs

@router.get("/{produto_id}", response_model=schemas.ProdutoOut)
def get_produto(produto_id: int, db: Session = Depends(get_db)):
    produto = db.get(models.Produto, produto_id)
    if not produto:
        raise HTTPException(status_code=404, detail="Produto não encontrado")
    data = schemas.ProdutoOut.model_validate(produto).model_dump()
    imagem_path = produto.imagem_path
    if imagem_path:
        # Se imagem_path for uma lista, pega o primeiro item
        if isinstance(imagem_path, list) and len(imagem_path) > 0:
            data["imagem_url"] = signed_url(imagem_path[0])
            data["imagens_url"] = [signed_url(path) for path in imagem_path]
        else:
            data["imagem_url"] = signed_url(imagem_path)
            data["imagens_url"] = [signed_url(imagem_path)]
    else:
        data["imagem_url"] = None
        data["imagens_url"] = []
    return data

@router.post("/", response_model=schemas.ProdutoOut, status_code=201)
def create_produto(payload: schemas.ProdutoCreate, db: Session = Depends(get_db)):
    produto = models.Produto(**payload.model_dump())
    db.add(produto)
    db.commit()
    db.refresh(produto)
    data = schemas.ProdutoOut.model_validate(produto).model_dump()
    data["imagem_url"] = None
    return data

@router.put("/{produto_id}", response_model=schemas.ProdutoOut)
def update_produto(produto_id: int, payload: schemas.ProdutoUpdate, db: Session = Depends(get_db)):
    produto = db.get(models.Produto, produto_id)
    if not produto:
        raise HTTPException(status_code=404, detail="Produto não encontrado")
    for field, value in payload.model_dump(exclude_unset=True).items():
        setattr(produto, field, value)
    db.commit()
    db.refresh(produto)
    data = schemas.ProdutoOut.model_validate(produto).model_dump()
    imagem_path = produto.imagem_path
    if imagem_path:
        # Se imagem_path for uma lista, pega o primeiro item
        if isinstance(imagem_path, list) and len(imagem_path) > 0:
            data["imagem_url"] = signed_url(imagem_path[0])
            data["imagens_url"] = [signed_url(path) for path in imagem_path]
        else:
            data["imagem_url"] = signed_url(imagem_path)
            data["imagens_url"] = [signed_url(imagem_path)]
    else:
        data["imagem_url"] = None
        data["imagens_url"] = []
    return data

@router.delete("/{produto_id}", status_code=204)
def delete_produto(produto_id: int, db: Session = Depends(get_db)):
    produto = db.get(models.Produto, produto_id)
    if not produto:
        raise HTTPException(status_code=404, detail="Produto não encontrado")
    
    # Guarda o caminho da imagem antes de excluir o produto
    imagem_path = produto.imagem_path
    
    # Exclui o produto do banco de dados
    db.delete(produto)
    db.commit()
    
    # Tenta excluir a imagem do Supabase se existir
    if imagem_path:
        # Se imagem_path for uma lista, exclui todas as imagens
        if isinstance(imagem_path, list):
            for path in imagem_path:
                delete_success = delete_image(path)
                if not delete_success:
                    print(f"Aviso: Não foi possível excluir a imagem {path} do Supabase")
        else:
            delete_success = delete_image(imagem_path)
            if not delete_success:
                print(f"Aviso: Não foi possível excluir a imagem {imagem_path} do Supabase")
    
    return

@router.post("/{produto_id}/imagem", response_model=schemas.ProdutoOut)
async def upload_imagem_produto(
    produto_id: int,
    arquivo: UploadFile = File(..., description="Imagem do produto"),
    db: Session = Depends(get_db),
):
    produto = db.get(models.Produto, produto_id)
    if not produto:
        raise HTTPException(status_code=404, detail="Produto não encontrado")

    if not arquivo.content_type or not arquivo.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="Arquivo precisa ser uma imagem")

    conteudo = await arquivo.read()
    up = upload_image(produto_id, conteudo, arquivo.filename, arquivo.content_type)

    # Inicializa ou atualiza a lista de imagens
    if produto.imagem_path is None:
        produto.imagem_path = [up["path"]]
    elif isinstance(produto.imagem_path, list):
        produto.imagem_path.append(up["path"])
    else:
        # Se era uma string, converte para lista
        produto.imagem_path = [produto.imagem_path, up["path"]]
    
    db.commit()
    db.refresh(produto)

    data = schemas.ProdutoOut.model_validate(produto).model_dump()
    data["imagem_url"] = up["url"]
    # Atualiza imagens_url com todas as imagens
    if produto.imagem_path:
        if isinstance(produto.imagem_path, list) and len(produto.imagem_path) > 0:
            data["imagens_url"] = [signed_url(path) for path in produto.imagem_path]
        else:
            data["imagens_url"] = [signed_url(produto.imagem_path)]
    else:
        data["imagens_url"] = []
    return data

@router.delete("/{produto_id}/imagem/{imagem_index}", response_model=schemas.ProdutoOut)
def delete_imagem_produto(
    produto_id: int, 
    imagem_index: int, 
    db: Session = Depends(get_db)
):
    produto = db.get(models.Produto, produto_id)
    if not produto:
        raise HTTPException(status_code=404, detail="Produto não encontrado")
    
    if not produto.imagem_path:
        raise HTTPException(status_code=404, detail="Produto não possui imagens")
    
    # Converte para lista se não for
    if not isinstance(produto.imagem_path, list):
        produto.imagem_path = [produto.imagem_path]
    
    if imagem_index < 0 or imagem_index >= len(produto.imagem_path):
        raise HTTPException(status_code=400, detail="Índice de imagem inválido")
    
    # Remove a imagem do Supabase
    imagem_path = produto.imagem_path[imagem_index]
    delete_success = delete_image(imagem_path)
    if not delete_success:
        print(f"Aviso: Não foi possível excluir a imagem {imagem_path} do Supabase")
    
    # Remove da lista
    produto.imagem_path.pop(imagem_index)
    
    # Se não sobrou nenhuma imagem, define como None
    if len(produto.imagem_path) == 0:
        produto.imagem_path = None
    
    db.commit()
    db.refresh(produto)

    data = schemas.ProdutoOut.model_validate(produto).model_dump()
    if produto.imagem_path and len(produto.imagem_path) > 0:
        data["imagem_url"] = signed_url(produto.imagem_path[0])
        data["imagens_url"] = [signed_url(path) for path in produto.imagem_path]
    else:
        data["imagem_url"] = None
        data["imagens_url"] = []
    return data

@router.get("/{produto_id}/imagens")
def get_imagens_produto(produto_id: int, db: Session = Depends(get_db)):
    produto = db.get(models.Produto, produto_id)
    if not produto:
        raise HTTPException(status_code=404, detail="Produto não encontrado")
    
    if not produto.imagem_path:
        return {"imagens": []}
    
    # Converte para lista se não for
    if not isinstance(produto.imagem_path, list):
        produto.imagem_path = [produto.imagem_path]
    
    imagens = []
    for i, path in enumerate(produto.imagem_path):
        imagens.append({
            "index": i,
            "url": signed_url(path),
            "path": path
        })
    
    return {"imagens": imagens}

@router.get("/{produto_id}/imagem-url")
def get_imagem_url(produto_id: int, db: Session = Depends(get_db)):
    produto = db.get(models.Produto, produto_id)
    if not produto or not produto.imagem_path:
        raise HTTPException(status_code=404, detail="Imagem não encontrada")
    
    imagem_path = produto.imagem_path
    if isinstance(imagem_path, list) and len(imagem_path) > 0:
        return {"imagem_url": signed_url(imagem_path[0])}
    else:
        return {"imagem_url": signed_url(imagem_path)}
