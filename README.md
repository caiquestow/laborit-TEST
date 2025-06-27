# 🤖 FinTechX API - API Inteligente com LLM

Uma API moderna que transforma perguntas em linguagem natural em consultas SQL usando OpenAI GPT, conectada ao banco de dados Northwind.

**Desenvolvido por Carlos Henrique Stow Chaves**

## ✨ Características

- **🤖 LLM Integration**: OpenAI GPT para geração inteligente de SQL
- **🗄️ Database**: MySQL Northwind na AWS
- **⚡ FastAPI**: API moderna e rápida
- **🎨 Dashboard**: Interface dark e minimalista
- **🛡️ Segurança**: Validação e sanitização de dados
- **📊 Serialização Inteligente**: Tratamento automático de qualquer tipo de dado

## 🚀 Quick Start

### 1. Configuração do Ambiente

```bash
# Clone o repositório
git clone <repository-url>
cd laborit

# Crie um ambiente virtual
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate     # Windows

# Instale as dependências
pip install -r requirements.txt
```

### 2. Configuração das Variáveis de Ambiente

```bash
# Copie o arquivo de exemplo
cp env.example .env

# Edite com suas credenciais
nano .env
```

Configure as seguintes variáveis:
```env
OPENAI_API_KEY=sua_chave_openai
DATABASE_URL=mysql://user:password@host:port/northwind
```

### 3. Executar a API

```bash
# Iniciar a API
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### 4. Acessar o Dashboard

```bash
# Em outro terminal, inicie o servidor do dashboard
python serve_dashboard.py
```

Acesse: **http://localhost:8080/index.html**

## 🎨 Dashboard

O dashboard oferece uma experiência dark e minimalista:

- **💬 Interface Simples**: Foco na pergunta e resposta
- **🎨 Design Dark**: Tema escuro para uso prolongado
- **📱 Responsivo**: Funciona em desktop e mobile
- **⚡ Tempo Real**: Indicador de status da API

### Exemplos de Perguntas:

- "Quais são os produtos mais caros?"
- "Mostre os clientes de Londres"
- "Quantos pedidos foram feitos em 2023?"

## 🔧 API Endpoints

### POST `/api/query`
Consulta principal em linguagem natural

```bash
curl -X POST "http://localhost:8000/api/query" \
  -H "Content-Type: application/json" \
  -d '{
    "question": "quais os produtos?",
    "limit": 10
  }'
```

### GET `/api/health`
Health check da aplicação

```bash
curl http://localhost:8000/api/health
```

## 🏗️ Arquitetura

```
laborit/
├── app/
│   ├── api/routes.py          # Rotas FastAPI
│   ├── services/
│   │   ├── llm_service.py     # Integração OpenAI
│   │   └── sql_service.py     # Execução SQL
│   ├── utils/
│   │   ├── serializers.py     # Serialização inteligente
│   │   ├── validators.py      # Validação de dados
│   │   └── prompts.py         # Prompts do LLM
│   └── models/schemas.py      # Schemas Pydantic
├── index.html                 # Dashboard
├── serve_dashboard.py         # Servidor do dashboard
└── requirements.txt           # Dependências
```

## 🚀 Serialização Inteligente

O projeto utiliza um sistema de serialização inteligente que:

- **🔄 Automático**: Trata qualquer tipo de dado automaticamente
- **🧠 Inteligente**: Detecta o tipo e aplica a melhor estratégia
- **⚡ Performance**: Otimizado para diferentes contextos
- **🛡️ Robusto**: Múltiplas estratégias de fallback

### Exemplo de Uso:

```python
from app.utils.serializers import DataSerializer

# Qualquer tipo de dado é tratado automaticamente
complex_data = [
    {
        "id": 1,
        "price": Decimal("19.99"),
        "image": b"\x89PNG\r\n\x1a\n...",  # bytes
        "created_at": datetime.now(),
        "tags": ["tag1", "tag2"]
    }
]

# Uma linha resolve tudo!
serialized = DataSerializer.to_dict_safe(complex_data)
```

## 🔒 Segurança

- **SQL Injection Protection**: Validação rigorosa de consultas
- **Input Sanitization**: Limpeza de dados de entrada
- **Error Handling**: Tratamento seguro de erros

## 🚀 Deploy

### Railway (Recomendado)

1. Conecte seu repositório ao Railway
2. Configure as variáveis de ambiente
3. Deploy automático a cada push

### Render

1. Crie um novo Web Service
2. Configure o build command: `pip install -r requirements.txt`
3. Configure o start command: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`

## 📝 Licença

Este projeto está sob a licença MIT.

---

**Desenvolvido com ❤️ por Carlos Henrique Stow Chaves**
