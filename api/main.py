"""
Ponto de Entrada Principal da Aplicação FastAPI.
"""
import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
# Importamos todos os routers, incluindo os novos
from api.routers import planos, usuarios, admin, chatbot, speedtest

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="ProvedorNet API",
    description="API para gerenciamento de ISP com Chatbot IA e Speedtest.",
    version="1.2.0",
)

# --- Configuração CORS ---
# Permite acesso de qualquer origem (*) para facilitar testes locais
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Registro das Rotas ---
app.include_router(planos.router)
app.include_router(usuarios.router)
app.include_router(admin.router)
app.include_router(chatbot.router)
app.include_router(speedtest.router)

@app.get("/", tags=["Root"])
async def read_root():
    return {"message": "API ProvedorNet está online!"}