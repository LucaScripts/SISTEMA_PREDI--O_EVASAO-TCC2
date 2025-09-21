"""
Analisador de grade curricular para regras de negócio.
"""

import pandas as pd
from typing import Dict, Any, Optional, List

from ..utilitarios import obter_registrador

registrador = obter_registrador(__name__)

class AnalisadorCurriculo:
    """Analisador de grade curricular e progressão de curso."""
    
    def __init__(self, df_disciplinas: Optional[pd.DataFrame] = None,
                 df_cursos: Optional[pd.DataFrame] = None):
        """
        Inicializa o analisador.
        
        Args:
            df_disciplinas: DataFrame com dados das disciplinas
            df_cursos: DataFrame com dados dos cursos
        """
        self.df_disciplinas = df_disciplinas
        self.df_cursos = df_cursos
        self.estatisticas_cursos = {}
        
        if df_cursos is not None:
            self._processar_dados_cursos()
        
        registrador.info("Analisador de currículo inicializado")
    
    def _processar_dados_cursos(self) -> None:
        """Processa dados dos cursos para análise."""
        try:
            if 'Código' in self.df_cursos.columns:
                self.estatisticas_cursos = self.df_cursos.set_index('Código').to_dict('index')
            else:
                registrador.warning("Coluna 'Código' não encontrada em cursos")
                # Tentar outras colunas possíveis
                for coluna in ['Cod', 'ID', 'Cód', 'Code']:
                    if coluna in self.df_cursos.columns:
                        self.estatisticas_cursos = self.df_cursos.set_index(coluna).to_dict('index')
                        break
        except Exception as e:
            registrador.error(f"Erro ao processar dados dos cursos: {e}")
    
    def eh_primeira_disciplina(self, dados_aluno: Dict[str, Any]) -> bool:
        """
        Verifica se o aluno está na primeira disciplina do curso.
        
        Args:
            dados_aluno: Dados do aluno
            
        Returns:
            True se está na primeira disciplina
        """
        try:
            modulo_atual = dados_aluno.get('Módulo atual', '')
            codigo_disciplina = dados_aluno.get('Cód.Disc. atual', '')
            
            # Considerar primeira disciplina se:
            # - Está no módulo 1
            # - Ou tem código que indica início (disciplinas que terminam em 001, 01, etc.)
            if str(modulo_atual) in ['1', '1.0', 'I', 'Módulo 1']:
                return True
            
            if codigo_disciplina:
                codigo_str = str(codigo_disciplina)
                # Padrões que indicam primeira disciplina
                if (codigo_str.endswith('001') or 
                    codigo_str.endswith('01') or
                    '001' in codigo_str or
                    'INTRO' in codigo_str.upper()):
                    return True
            
            return False
            
        except Exception as e:
            registrador.debug(f"Erro ao verificar primeira disciplina: {e}")
            return False
    
    def curso_completado(self, dados_aluno: Dict[str, Any]) -> bool:
        """
        Verifica se o aluno completou o curso.
        
        Args:
            dados_aluno: Dados do aluno
            
        Returns:
            True se o curso foi completado
        """
        try:
            # Verificar indicadores de conclusão
            situacao = dados_aluno.get('Situação', '').upper()
            modulo_atual = dados_aluno.get('Módulo atual', '')
            
            # Situações que indicam conclusão
            situacoes_conclusao = ['FORMADO', 'CONCLUÍDO', 'FINALIZADO', 'TF']
            if any(sit in situacao for sit in situacoes_conclusao):
                return True
            
            # Verificar se está no último módulo (assumindo máximo de 4 módulos)
            if str(modulo_atual) in ['4', '4.0', 'IV', 'Módulo 4', 'ÚLTIMO']:
                return True
            
            # Verificar através do currículo se disponível
            codigo_curso = dados_aluno.get('Cód.Curso', '')
            if codigo_curso and self.df_cursos is not None:
                # Lógica adicional baseada nos dados do curso
                pass
            
            return False
            
        except Exception as e:
            registrador.debug(f"Erro ao verificar conclusão do curso: {e}")
            return False
    
    def obter_estatisticas_curso(self) -> Dict[str, Any]:
        """
        Retorna estatísticas dos cursos analisados.
        
        Returns:
            Dicionário com estatísticas
        """
        estatisticas = {
            'total_cursos': len(self.estatisticas_cursos) if self.df_cursos is not None else 0,
            'total_disciplinas': len(self.df_disciplinas) if self.df_disciplinas is not None else 0,
            'cursos_disponiveis': list(self.estatisticas_cursos.keys()) if self.estatisticas_cursos else []
        }
        
        return estatisticas
    
    def analisar_progressao_aluno(self, dados_aluno: Dict[str, Any]) -> Dict[str, Any]:
        """
        Analisa a progressão do aluno no curso.
        
        Args:
            dados_aluno: Dados do aluno
            
        Returns:
            Análise da progressão
        """
        analise = {
            'primeira_disciplina': self.eh_primeira_disciplina(dados_aluno),
            'curso_completado': self.curso_completado(dados_aluno),
            'modulo_atual': dados_aluno.get('Módulo atual', 'Não informado'),
            'disciplina_atual': dados_aluno.get('Disciplina atual', 'Não informada'),
            'codigo_curso': dados_aluno.get('Cód.Curso', 'Não informado')
        }
        
        return analise