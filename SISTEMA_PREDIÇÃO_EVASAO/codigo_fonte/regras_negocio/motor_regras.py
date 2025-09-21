"""
Motor de regras de negócio para classificação de estudantes.
"""

import pandas as pd
from typing import Dict, Any, Tuple
from dataclasses import dataclass

from ..utilitarios import obter_registrador
from ..configuracao import configuracoes
from .analisador_curriculo import AnalisadorCurriculo

registrador = obter_registrador(__name__)

@dataclass
class ResultadoRegra:
    """Resultado da aplicação de uma regra de negócio."""
    situacao: str
    probabilidade: float
    razao: str
    regra_aplicada: str

class MotorRegrasNegocio:
    """Motor de regras de negócio do Grau Técnico."""
    
    def __init__(self, analisador_curriculo: AnalisadorCurriculo = None):
        """
        Inicializa o motor de regras.
        
        Args:
            analisador_curriculo: Analisador de grade curricular
        """
        self.analisador_curriculo = analisador_curriculo
        self.contador_regras = {
            'NC_por_regra': 0,
            'LFR_por_regra': 0,
            'LFI_por_regra': 0,
            'LAC_por_regra': 0,
            'NF_por_regra': 0,
            'MT_por_regra': 0,
            'total_ajustes': 0
        }
    
    def resetar_contadores(self) -> None:
        """Reseta os contadores de regras aplicadas."""
        for chave in self.contador_regras:
            self.contador_regras[chave] = 0
    
    def aplicar_regras_negocio(self, dados_aluno: Dict[str, Any], 
                             predicao_ml: str, probabilidade_ml: float) -> ResultadoRegra:
        """
        Aplica regras de negócio para um aluno específico.
        
        Args:
            dados_aluno: Dados do aluno
            predicao_ml: Predição do modelo ML
            probabilidade_ml: Probabilidade da predição ML
            
        Returns:
            Resultado da aplicação das regras
        """
        # Extrair e limpar dados do aluno
        faltas_consecutivas = self._extrair_valor_numerico(
            dados_aluno.get('Faltas Consecutivas', 0)
        )
        pendencia_financeira = self._extrair_valor_financeiro(
            dados_aluno.get('Pend. Financ.', 0)
        )
        # Tratar NaN corretamente para pendência acadêmica
        pendencia_academica_bruta = dados_aluno.get('Pend. Acad.', '')
        pendencia_academica = '' if pd.isna(pendencia_academica_bruta) else str(pendencia_academica_bruta).strip()
        
        registrador.debug(f"Analisando aluno: faltas={faltas_consecutivas}, "
                         f"pend_fin={pendencia_financeira}, pend_acad='{pendencia_academica}'")
        
        # Aplicar regras em ordem de prioridade
        
        # REGRA 1: NC (Nunca Compareceu) - MELHORADA
        if faltas_consecutivas >= configuracoes.regras_negocio.nc_minimo_faltas:
            if self.analisador_curriculo and self.analisador_curriculo.eh_primeira_disciplina(dados_aluno):
                self.contador_regras['NC_por_regra'] += 1
                self.contador_regras['total_ajustes'] += 1
                return ResultadoRegra(
                    situacao='Nunca Compareceu',
                    probabilidade=configuracoes.regras_negocio.probabilidade_nc,
                    razao=f'≥{configuracoes.regras_negocio.nc_minimo_faltas} faltas na primeira disciplina',
                    regra_aplicada='NC'
                )
            elif faltas_consecutivas >= configuracoes.regras_negocio.lfr_minimo_faltas:
                # Se não é primeira disciplina mas tem muitas faltas, pode ser LFR
                self.contador_regras['LFR_por_regra'] += 1
                self.contador_regras['total_ajustes'] += 1
                return ResultadoRegra(
                    situacao='Limpeza de Frequencia',
                    probabilidade=configuracoes.regras_negocio.probabilidade_lfr,
                    razao=f'≥{configuracoes.regras_negocio.lfr_minimo_faltas} faltas (não primeira disciplina)',
                    regra_aplicada='LFR'
                )
        
        # REGRA 2: LFI (Limpeza Financeira) - AJUSTADA PARA ≥2 PARCELAS
        if pendencia_financeira >= configuracoes.regras_negocio.lfi_minimo_parcelas:
            self.contador_regras['LFI_por_regra'] += 1
            self.contador_regras['total_ajustes'] += 1
            return ResultadoRegra(
                situacao='Limpeza Financeira',
                probabilidade=configuracoes.regras_negocio.probabilidade_lfi,
                razao=f'≥{configuracoes.regras_negocio.lfi_minimo_parcelas} parcelas em aberto',
                regra_aplicada='LFI'
            )
        
        # REGRA 3: LFR (Limpeza de Frequência) - GRAU TÉCNICO
        if (pendencia_financeira > 0 and 
            faltas_consecutivas >= configuracoes.regras_negocio.lfr_minimo_faltas):
            self.contador_regras['LFR_por_regra'] += 1
            self.contador_regras['total_ajustes'] += 1
            return ResultadoRegra(
                situacao='Limpeza de Frequencia',
                probabilidade=configuracoes.regras_negocio.probabilidade_lfr,
                razao=f'Pend. financeira + ≥{configuracoes.regras_negocio.lfr_minimo_faltas} faltas',
                regra_aplicada='LFR'
            )
        
        # REGRA 4: LAC (Limpeza Acadêmica) - GRAU TÉCNICO
        if self._tem_pendencia_academica(pendencia_academica):
            self.contador_regras['LAC_por_regra'] += 1
            self.contador_regras['total_ajustes'] += 1
            return ResultadoRegra(
                situacao='Limpeza Academica',
                probabilidade=configuracoes.regras_negocio.probabilidade_lac,
                razao='Pendência acadêmica',
                regra_aplicada='LAC'
            )
        
        # REGRA 5: NF (Não Formado) - MELHORADA
        if (self.analisador_curriculo and 
            self.analisador_curriculo.curso_completado(dados_aluno) and
            0 < pendencia_financeira <= 2):
            self.contador_regras['NF_por_regra'] += 1
            self.contador_regras['total_ajustes'] += 1
            return ResultadoRegra(
                situacao='Não Formados',
                probabilidade=configuracoes.regras_negocio.probabilidade_nf,
                razao='Curso completo + ≤2 parcelas',
                regra_aplicada='NF'
            )
        
        # REGRA 6: MT (Matriculado) - GRAU TÉCNICO
        if (pendencia_financeira == 0 and 
            faltas_consecutivas <= configuracoes.regras_negocio.mt_maximo_faltas):
            self.contador_regras['MT_por_regra'] += 1
            self.contador_regras['total_ajustes'] += 1
            return ResultadoRegra(
                situacao='Matriculado',
                probabilidade=configuracoes.regras_negocio.probabilidade_mt,
                razao='Sem pendências significativas',
                regra_aplicada='MT'
            )
        
        # Se nenhuma regra se aplica, usar predição do ML
        return ResultadoRegra(
            situacao=predicao_ml,
            probabilidade=probabilidade_ml,
            razao='Predição ML',
            regra_aplicada='ML'
        )
    
    def _extrair_valor_numerico(self, valor: Any) -> float:
        """
        Extrai valor numérico de forma segura.
        
        Args:
            valor: Valor a ser convertido
            
        Returns:
            Valor numérico ou 0 se conversão falhar
        """
        try:
            return float(valor) if pd.notna(valor) else 0.0
        except (ValueError, TypeError):
            return 0.0
    
    def _extrair_valor_financeiro(self, valor: Any) -> float:
        """
        Extrai valor financeiro considerando 'PC' (Pagamento Completo).
        
        Args:
            valor: Valor financeiro
            
        Returns:
            Valor numérico ou 0 se 'PC' ou conversão falhar
        """
        if pd.notna(valor) and str(valor).upper() != 'PC':
            try:
                return float(valor)
            except (ValueError, TypeError):
                return 0.0
        return 0.0  # PC = Pagamento Completo
    
    def _tem_pendencia_academica(self, pendencia_academica: str) -> bool:
        """
        Verifica se há pendência acadêmica.
        
        Args:
            pendencia_academica: String de pendência acadêmica
            
        Returns:
            True se há pendência, False caso contrário
        """
        # Verificar se o valor é válido
        if pd.isna(pendencia_academica) or not pendencia_academica:
            return False
        
        pendencia_academica_str = str(pendencia_academica).strip().upper()
        
        # Verificar se é um valor válido que indica pendência
        # PR, PV, PF são códigos reais de pendência acadêmica
        if pendencia_academica_str in ['PR', 'PV', 'PF']:
            return True
        
        # Verificar valores que indicam sem pendência
        if pendencia_academica_str in ['', 'NÃO', 'NAO', 'NAN', 'NONE']:
            return False
        
        # Para qualquer outro valor não-vazio que não seja explicitamente "não", 
        # consideramos como pendência
        return pendencia_academica_str != ''
    
    def obter_resumo_regras(self) -> Dict[str, int]:
        """
        Retorna resumo das regras aplicadas.
        
        Returns:
            Dicionário com contadores das regras
        """
        return self.contador_regras.copy()