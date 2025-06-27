"""
Aplicação principal FastAPI
"""
import time
from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from app.config import settings
from app.api.routes import router

# Criar aplicação FastAPI
app = FastAPI(
    title=settings.app_name,
    description="API Inteligente com LLM para análise de dados",
    version=settings.app_version,
    docs_url="/docs",
    redoc_url="/redoc"
)

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Em produção, especifique os domínios permitidos
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Middleware para logging de requisições
@app.middleware("http")
async def log_requests(request: Request, call_next):
    """
    Middleware para logging de requisições
    """
    start_time = time.time()
    
    # Processar requisição
    response = await call_next(request)
    
    # Calcular tempo de execução
    execution_time = time.time() - start_time
    
    # Log da requisição
    print(f"{request.method} {request.url.path} - {response.status_code} - {execution_time:.3f}s")
    
    return response

# Middleware para tratamento de erros
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """
    Handler global para exceções
    """
    return JSONResponse(
        status_code=500,
        content={
            "error": "Erro interno do servidor",
            "detail": str(exc),
            "timestamp": time.time()
        }
    )

@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    """
    Handler para exceções HTTP
    """
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": exc.detail,
            "status_code": exc.status_code,
            "timestamp": time.time()
        }
    )

# Incluir rotas
app.include_router(router)

if __name__ == "__main__":
    import uvicorn
    
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.debug
    ) 