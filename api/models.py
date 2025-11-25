"""
Camada de Modelos (Data Transfer Objects).
Define a estrutura dos dados que trafegam na API.
"""
from pydantic import BaseModel, Field
from typing import Optional

# --- Modelos de Plano ---
class PlanoBase(BaseModel):
    nome: str
    velocidade_mbps: int = Field(..., gt=0)
    preco_mensal: float = Field(..., gt=0.0)

class Plano(PlanoBase):
    id: int

class PlanoCreate(PlanoBase):
    pass

class PlanoUpdate(BaseModel):
    nome: Optional[str] = None
    velocidade_mbps: Optional[int] = Field(None, gt=0)
    preco_mensal: Optional[float] = Field(None, gt=0.0)

# --- Modelos de Assinatura ---
class Assinatura(BaseModel):
    user_id: str
    plano_id: int
    status: str = "ativo"

    class Config:
        from_attributes = True

# --- NOVO: Modelos para o Chatbot ---
class ChatMensagem(BaseModel):
    mensagem: str

class ChatResposta(BaseModel):
    resposta: str