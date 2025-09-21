"""
Sistema de logging para o projeto de predição de evasão estudantil.
"""

import logging
import sys
from pathlib import Path
from typing import Optional

from ..configuracao import configuracoes

class Registrador:
    """Classe para configurar e gerenciar logging."""
    
    _registradores = {}
    
    @classmethod
    def obter_registrador(cls, nome: str, arquivo_log: Optional[str] = None) -> logging.Logger:
        """
        Obtém um logger configurado.
        
        Args:
            nome: Nome do logger
            arquivo_log: Arquivo de log opcional
            
        Returns:
            Logger configurado
        """
        if nome in cls._registradores:
            return cls._registradores[nome]
        
        registrador = logging.getLogger(nome)
        registrador.setLevel(getattr(logging, configuracoes.logs.nivel))
        
        # Evitar duplicação de handlers
        if registrador.handlers:
            return registrador
        
        formatador = logging.Formatter(configuracoes.logs.formato)
        
        # Console handler
        if configuracoes.logs.console_handler:
            manipulador_console = logging.StreamHandler(sys.stdout)
            manipulador_console.setLevel(logging.INFO)
            manipulador_console.setFormatter(formatador)
            registrador.addHandler(manipulador_console)
        
        # File handler
        if configuracoes.logs.arquivo_handler:
            caminho_arquivo_log = arquivo_log or configuracoes.logs.arquivo_log
            
            # Garantir que o diretório pai existe
            if '/' in caminho_arquivo_log or '\\' in caminho_arquivo_log:
                Path(caminho_arquivo_log).parent.mkdir(parents=True, exist_ok=True)
            
            manipulador_arquivo = logging.FileHandler(
                caminho_arquivo_log, encoding='utf-8'
            )
            manipulador_arquivo.setLevel(logging.DEBUG)
            manipulador_arquivo.setFormatter(formatador)
            registrador.addHandler(manipulador_arquivo)
        
        cls._registradores[nome] = registrador
        return registrador

def obter_registrador(nome: str, arquivo_log: Optional[str] = None) -> logging.Logger:
    """
    Função de conveniência para obter um logger.
    
    Args:
        nome: Nome do logger
        arquivo_log: Arquivo de log opcional
        
    Returns:
        Logger configurado
    """
    return Registrador.obter_registrador(nome, arquivo_log)