"""
Módulo de Autenticação e Autorização Dinâmico.
Agora verifica os usuários reais no database.py.
"""
from fastapi import Header, HTTPException, Depends, status
from api import database  # Importamos o banco de dados

async def get_user_from_token_header(x_token: str = Header(...)):
    """
    Função auxiliar para validar o token no banco de dados.
    """
    user = database.get_user_by_token(x_token)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido ou usuário não encontrado",
        )
    return user

async def get_current_user_role(x_token: str = Header(...)):
    """
    Retorna o papel (role) do usuário dono do token.
    """
    user = await get_user_from_token_header(x_token)
    return user["role"]

async def get_user_id_from_token(x_token: str = Header(...)):
    """
    Retorna o ID (que no nosso mock é o próprio token ou email) do usuário.
    """
    user = await get_user_from_token_header(x_token)
    return user["id"]

async def is_admin(role: str = Depends(get_current_user_role)):
    """
    Verifica se é admin.
    """
    if role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Acesso negado. Requer privilégios de administrador.",
        )
    return True