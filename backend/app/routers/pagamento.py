from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from decimal import Decimal
from brcode import BRCode
import qrcode
import base64
from io import BytesIO

router = APIRouter(prefix="/pagamento", tags=["pagamento"])

class PixRequest(BaseModel):
    nome: str
    valor: float
    cidade: str
    descricao: str = "Compra na loja Luyka"

def generate_qr_code_base64(pix_code: str) -> str:
    """Gera um QR code a partir do código Pix e retorna em base64"""
    try:
        # Criar QR code com configurações mais simples
        qr = qrcode.QRCode(
            version=None,  # Auto-determinar versão
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=8,
            border=2,
        )
        qr.add_data(pix_code)
        qr.make(fit=True)
        
        # Criar imagem
        img = qr.make_image(fill_color="black", back_color="white")
        
        # Converter para base64
        buffer = BytesIO()
        img.save(buffer, format="PNG")
        img_str = base64.b64encode(buffer.getvalue()).decode()
        
        return f"data:image/png;base64,{img_str}"
    except Exception as e:
        print(f"Erro ao gerar QR code: {e}")
        return None

@router.post("/gerar-pix")
async def gerar_pix(request: PixRequest):
    try:
        brcode = BRCode(
            name=request.nome,
            key="61835152000107",  # CNPJ da Luyka (fixo)
            city=request.cidade,
            amount=Decimal(str(request.valor)),
            description=request.descricao,  # Descrição fixa
        )
        
        payload = str(brcode)
        
        # Gerar QR code
        qr_code_base64 = generate_qr_code_base64(payload)
        
        return {
            "success": True,
            "pix_code": payload,
            "qr_code": qr_code_base64,
            "cnpj": "61835152000107",
            "valor": request.valor,
            "nome": request.nome,
            "cidade": request.cidade
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao gerar código Pix: {str(e)}")
