from pydantic import BaseModel, Field, condecimal
from typing import Optional, List, Union
from datetime import datetime

class FreteItem(BaseModel):
    codigo: str
    nome: str
    preco: str
    prazo: int
    erro: str
    msg: str
    valorMaoProp: str
    valorAviso: str
    valorDecl: str

class FreteResponse(BaseModel):
    fretes: List[FreteItem] = Field(default_factory=list)

class FreteQuery(BaseModel):
    nCdServico: str
    sCepOrigem: str
    sCepDestino: str
    nVlPeso: str
    nCdFormato: int
    nVlComprimento: str
    nVlAltura: str
    nVlLargura: str
    nVlDiametro: str = "0"
    sCdMaoPropria: str = "N"
    nVlValorDeclarado: str = "0"
    sCdAvisoRecebimento: str = "N"

class ProdutoBase(BaseModel):
    nome: str = Field(..., max_length=150)
    descricao: Optional[str] = None
    preco: condecimal(max_digits=10, decimal_places=2) 
    estoque: int = 0
    categoria: Optional[str] = None
    imagem_path: Optional[List[str]] = None

class ProdutoCreate(ProdutoBase):
    pass

class ProdutoUpdate(BaseModel):
    nome: Optional[str] = Field(None, max_length=150)
    descricao: Optional[str] = None
    preco: Optional[condecimal(max_digits=10, decimal_places=2)] = None 
    estoque: Optional[int] = None
    categoria: Optional[str] = None
    imagem_path: Optional[List[str]] = None

class ProdutoOut(ProdutoBase):
    id: int
    criado_em: datetime
    atualizado_em: datetime
    imagem_url: Optional[str] = None
    imagens_url: Optional[List[str]] = None
    imagem_path: Optional[List[str]] = None

    class Config:
        from_attributes = True
