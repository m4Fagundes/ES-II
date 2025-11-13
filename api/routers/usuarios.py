"""
Camada de Interface (API) - Endpoints de Usuário.

Rotas que exigem que o usuário esteja "logado" (tenha um token válido),
mas não necessariamente que seja admin.
"""
from fastapi import APIRouter, Depends, HTTPException, status
from api import models, database, auth

router = APIRouter(
    tags=["Usuários"]
)

@router.post("/assinar/{plano_id}", response_model=models.Assinatura)
async def assinar_plano(
    plano_id: int,
    user_id: str = Depends(auth.get_user_id_from_token) # Garante que o usuário está "logado"
):
    """
    Simula um usuário (logado) assinando um plano.
    O user_id é extraído do token.
    """
    # Verifica se o plano existe antes de assinar
    plano = database.get_plano_by_id(plano_id)
    if not plano:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Plano não encontrado. Não é possível assinar."
        )
    
    # Cria ou atualiza a assinatura
    assinatura = database.create_assinatura(user_id=user_id, plano_id=plano_id)
    return assinatura

@router.get("/minha-assinatura", response_model=models.Assinatura)
async def ver_minha_assinatura(
    user_id: str = Depends(auth.get_user_id_from_token) # Pega o ID do usuário logado
):
    """Retorna a assinatura do usuário atual (baseado no token)."""
    assinatura = database.get_assinatura_by_user_id(user_id)
    if not assinatura:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Nenhuma assinatura encontrada."
        )
    return assinatura