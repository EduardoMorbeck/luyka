from fastapi import APIRouter, Depends, HTTPException, Query, UploadFile, File
from sqlalchemy.orm import Session
from typing import List, Optional
from pydantic import TypeAdapter
from ..db import get_db
from .. import models, schemas
from ..services.images import upload_image, signed_url

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
        o.imagem_url = signed_url(getattr(p, "imagem_path", None)) if getattr(p, "imagem_path", None) else None

    return outs

@router.get("/{produto_id}", response_model=schemas.ProdutoOut)
def get_produto(produto_id: int, db: Session = Depends(get_db)):
    produto = db.get(models.Produto, produto_id)
    if not produto:
        raise HTTPException(status_code=404, detail="Produto não encontrado")
    data = schemas.ProdutoOut.model_validate(produto).model_dump()
    data["imagem_url"] = signed_url(produto.imagem_path) if produto.imagem_path else None
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
    data["imagem_url"] = signed_url(produto.imagem_path) if produto.imagem_path else None
    return data

@router.delete("/{produto_id}", status_code=204)
def delete_produto(produto_id: int, db: Session = Depends(get_db)):
    produto = db.get(models.Produto, produto_id)
    if not produto:
        raise HTTPException(status_code=404, detail="Produto não encontrado")
    db.delete(produto)
    db.commit()
    return

# --------- IMAGENS ---------

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

    produto.imagem_path = up["path"]
    db.commit()
    db.refresh(produto)

    data = schemas.ProdutoOut.model_validate(produto).model_dump()
    data["imagem_url"] = up["url"]
    return data

@router.get("/{produto_id}/imagem-url")
def get_imagem_url(produto_id: int, db: Session = Depends(get_db)):
    produto = db.get(models.Produto, produto_id)
    if not produto or not produto.imagem_path:
        raise HTTPException(status_code=404, detail="Imagem não encontrada")
    return {"imagem_url": signed_url(produto.imagem_path)}
