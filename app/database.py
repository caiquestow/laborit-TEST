"""
Configuração do banco de dados
"""
from sqlalchemy import create_engine, MetaData
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.config import settings

# Criar engine do banco de dados
engine = create_engine(
    settings.database_url,
    pool_pre_ping=True,
    pool_recycle=300,
    echo=settings.debug
)

# Criar sessão
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base para modelos
Base = declarative_base()

# Metadata para refletir tabelas existentes
metadata = MetaData()

def get_db():
    """Dependency para obter sessão do banco"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db():
    """Inicializar banco de dados"""
    # Aqui você pode adicionar lógica de inicialização se necessário
    pass 