from __future__ import annotations

import os
import httpx
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field, field_validator
from ..utils.validation import validate_cep, validate_positive_value

router = APIRouter(prefix="/frete", tags=["frete"])

MELHOR_ENVIO_TOKEN = os.getenv("MELHOR_ENVIO_TOKEN", "")
MELHOR_ENVIO_EMAIL = os.getenv("MELHOR_ENVIO_EMAIL", "")
MELHOR_ENVIO_URL = "https://www.melhorenvio.com.br/api/v2/me/shipment/calculate"


class CalcularFreteIn(BaseModel):
    from_postal_code: str = Field(..., description="CEP de origem, só números (8 dígitos)")
    to_postal_code: str = Field(..., description="CEP de destino, só números (8 dígitos)")
    height: float = Field(..., gt=0, le=200, description="Altura em cm (máximo 200cm)")
    width: float = Field(..., gt=0, le=200, description="Largura em cm (máximo 200cm)")
    length: float = Field(..., gt=0, le=200, description="Comprimento em cm (máximo 200cm)")
    weight: float = Field(..., gt=0, le=30, description="Peso em kg (máximo 30kg)")
    
    @field_validator("from_postal_code", "to_postal_code")
    @classmethod
    def validate_cep(cls, v: str) -> str:
        return validate_cep(v)

@router.post("/")
async def calcular_frete(body: CalcularFreteIn):
    headers = {
        "Accept": "application/json",
        "Authorization": f"Bearer {MELHOR_ENVIO_TOKEN}",
        "Content-Type": "application/json",
        "User-Agent": MELHOR_ENVIO_EMAIL,
    }

    payload = {
        "from": {"postal_code": body.from_postal_code},
        "to": {"postal_code": body.to_postal_code},
        "package": {
            "height": body.height,
            "width": body.width,
            "length": body.length,
            "weight": body.weight,
        },
    }

    try:
        async with httpx.AsyncClient(timeout=15.0) as client:
            resp = await client.post(MELHOR_ENVIO_URL, json=payload, headers=headers)
    except httpx.HTTPError as e:
        raise HTTPException(
            status_code=502,
            detail={"message": "Falha ao contatar o serviço de frete. Tente novamente mais tarde."}
        )

    if not (200 <= resp.status_code < 300):
        raise HTTPException(
            status_code=502,
            detail={"message": "Erro ao calcular frete. Tente novamente mais tarde."}
        )

    try:
        return resp.json()
    except ValueError:
        raise HTTPException(status_code=502, detail={"message": "Resposta inválida da API do Melhor Envio."})
