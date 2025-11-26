from fastapi import APIRouter, Depends, HTTPException, status
from api import models, database, auth

# CORREÇÃO: Definimos o prefixo aqui explicitamente
router = APIRouter(
    prefix="/admin/planos",
    tags=["Admin"],
    dependencies=[Depends(auth.is_admin)] 
)

@router.post("/", response_model=models.Plano, status_code=status.HTTP_201_CREATED)
async def criar_plano(plano_data: models.PlanoCreate):
    novo_plano = database.create_novo_plano(plano_data)
    return novo_plano

@router.put("/{plano_id}", response_model=models.Plano)
async def alterar_plano(plano_id: int, plano_data: models.PlanoUpdate):
    updated_plano = database.update_plano_by_id(plano_id, plano_data)
    if not updated_plano:
        raise HTTPException(status_code=404, detail="Plano não encontrado")
    return updated_plano

@router.delete("/{plano_id}", status_code=status.HTTP_204_NO_CONTENT)
async def deletar_plano(plano_id: int):
    sucesso = database.delete_plano_by_id(plano_id)
    if not sucesso:
        raise HTTPException(status_code=404, detail="Plano não encontrado")
    return

@router.get("/financeiro", response_model=models.DashboardFinanceiro)
async def obter_receita():
    """Retorna dados consolidados para o dashboard financeiro."""
    return database.get_dados_financeiros()