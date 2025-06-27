"""
Serializadores inteligentes para diferentes tipos de dados
"""
import json
import base64
from datetime import datetime, date
from decimal import Decimal
from typing import Any, Dict, List
from enum import Enum


class SmartJSONEncoder(json.JSONEncoder):
    """
    Encoder JSON inteligente que trata automaticamente qualquer tipo de dado
    """
    
    def default(self, obj: Any) -> Any:
        """Trata tipos não serializáveis automaticamente"""
        
        # Bytes - tentar decodificar como UTF-8, senão converter para base64
        if isinstance(obj, bytes):
            try:
                return obj.decode('utf-8')
            except UnicodeDecodeError:
                return {
                    "_type": "bytes",
                    "encoding": "base64",
                    "data": base64.b64encode(obj).decode('ascii'),
                    "size": len(obj)
                }
        
        # Decimal - converter para float
        if isinstance(obj, Decimal):
            return float(obj)
        
        # Datetime - converter para ISO string
        if isinstance(obj, (datetime, date)):
            return obj.isoformat()
        
        # Enum - converter para valor
        if isinstance(obj, Enum):
            return obj.value
        
        # Objetos com método to_dict()
        if hasattr(obj, 'to_dict'):
            return obj.to_dict()
        
        # Objetos com método __dict__
        if hasattr(obj, '__dict__'):
            return {
                "_type": obj.__class__.__name__,
                "data": obj.__dict__
            }
        
        # Objetos com método __str__
        if hasattr(obj, '__str__'):
            return str(obj)
        
        # Fallback - converter para string truncada
        return f"{obj.__class__.__name__}: {str(obj)[:100]}..."


class DataSerializer:
    """
    Serializador inteligente de dados com múltiplas estratégias
    """
    
    @staticmethod
    def to_json_safe(data: Any, **kwargs) -> str:
        """
        Converte dados para JSON de forma segura usando encoder customizado
        
        Args:
            data: Dados a serem serializados
            **kwargs: Argumentos adicionais para json.dumps
            
        Returns:
            String JSON
        """
        return json.dumps(data, cls=SmartJSONEncoder, ensure_ascii=False, **kwargs)
    
    @staticmethod
    def to_dict_safe(data: Any) -> Any:
        """
        Converte dados para dict de forma segura
        
        Args:
            data: Dados a serem convertidos
            
        Returns:
            Dados convertidos
        """
        try:
            # Tentar serializar e deserializar para garantir compatibilidade
            json_str = DataSerializer.to_json_safe(data)
            return json.loads(json_str)
        except Exception as e:
            # Fallback para conversão manual
            return DataSerializer._manual_convert(data)
    
    @staticmethod
    def _manual_convert(obj: Any) -> Any:
        """
        Conversão manual para casos extremos
        """
        if isinstance(obj, dict):
            return {str(k): DataSerializer._manual_convert(v) for k, v in obj.items()}
        elif isinstance(obj, list):
            return [DataSerializer._manual_convert(item) for item in obj]
        elif isinstance(obj, bytes):
            try:
                return obj.decode('utf-8')
            except:
                return f"<bytes:{len(obj)}>"
        elif hasattr(obj, 'as_tuple'):  # Decimal
            return float(obj)
        elif isinstance(obj, (datetime, date)):
            return obj.isoformat()
        elif isinstance(obj, (int, float, str, bool, type(None))):
            return obj
        else:
            return str(obj)[:100] + "..." if len(str(obj)) > 100 else str(obj)


class LLMDataPreparer:
    """
    Preparador inteligente de dados para LLM
    """
    
    @staticmethod
    def prepare_for_llm(data: List[Dict[str, Any]], max_items: int = 10) -> str:
        """
        Prepara dados para envio ao LLM de forma inteligente
        
        Args:
            data: Dados a serem preparados
            max_items: Máximo de itens a incluir
            
        Returns:
            String JSON preparada para LLM
        """
        # Limitar quantidade de dados
        limited_data = data[:max_items] if len(data) > max_items else data
        
        # Serializar de forma inteligente
        serialized = DataSerializer.to_dict_safe(limited_data)
        
        # Adicionar metadados úteis para o LLM
        metadata = {
            "total_records": len(data),
            "showing_records": len(limited_data),
            "data_type": "database_result",
            "truncated": len(data) > max_items
        }
        
        result = {
            "metadata": metadata,
            "data": serialized
        }
        
        return DataSerializer.to_json_safe(result, indent=2) 