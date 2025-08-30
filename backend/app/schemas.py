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
    # Opcional: útil se quiser aceitar POST JSON; no nosso GET vamos usar Query params
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
    preco: condecimal(max_digits=10, decimal_places=2) # type: ignore
    estoque: int = 0
    categoria: Optional[str] = None
    imagem_path: Optional[List[str]] = None  # Array de strings para múltiplas imagens

class ProdutoCreate(ProdutoBase):
    pass

class ProdutoUpdate(BaseModel):
    nome: Optional[str] = Field(None, max_length=150)
    descricao: Optional[str] = None
    preco: Optional[condecimal(max_digits=10, decimal_places=2)] = None # type: ignore
    estoque: Optional[int] = None
    categoria: Optional[str] = None
    imagem_path: Optional[List[str]] = None  # Array de strings para múltiplas imagens

class ProdutoOut(ProdutoBase):
    id: int
    criado_em: datetime
    atualizado_em: datetime
    imagem_url: Optional[str] = None   # URL pronta pra exibição (pública ou assinada) - primeira imagem
    imagens_url: Optional[List[str]] = None  # URLs de todas as imagens
    imagem_path: Optional[List[str]] = None  # Array de strings para múltiplas imagens

    class Config:
        from_attributes = True
