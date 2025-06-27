"""
Rotas principais da API
"""
import time
from typing import Dict, Any
from fastapi import APIRouter, HTTPException
from app.models.schemas import QueryRequest, QueryResponse, HealthResponse
from app.services.llm_service import LLMService
from app.services.sql_service import SQLService
from app.utils.validators import InputValidator
from app.config import settings
from datetime import datetime

router = APIRouter(prefix="/api", tags=["FinTechX API"])

# Instanciar serviços
llm_service = LLMService()
sql_service = SQLService()


@router.post("/query", response_model=QueryResponse)
async def natural_language_query(request: QueryRequest):
    """Endpoint principal para consultas em linguagem natural"""
    try:
        start_time = time.time()
        
        # Validar entrada
        validation = InputValidator.validate_question(request.question)
        if not validation['valid']:
            raise HTTPException(status_code=400, detail=validation['reason'])
        
        # Gerar SQL usando LLM
        llm_result = await llm_service.generate_sql(request.question)
        if not llm_result['success']:
            raise HTTPException(status_code=500, detail=f"Erro ao gerar SQL: {llm_result.get('error', 'Erro desconhecido')}")
        
        sql_query = llm_result['sql_query']
        
        # Executar consulta SQL
        sql_result = await sql_service.execute_query(sql_query, request.limit)
        if not sql_result['success']:
            raise HTTPException(status_code=500, detail=f"Erro ao executar SQL: {sql_result.get('error', 'Erro desconhecido')}")
        
        # Gerar explicação usando LLM
        explanation = await llm_service.explain_results(request.question, sql_result['data'])
        
        execution_time = time.time() - start_time
        
        # Preparar resposta
        response_data = {
            'question': request.question,
            'sql_query': sql_query,
            'result': sql_result['data'],
            'explanation': explanation,
            'execution_time': execution_time
        }
        
        return QueryResponse(**response_data)
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro interno: {str(e)}")


# TODO: Endpoints de Analytics - Usados para debug e testes
# @router.get("/analytics/top-products")
# async def get_top_products(limit: int = 10):
#     """
#     Obtém os produtos mais vendidos
#     """
#     try:
#         if not InputValidator.validate_limit(limit):
#             raise HTTPException(status_code=400, detail="Limite deve estar entre 1 e 1000")
#         
#         result = await analytics_service.get_top_products(limit)
#         
#         if not result['success']:
#             raise HTTPException(status_code=500, detail=result.get('error', 'Erro desconhecido'))
#         
#         return {
#             'success': True,
#             'data': result['data'],
#             'chart_data': result.get('chart_data'),
#             'insights': result.get('insights', []),
#             'execution_time': result['execution_time']
#         }
#         
#     except HTTPException:
#         raise
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=f"Erro interno: {str(e)}")


# TODO: Endpoints de Banco - Usados para debug e desenvolvimento
# @router.get("/database/tables")
# async def get_database_tables():
#     """
#     Lista todas as tabelas disponíveis no banco
#     """
#     try:
#         result = await sql_service.get_table_info()
#         
#         if not result['success']:
#             raise HTTPException(status_code=500, detail=result.get('error', 'Erro desconhecido'))
#         
#         return {
#             'success': True,
#             'tables': result['data'],
#             'count': len(result['data'])
#         }
#         
#     except HTTPException:
#         raise
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=f"Erro interno: {str(e)}")


# TODO: Endpoints de Cache - Usados para monitoramento em produção
# @router.get("/cache/stats")
# async def get_cache_stats():
#     """
#     Obtém estatísticas do cache
#     """
#     try:
#         stats = await cache_service.get_cache_stats()
#         return stats
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=f"Erro interno: {str(e)}")


@router.get("/health", response_model=HealthResponse)
async def health_check():
    """
    Health check da aplicação
    """
    return HealthResponse(
        status="healthy",
        version="1.0.0",
        timestamp=datetime.now(),
        database_status="connected",
        redis_status="not_configured"
    )


@router.get("/")
async def root():
    """Endpoint raiz"""
    return {
        "message": "FinTechX API - API Inteligente com LLM",
        "version": settings.app_version,
        "docs": "/docs",
        "health": "/api/health"
    } 