from fastapi import APIRouter, HTTPException, status
from api import models, database

router = APIRouter(tags=["Autenticação"])

@router.post("/auth/register", response_model=models.TokenResponse)
async def registrar(user: models.UserCreate):
    novo_user = database.create_user(user)
    if not novo_user:
        raise HTTPException(status_code=400, detail="Email já cadastrado")
    
    return {
        "access_token": novo_user["id"],
        "token_type": "bearer",
        "user_name": novo_user["nome"],
        "role": "user"
    }

@router.post("/auth/login", response_model=models.TokenResponse)
async def login(dados: models.UserLogin):
    user = database.get_user_by_email(dados.email)
    
    # Verificação simples de senha (sem hash para o exemplo)
    if not user or user["password"] != dados.password:
        raise HTTPException(status_code=401, detail="Email ou senha incorretos")
    
    return {
        "access_token": user["id"],
        "token_type": "bearer",
        "user_name": user["nome"],
        "role": user["role"]
    }
    