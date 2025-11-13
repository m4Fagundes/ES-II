"""
Rotas para o gerenciamento de Planos (CRUD).
Acesso restrito apenas a administradores.
"""
from fastapi import APIRouter, Depends, HTTPException, status
from api import models, db, auth

# O prefixo '/planos' será combinado com o prefixo '/admin' de main.py
router = APIRouter(
    prefix="/planos",
    tags=["Admin (Gerenciamento)"],
    # Adiciona a dependência 'is_admin' a todas as rotas neste router
    dependencies=[Depends(auth.is_admin)], 
)

# --- Endpoints de Admin ---

@router.post("/", response_model=models.Plano, status_code=status.HTTP_201_CREATED)
async def cria_plano(plano: models.PlanoCreate):
    """Cria um novo plano de internet (apenas Admin)."""
    # A validação de admin já foi feita pela dependência
    return db.create_novo_plano(plano)


@router.put("/{plano_id}", response_model=models.Plano)
async def altera_plano(plano_id: int, plano_data: models.PlanoUpdate):
    """Altera os dados de um plano existente (apenas Admin)."""
    # Verifica se há pelo menos um campo para atualizar
    if not plano_data.model_dump(exclude_unset=True):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Pelo menos um campo deve ser fornecido para atualização."
        )

    plano_atualizado = db.update_plano_by_id(plano_id, plano_data)
    
    if not plano_atualizado:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Plano com ID {plano_id} não encontrado."
        )
    return plano_atualizado


@router.delete("/{plano_id}", status_code=status.HTTP_204_NO_CONTENT)
async def deleta_plano(plano_id: int):
    """Deleta um plano existente (apenas Admin)."""
    deletado = db.delete_plano_by_id(plano_id)
    
    if not deletado:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Plano com ID {plano_id} não encontrado."
        )
    # Retorna 204 No Content se a deleção foi bem-sucedida ou se o plano não existia
    # O HTTPException acima cobre o caso 'não encontrado' esperado pelos testes.
    return