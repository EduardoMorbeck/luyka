from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel
from datetime import timedelta
from ..auth import create_access_token, verify_password, ADMIN_USERNAME, ADMIN_PASSWORD_HASH
import os

router = APIRouter(prefix="/auth", tags=["Autenticação"])

security = HTTPBearer()

class LoginRequest(BaseModel):
    username: str
    password: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"

@router.post("/login", response_model=TokenResponse)
async def login(credentials: LoginRequest):
    if credentials.username != ADMIN_USERNAME:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciais inválidas"
        )
    
    if ADMIN_PASSWORD_HASH:
        if not verify_password(credentials.password, ADMIN_PASSWORD_HASH):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Credenciais inválidas"
            )
    
    access_token = create_access_token(
        data={"sub": credentials.username},
        expires_delta=timedelta(hours=24)
    )
    
    return TokenResponse(access_token=access_token)

