from __future__ import annotations

import os
import httpx
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

router = APIRouter(prefix="/frete", tags=["frete"])

MELHOR_ENVIO_TOKEN = os.environ["MELHOR_ENVIO_TOKEN"]
MELHOR_ENVIO_EMAIL = os.environ["MELHOR_ENVIO_EMAIL"]
MELHOR_ENVIO_URL = "https://www.melhorenvio.com.br/api/v2/me/shipment/calculate"


class CalcularFreteIn(BaseModel):
    from_postal_code: str = Field(..., description="CEP de origem, só números (8 dígitos)")
    to_postal_code: str = Field(..., description="CEP de destino, só números (8 dígitos)")
    height: float = Field(..., gt=0, description="Altura em cm")
    width: float = Field(..., gt=0, description="Largura em cm")
    length: float = Field(..., gt=0, description="Comprimento em cm")
    weight: float = Field(..., gt=0, description="Peso em kg")

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
            detail={"message": "Falha ao contatar o serviço de frete (network).", "reason": str(e)},
        )

    if not (200 <= resp.status_code < 300):
        try:
            upstream = resp.json()
        except Exception:
            upstream = {"raw": resp.text}
        raise HTTPException(
            status_code=resp.status_code,
            detail={"message": "Erro na API do Melhor Envio.", "upstream": upstream},
        )

    try:
        return resp.json()
    except ValueError:
        raise HTTPException(status_code=502, detail={"message": "Resposta inválida da API do Melhor Envio."})
