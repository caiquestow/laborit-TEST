"""
Entry point para Vercel
"""
import sys
import os

# Adicionar o diretório raiz ao path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    from app.main import app
    print("✅ Aplicação FastAPI carregada com sucesso")
except Exception as e:
    print(f"❌ Erro ao carregar aplicação: {e}")
    raise

# Exportar a aplicação FastAPI para o Vercel
handler = app 