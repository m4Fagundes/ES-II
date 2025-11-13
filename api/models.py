"""
Camada de Modelos (Data Transfer Objects).

Define a "forma" dos dados que entram e saem da API, garantindo
a validação e os limites do sistema (Clean Architecture).
"""
from pydantic import BaseModel, Field, ConfigDict # Importação do ConfigDict
from typing import Optional

# --- Modelos de Plano ---

class PlanoBase(BaseModel):
    """Modelo base para um plano, com campos comuns."""
    nome: str
    velocidade_mbps: int = Field(..., gt=0, description="Velocidade de download em Mbps")
    preco_mensal: float = Field(..., gt=0.0, description="Preço em R$")

class Plano(PlanoBase):
    """Modelo de dados completo de um Plano (como ele existe no DB)."""
    id: int

class PlanoCreate(PlanoBase):
    """Modelo para criação de um novo plano (sem ID)."""
    pass # Herda todos os campos do PlanoBase

class PlanoUpdate(BaseModel):
    """
    Modelo para atualização de um plano.
    Todos os campos são opcionais (None).
    """
    nome: Optional[str] = None
    velocidade_mbps: Optional[int] = Field(None, gt=0)
    preco_mensal: Optional[float] = Field(None, gt=0.0)

# --- Modelos de Assinatura ---

class Assinatura(BaseModel):
    """Modelo simples para representar uma assinatura de usuário."""
    user_id: str
    plano_id: int
    status: str = "ativo"

    # CORREÇÃO Pydantic: Usando ConfigDict em vez de class Config
    model_config = ConfigDict(from_attributes=True)