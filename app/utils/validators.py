"""
Validadores para segurança e validação de dados
"""
from typing import Dict, Any


class InputValidator:
    """Validador de entrada de dados"""
    
    @classmethod
    def validate_question(cls, question: str) -> Dict[str, Any]:
        """Valida uma pergunta em linguagem natural"""
        if not question or not question.strip():
            return {
                'valid': False,
                'reason': 'Pergunta não pode estar vazia'
            }
        
        if len(question) > 500:
            return {
                'valid': False,
                'reason': 'Pergunta muito longa (máximo 500 caracteres)'
            }
        
        # Verificar caracteres suspeitos
        suspicious_chars = ['<', '>', '&', '"', "'", ';', '=', '{', '}']
        for char in suspicious_chars:
            if char in question:
                return {
                    'valid': False,
                    'reason': f'Caractere suspeito encontrado: {char}'
                }
        
        return {
            'valid': True,
            'reason': 'Pergunta válida'
        } 