"""
Módulo de Autenticação e Autorização.

Define as dependências do FastAPI para verificar a identidade
e as permissões do usuário.
"""
from fastapi import Header, HTTPException, Depends, status

# --- Tokens Falsos para Simulação ---
# Em uma aplicação real, isso viria de um provedor OAuth2 (ex: JWT)
TOKEN_DB = {
    "admin-secret-token": "admin",
    "user-normal-token": "user",
}

async def get_current_user_role(x_token: str = Header(...)):
    """
    Dependência que verifica o 'X-Token' e retorna o "role" (papel)
    do usuário (admin ou user).
    """
    role = TOKEN_DB.get(x_token)
    if not role:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido ou ausente",
        )
    return role

async def get_user_id_from_token(x_token: str = Header(...)):
    """
    Dependência que valida o token e retorna o "user_id" (o próprio token).
    """
    if x_token not in TOKEN_DB:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido ou ausente",
        )
    return x_token

async def is_admin(role: str = Depends(get_current_user_role)):
    """
    Dependência que valida se o "role" obtido do token é 'admin'.
    Usada para proteger endpoints de administração.
    """
    if role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Acesso negado. Requer privilégios de administrador.",
        )
    return True