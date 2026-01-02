import re
from typing import Optional
from fastapi import HTTPException, status

MAX_FILE_SIZE = 10 * 1024 * 1024

ALLOWED_IMAGE_TYPES = {
    "image/jpeg": [b"\xff\xd8\xff"],
    "image/png": [b"\x89\x50\x4e\x47\x0d\x0a\x1a\x0a"],
    "image/gif": [b"GIF87a", b"GIF89a"],
    "image/webp": [b"RIFF", b"WEBP"],
}

def validate_cep(cep: str) -> str:
    cep_clean = re.sub(r"[^\d]", "", cep)
    
    if len(cep_clean) != 8:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="CEP deve conter exatamente 8 dígitos"
        )
    
    if not cep_clean.isdigit():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="CEP deve conter apenas números"
        )
    
    return cep_clean

def validate_file_size(file_size: int) -> None:
    if file_size > MAX_FILE_SIZE:
        raise HTTPException(
            status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
            detail=f"Arquivo muito grande. Tamanho máximo: {MAX_FILE_SIZE / (1024*1024):.1f}MB"
        )

def validate_image_content(file_bytes: bytes, content_type: str) -> None:
    if not content_type or not content_type.startswith("image/"):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Arquivo precisa ser uma imagem"
        )
    
    if content_type in ALLOWED_IMAGE_TYPES:
        magic_bytes = ALLOWED_IMAGE_TYPES[content_type]
        file_header = file_bytes[:12]
        
        is_valid = any(file_header.startswith(mb) for mb in magic_bytes)
        
        if not is_valid:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Arquivo não é uma imagem válida ou está corrompido"
            )
    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Tipo de imagem não suportado. Tipos permitidos: {', '.join(ALLOWED_IMAGE_TYPES.keys())}"
        )

def sanitize_string(value: str, max_length: Optional[int] = None) -> str:
    sanitized = re.sub(r'[<>"\']', '', value)
    sanitized = re.sub(r'[\x00-\x1f\x7f-\x9f]', '', sanitized)
    
    if max_length:
        sanitized = sanitized[:max_length]
    
    return sanitized.strip()

def validate_positive_value(value: float, field_name: str, max_value: Optional[float] = None) -> None:
    if value <= 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"{field_name} deve ser maior que zero"
        )
    
    if max_value and value > max_value:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"{field_name} não pode ser maior que {max_value}"
        )

