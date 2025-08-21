from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional

from ..db import get_db
from .. import models, schemas

router = APIRouter(prefix="/produtos", tags=["Produtos"])

@router.get("/", response_model=List[schemas.ProdutoOut])
def list_produtos(
    q: Optional[str] = Query(None, description="Busca por nome/categoria"),
    limit: int = Query(50, ge=1, le=200),
    offset: int = Query(0, ge=0),
    db: Session = Depends(get_db),
):
    query = db.query(models.Produto)
    if q:
        like = f"%{q}%"
        query = query.filter(
            (models.Produto.nome.ilike(like)) | (models.Produto.categoria.ilike(like))
        )
    return query.order_by(models.Produto.id.desc()).limit(limit).offset(offset).all()

@router.get("/{produto_id}", response_model=schemas.ProdutoOut)
def get_produto(produto_id: int, db: Session = Depends(get_db)):
    produto = db.get(models.Produto, produto_id)
    if not produto:
        raise HTTPException(status_code=404, detail="Produto não encontrado")
    return produto

@router.post("/", response_model=schemas.ProdutoOut, status_code=201)
def create_produto(payload: schemas.ProdutoCreate, db: Session = Depends(get_db)):
    produto = models.Produto(**payload.model_dump())
    db.add(produto)
    db.commit()
    db.refresh(produto)
    return produto

@router.put("/{produto_id}", response_model=schemas.ProdutoOut)
def update_produto(produto_id: int, payload: schemas.ProdutoUpdate, db: Session = Depends(get_db)):
    produto = db.get(models.Produto, produto_id)
    if not produto:
        raise HTTPException(status_code=404, detail="Produto não encontrado")
    for field, value in payload.model_dump(exclude_unset=True).items():
        setattr(produto, field, value)
    db.commit()
    db.refresh(produto)
    return produto

@router.delete("/{produto_id}", status_code=204)
def delete_produto(produto_id: int, db: Session = Depends(get_db)):
    produto = db.get(models.Produto, produto_id)
    if not produto:
        raise HTTPException(status_code=404, detail="Produto não encontrado")
    db.delete(produto)
    db.commit()
    return
