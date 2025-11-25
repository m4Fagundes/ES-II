from fastapi import APIRouter, Response, Request

router = APIRouter(prefix="/speedtest", tags=["Speed Test"])

# Este endpoint é usado se você quiser testar download local (opcional agora)
@router.get("/download")
async def download_test():
    tamanho_bytes = 25 * 1024 * 1024 
    dados = b'\0' * tamanho_bytes
    return Response(
        content=dados,
        media_type="application/octet-stream",
        headers={
            "Content-Length": str(tamanho_bytes),
            "Cache-Control": "no-store, no-cache, must-revalidate",
        }
    )

# --- ESSENCIAL PARA O SEU TESTE DE UPLOAD ---
@router.post("/upload")
async def upload_test(request: Request):
    """
    O Frontend manda dados para cá para medir a velocidade de Upload.
    """
    total_bytes = 0
    async for chunk in request.stream():
        total_bytes += len(chunk)
    
    return {"received_bytes": total_bytes, "message": "Upload OK"}