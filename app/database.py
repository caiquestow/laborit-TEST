"""
Configuração do banco de dados
"""
from sqlalchemy import create_engine, MetaData
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.config import settings

# Criar engine do banco de dados com tratamento de erro
try:
    engine = create_engine(
        settings.database_url,
        pool_pre_ping=True,
        pool_recycle=300,
        echo=settings.debug
    )
    print("✅ Engine do banco criado com sucesso")
except Exception as e:
    print(f"❌ Erro ao criar engine do banco: {e}")
    engine = None

# Criar sessão
if engine:
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
else:
    SessionLocal = None

# Base para modelos
Base = declarative_base()

# Metadata para refletir tabelas existentes
metadata = MetaData()

def get_db():
    """Dependency para obter sessão do banco"""
    if not SessionLocal:
        raise Exception("Banco de dados não configurado")
    
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def init_db():
    """Inicializar banco de dados"""
    # Aqui você pode adicionar lógica de inicialização se necessário
    pass 