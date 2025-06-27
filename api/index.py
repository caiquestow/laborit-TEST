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

# Para Vercel, exportar diretamente a aplicação ASGI
app.debug = False 