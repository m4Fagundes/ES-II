"""
Camada de Interface (API) - Endpoints Públicos de Planos.

Estes endpoints podem ser acessados por qualquer pessoa,
autenticada ou não.
"""
from fastapi import APIRouter, HTTPException, status
from typing import List
from api import models, database

# Cria um "mini-aplicativo" FastAPI para este conjunto de rotas
router = APIRouter(
    prefix="/planos",  # Prefixo para todas as rotas neste arquivo
    tags=["Planos"]      # Agrupamento na documentação do Swagger
)

@router.get("/", response_model=List[models.Plano])
async def listar_planos():
    """Retorna uma lista de todos os planos de internet disponíveis."""
    return database.get_all_planos()

@router.get("/{plano_id}", response_model=models.Plano)
async def obter_plano(plano_id: int):
    """Retorna um plano específico pelo ID."""
    plano = database.get_plano_by_id(plano_id)
    if not plano:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Plano não encontrado"
        )
    return plano