"""
Schemas Pydantic para validação de dados
"""
from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field
from datetime import datetime


class QueryRequest(BaseModel):
    """Schema para requisição de consulta"""
    question: str = Field(..., description="Pergunta em linguagem natural")
    limit: Optional[int] = Field(10, description="Limite de resultados")


class QueryResponse(BaseModel):
    """Schema para resposta de consulta"""
    question: str
    sql_query: str
    result: List[Dict[str, Any]]
    explanation: str
    execution_time: float


class HealthResponse(BaseModel):
    """Schema para resposta de health check"""
    status: str
    timestamp: datetime
    version: str
    database_status: str
    redis_status: str 