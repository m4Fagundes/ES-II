"""
Camada de Interface (API) - Endpoints de Administração.

Rotas protegidas que só podem ser acessadas por usuários
com o "role" de "admin".
"""
from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from api import models, database, auth

router = APIRouter(
    prefix="/admin/planos",
    tags=["Admin"],
    # Aplica a dependência 'is_admin' a TODAS as rotas neste arquivo.
    # Isso é muito mais limpo (DRY - Don't Repeat Yourself).
    dependencies=[Depends(auth.is_admin)] 
)

@router.post("/", response_model=models.Plano, status_code=status.HTTP_201_CREATED)
async def criar_plano(plano_data: models.PlanoCreate):
    """
    [Admin] Cria um novo plano de internet.
    """
    novo_plano = database.create_novo_plano(plano_data)
    return novo_plano

@router.put("/{plano_id}", response_model=models.Plano)
async def alterar_plano(plano_id: int, plano_data: models.PlanoUpdate):
    """
    [Admin] Altera os dados de um plano existente.
    """
    updated_plano = database.update_plano_by_id(plano_id, plano_data)
    
    if not updated_plano:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Plano não encontrado"
        )
    
    if not plano_data.model_dump(exclude_unset=True):
         raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="Nenhum dado enviado para atualização"
        )

    return updated_plano

@router.delete("/{plano_id}", status_code=status.HTTP_204_NO_CONTENT)
async def deletar_plano(plano_id: int):
    """
    [Admin] Deleta um plano de internet.
    """
    sucesso = database.delete_plano_by_id(plano_id)
    if not sucesso:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Plano não encontrado"
        )
    
    # Se sucesso, retorna 204 No Content automaticamente (sem corpo)
    return