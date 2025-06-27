# 🤖 FinTechX API - API Inteligente com LLM

Uma API moderna que transforma perguntas em linguagem natural em consultas SQL usando OpenAI GPT, conectada ao banco de dados Northwind.

**Desenvolvido por Carlos Henrique Stow Chaves**

## ✨ Características

- **🤖 LLM Integration**: OpenAI GPT para geração inteligente de SQL
- **🗄️ Database**: MySQL [base teste Northwind na AWS]
- **⚡ FastAPI**: API moderna e rápida
- **🎨 Painel**: Interface web para utilização alem da API
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

### 3.1. Executar com Docker (Alternativa)

```bash
# Build e execução com Docker Compose
docker-compose up --build

# Ou apenas build da imagem
docker build -t fintechx-api .
docker run -p 8000:8000 -e OPENAI_API_KEY=sua_chave fintechx-api
```

### 4. Acessar o Painel

Foi criado um front basico que está integrado à API e é servido automaticamente na rota raiz.

**Local:** Acesse: **http://localhost:8000/**

**Produção:** Acesse: **https://laborit-test-gt3b.vercel.app/**


### Exemplos de Perguntas:

- "Quais são os produtos mais populares entre os clientes corporativos?"
- "Quais são os produtos mais vendidos em termos de quantidade?"
- "Qual é o volume de vendas por cidade?"
- "Quais são os clientes que mais compraram?"
- "Quais são os produtos mais caros da loja?"
- "Quais são os fornecedores mais frequentes nos pedidos?"
- "Quais os melhores vendedores?"
- "Qual é o valor total de todas as vendas realizadas por ano?"
- "Qual é o valor total de vendas por categoria de produto?"
- "Qual o ticket médio por compra?"

## 🔧 API Endpoints

### GET `/`
Painel web da aplicação

### POST `/api/query`
Consulta principal em linguagem natural

```bash
curl -X POST "http://localhost:8000/api/query" \
  -H "Content-Type: application/json" \
  -d '{
    "question": "Quais são os produtos mais populares entre os clientes corporativos?",
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
├── index.py                 # Entry point para Vercel
├── vercel.json              # Configuração Vercel
├── app/
│   ├── main.py              # Aplicação FastAPI
│   ├── api/routes.py        # Rotas da API
│   ├── services/
│   │   ├── llm_service.py   # Integração OpenAI
│   │   └── sql_service.py   # Execução SQL
│   ├── utils/
│   │   ├── serializers.py   # Serialização inteligente
│   │   ├── validators.py    # Validação de dados
│   │   └── prompts.py       # Prompts do LLM
│   └── models/schemas.py    # Schemas Pydantic
├── index.html               # Painel WEB
├── requirements.txt         # Dependências
└── LICENSE                  # Licença MIT
```

## 🚀 Serialização Inteligente

O projeto utiliza um sistema de serialização inteligente que:

- **🔄 Automático**: Trata qualquer tipo de dado automaticamente
- **🧠 Inteligente**: Detecta o tipo e aplica a melhor estratégia
- **⚡ Performance**: Otimizado para diferentes contextos
- **🛡️ Robusto**: Múltiplas estratégias de fallback

```

## 🔒 Segurança

- **SQL Injection Protection**: Validação rigorosa de consultas
- **Input Sanitization**: Limpeza de dados de entrada
- **Error Handling**: Tratamento seguro de erros

## 🚀 Deploy

### Vercel

1. Conecte seu repositório ao Vercel
2. Configure as variáveis de ambiente:
   - `DATABASE_URL`
   - `OPENAI_API_KEY`
   - `OPENAI_MODEL`
   - `APP_NAME`
   - `APP_VERSION`
   - `DEBUG`
3. Deploy automático a cada push

**URL da API:** `https://laborit-test-gt3b.vercel.app/api/`  
**URL da DOC:** `https://laborit-test-gt3b.vercel.app/docs/`  
**URL do Painel:** `https://laborit-test-gt3b.vercel.app/`

## 📝 Licença

Este projeto está sob a licença MIT.

---

**Desenvolvido por Carlos Henrique Stow Chaves**
