from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel, Field, field_validator
from decimal import Decimal
from brcode import BRCode
import qrcode
import base64
from io import BytesIO
from ..utils.validation import sanitize_string, validate_positive_value

router = APIRouter(prefix="/pagamento", tags=["pagamento"])

class PixRequest(BaseModel):
    nome: str = Field(..., min_length=2, max_length=100)
    valor: float = Field(..., gt=0, le=100000, description="Valor em reais (máximo R$ 100.000)")
    cidade: str = Field(..., min_length=2, max_length=100)
    descricao: str = Field(default="Compra na loja Luyka", max_length=200)
    
    @field_validator("nome", "cidade", "descricao")
    @classmethod
    def sanitize_fields(cls, v: str) -> str:
        return sanitize_string(v)

def generate_qr_code_base64(pix_code: str) -> str:
    try:
        qr = qrcode.QRCode(
            version=None,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=8,
            border=2,
        )
        qr.add_data(pix_code)
        qr.make(fit=True)
        
        img = qr.make_image(fill_color="black", back_color="white")
        
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
            key="",  
            city=request.cidade,
            amount=Decimal(str(request.valor)),
            description=request.descricao,
        )
        
        payload = str(brcode)
        
        qr_code_base64 = generate_qr_code_base64(payload)
        
        return {
            "success": True,
            "pix_code": payload,
            "qr_code": qr_code_base64,
            "cnpj": "",
            "valor": request.valor,
            "nome": request.nome,
            "cidade": request.cidade
        }
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Dados inválidos para gerar código Pix"
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro ao gerar código Pix. Tente novamente mais tarde."
        )
