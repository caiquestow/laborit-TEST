"""
Configurações da aplicação
"""
import os
from typing import Optional
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Configurações da aplicação"""
    
    # Banco de Dados
    database_url: str = "mysql+pymysql://user_read_only:laborit_teste_2789@northwind-mysql-db.ccghzwgwh2c7.us-east-1.rds.amazonaws.com:3306/northwind"
    
    # OpenAI
    openai_api_key: Optional[str] = None
    openai_model: str = "gpt-4o-mini"
    
    # Aplicação
    app_name: str = "FinTechX API"
    app_version: str = "1.0.0"
    debug: bool = True
    
    # TODO: Redis e cache podem ser implementados para otimizar consultas repetidas
    
    class Config:
        env_file = ".env"
        case_sensitive = False


# Instância global das configurações
settings = Settings() 