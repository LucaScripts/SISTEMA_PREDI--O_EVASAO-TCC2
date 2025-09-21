"""
Módulo de regras de negócio.
"""

from .motor_regras import MotorRegrasNegocio, ResultadoRegra
from .analisador_curriculo import AnalisadorCurriculo

__all__ = [
    'MotorRegrasNegocio',
    'ResultadoRegra',
    'AnalisadorCurriculo'
]