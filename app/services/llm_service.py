"""
Serviço de LLM para geração de SQL e análise
"""
import json
import time
from typing import Dict, Any, Optional, List
from openai import OpenAI
from app.config import settings
from app.utils.prompts import (
    SQL_GENERATION_PROMPT,
    SQL_VALIDATION_PROMPT,
    EXPLANATION_PROMPT
)
from app.utils.serializers import LLMDataPreparer


class LLMService:
    """Serviço para interação com LLM"""
    
    def __init__(self):
        """Inicializa o serviço de LLM"""
        if not settings.openai_api_key:
            raise ValueError("OpenAI API key não configurada")
        
        self.client = OpenAI(api_key=settings.openai_api_key)
        self.model = settings.openai_model
    
    async def generate_sql(self, question: str) -> Dict[str, Any]:
        """Gera SQL a partir de uma pergunta em linguagem natural"""
        try:
            import asyncio
            import json
            from openai.types.chat import ChatCompletionMessageToolCall
            
            start_time = time.time()
            tools = [
                {
                    "type": "function",
                    "function": {
                        "name": "generate_sql",
                        "description": "Gera apenas a query SQL para a pergunta do usuário, sem explicação.",
                        "parameters": {
                            "type": "object",
                            "properties": {
                                "sql_query": {
                                    "type": "string",
                                    "description": "A query SQL gerada para a pergunta do usuário."
                                }
                            },
                            "required": ["sql_query"]
                        }
                    }
                }
            ]
            
            prompt = SQL_GENERATION_PROMPT.format(question=question)
            response = await asyncio.to_thread(
                self.client.chat.completions.create,
                model=self.model,
                messages=[
                    {"role": "system", "content": "Você é um assistente especializado em SQL. Sempre use a função generate_sql para responder."},
                    {"role": "user", "content": prompt}
                ],
                tools=tools,  # type: ignore
                tool_choice={"type": "function", "function": {"name": "generate_sql"}},
                max_tokens=1000,
                temperature=0.1
            )
            
            tool_calls = response.choices[0].message.tool_calls
            sql_query = None
            if tool_calls and isinstance(tool_calls[0], ChatCompletionMessageToolCall):
                args = tool_calls[0].function.arguments
                if isinstance(args, str):
                    args = json.loads(args)
                sql_query = args.get("sql_query")
            
            if sql_query:
                validation_result = await self._validate_sql(sql_query)
            else:
                validation_result = {'valid': False, 'reason': 'SQL não gerado', 'risk_level': 'HIGH'}
            
            execution_time = time.time() - start_time
            
            return {
                'sql_query': sql_query,
                'validation': validation_result,
                'execution_time': execution_time,
                'success': validation_result.get('valid', False),
                'error': None
            }
        except Exception as e:
            return {
                'sql_query': None,
                'validation': {'valid': False, 'reason': str(e)},
                'execution_time': 0,
                'success': False,
                'error': str(e)
            }
    
    async def explain_results(self, question: str, data: List[Dict[str, Any]]) -> str:
        """Gera explicação para os resultados usando LLM"""
        try:
            # Usar o preparador inteligente de dados para LLM
            prepared_data = LLMDataPreparer.prepare_for_llm(data, max_items=10)
            
            prompt = EXPLANATION_PROMPT.format(
                question=question,
                data=prepared_data
            )
            
            response = await self._call_llm(prompt)
            return response.strip()
            
        except Exception as e:
            return f"Erro ao gerar explicação: {str(e)}"
    
    async def _call_llm(self, prompt: str) -> str:
        """Chamada genérica para o LLM"""
        try:
            import asyncio
            
            response = await asyncio.to_thread(
                self.client.chat.completions.create,
                model=self.model,
                messages=[
                    {"role": "system", "content": "Você é um assistente especializado em análise de dados."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=1000,
                temperature=0.3
            )
            
            return response.choices[0].message.content or ""
            
        except Exception as e:
            return f"Erro na chamada do LLM: {str(e)}"
    
    async def _validate_sql(self, sql_query: str) -> Dict[str, Any]:
        """Valida uma consulta SQL usando LLM"""
        try:
            import asyncio
            import json
            from openai.types.chat import ChatCompletionMessageToolCall
            
            tools = [
                {
                    "type": "function",
                    "function": {
                        "name": "validate_sql",
                        "description": "Valida se a query SQL é segura e correta.",
                        "parameters": {
                            "type": "object",
                            "properties": {
                                "is_valid": {"type": "boolean", "description": "Se a query é válida."},
                                "reason": {"type": "string", "description": "Motivo da validação."}
                            },
                            "required": ["is_valid", "reason"]
                        }
                    }
                }
            ]
            
            prompt = SQL_VALIDATION_PROMPT.format(sql_query=sql_query)
            response = await asyncio.to_thread(
                self.client.chat.completions.create,
                model=self.model,
                messages=[
                    {"role": "system", "content": "Você é um assistente especializado em SQL. Sempre use a função validate_sql para responder."},
                    {"role": "user", "content": prompt}
                ],
                tools=tools,  # type: ignore
                tool_choice={"type": "function", "function": {"name": "validate_sql"}},
                max_tokens=500,
                temperature=0.1
            )
            
            tool_calls = response.choices[0].message.tool_calls
            if tool_calls and isinstance(tool_calls[0], ChatCompletionMessageToolCall):
                args = tool_calls[0].function.arguments
                if isinstance(args, str):
                    args = json.loads(args)
                return {
                    'valid': args.get('is_valid', False),
                    'reason': args.get('reason', ''),
                    'risk_level': 'LOW' if args.get('is_valid', False) else 'HIGH'
                }
            
            return {
                'valid': False,
                'reason': 'Erro ao validar via LLM',
                'risk_level': 'UNKNOWN'
            }
        except Exception as e:
            return {
                'valid': False,
                'reason': f'Erro na validação: {str(e)}',
                'risk_level': 'UNKNOWN'
            } 