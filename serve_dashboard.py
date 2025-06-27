#!/usr/bin/env python3
"""
Servidor HTTP simples para servir o dashboard
"""
import http.server
import socketserver
import os
import sys
from pathlib import Path

def main():
    # Configurações
    PORT = 8080
    DIRECTORY = Path(__file__).parent
    
    # Mudar para o diretório do script
    os.chdir(DIRECTORY)
    
    # Verificar se o arquivo index.html existe
    if not (DIRECTORY / "index.html").exists():
        print("❌ Erro: arquivo index.html não encontrado!")
        print("📁 Diretório atual:", DIRECTORY)
        print("📋 Arquivos disponíveis:")
        for file in DIRECTORY.glob("*.html"):
            print(f"   - {file.name}")
        sys.exit(1)
    
    # Configurar handler
    Handler = http.server.SimpleHTTPRequestHandler
    
    # Criar servidor
    with socketserver.TCPServer(("", PORT), Handler) as httpd:
        print("🚀 Servidor rodando em http://localhost:8080")
        print("📊 Dashboard disponível em http://localhost:8080/index.html")
        print("🛑 Pressione Ctrl+C para parar")
        
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\n🛑 Servidor parado pelo usuário")
            httpd.shutdown()

if __name__ == "__main__":
    main() 