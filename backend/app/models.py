from sqlalchemy import Column, Integer, String, Text, Numeric, TIMESTAMP
from sqlalchemy.sql import func
from .db import Base

class Produto(Base):
    __tablename__ = "produtos"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String(150), nullable=False)
    descricao = Column(Text)
    preco = Column(Numeric(10, 2), nullable=False)
    estoque = Column(Integer, nullable=False, default=0)
    categoria = Column(String(100))
    criado_em = Column(TIMESTAMP(timezone=True), server_default=func.now(), nullable=False)
    atualizado_em = Column(TIMESTAMP(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)
