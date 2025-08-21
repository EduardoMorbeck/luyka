from pydantic import BaseModel, Field, condecimal
from typing import Optional
from datetime import datetime

class ProdutoBase(BaseModel):
    nome: str = Field(..., max_length=150)
    descricao: Optional[str] = None
    preco: condecimal(max_digits=10, decimal_places=2)
    estoque: int = 0
    categoria: Optional[str] = None

class ProdutoCreate(ProdutoBase):
    pass

class ProdutoUpdate(BaseModel):
    nome: Optional[str] = Field(None, max_length=150)
    descricao: Optional[str] = None
    preco: Optional[condecimal(max_digits=10, decimal_places=2)] = None
    estoque: Optional[int] = None
    categoria: Optional[str] = None

class ProdutoOut(ProdutoBase):
    id: int
    criado_em: datetime
    atualizado_em: datetime

    class Config:
        from_attributes = True
