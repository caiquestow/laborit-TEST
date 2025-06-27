"""
Aplicação principal FastAPI
"""
import time
import os
from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, FileResponse
from app.config import settings

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
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Middleware para logging de requisições
@app.middleware("http")
async def log_requests(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    execution_time = time.time() - start_time
    print(f"{request.method} {request.url.path} - {response.status_code} - {execution_time:.3f}s")
    return response

# Middleware para tratamento de erros
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
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
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": exc.detail,
            "status_code": exc.status_code,
            "timestamp": time.time()
        }
    )

# Rota para servir o dashboard
@app.get("/", include_in_schema=False)
def serve_dashboard():
    """Serve o dashboard HTML"""
    return FileResponse(
        os.path.join(os.path.dirname(__file__), "..", "index.html"),
        media_type="text/html"
    )

# Incluir rotas da API
from app.api.routes import router
app.include_router(router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=settings.debug) 