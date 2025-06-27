"""
Entry point para Vercel
"""
from app.main import app

# Exportar a aplicação FastAPI para o Vercel
handler = app 