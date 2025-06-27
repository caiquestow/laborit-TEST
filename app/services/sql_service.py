"""
Serviço para execução de consultas SQL
"""
import time
from typing import List, Dict, Any, Optional
from sqlalchemy import text
from app.database import get_db
from app.utils.serializers import DataSerializer


class SQLService:
    """Serviço para execução de consultas SQL"""
    
    def __init__(self):
        """Inicializa o serviço SQL"""
        pass
    
    async def execute_query(self, sql_query: str, limit: Optional[int] = None) -> Dict[str, Any]:
        """Executa uma consulta SQL"""
        try:
            start_time = time.time()
            
            # Aplicar limite se especificado
            if limit and 'LIMIT' not in sql_query.upper():
                sql_query += f" LIMIT {limit}"
            
            # Executar consulta
            db = next(get_db())
            result = db.execute(text(sql_query))
            
            # Converter resultados
            columns = result.keys()
            data = [dict(zip(columns, row)) for row in result.fetchall()]
            
            # Sanitizar dados
            sanitized_data = DataSerializer.to_dict_safe(data)
            
            execution_time = time.time() - start_time
            
            return {
                'success': True,
                'data': sanitized_data,
                'execution_time': execution_time,
                'row_count': len(sanitized_data)
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'data': [],
                'execution_time': 0
            }
    
    async def test_connection(self) -> Dict[str, Any]:
        """Testa a conexão com o banco de dados"""
        try:
            start_time = time.time()
            
            sql_query = "SELECT 1 as test"
            result = await self.execute_query(sql_query)
            
            execution_time = time.time() - start_time
            
            return {
                'success': result['success'],
                'execution_time': execution_time,
                'error': result.get('error', None)
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'execution_time': 0
            } 