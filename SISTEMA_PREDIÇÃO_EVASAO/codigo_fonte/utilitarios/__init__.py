"""
Módulo de utilitários do sistema.
"""

from .registrador import obter_registrador, Registrador
from .carregador_dados import CarregadorDados

__all__ = [
    'obter_registrador',
    'Registrador', 
    'CarregadorDados'
]