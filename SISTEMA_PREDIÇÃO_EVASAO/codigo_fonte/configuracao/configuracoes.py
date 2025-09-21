"""
Configurações do sistema de predição de evasão estudantil.
"""

import os
from pathlib import Path
from typing import Dict, List, Any
from dataclasses import dataclass

# Diretório raiz do projeto
RAIZ_PROJETO = Path(__file__).parent.parent.parent

@dataclass
class ConfiguracaoModelo:
    """Configurações do modelo XGBoost."""
    numero_estimadores: int = 200
    profundidade_maxima: int = 6
    taxa_aprendizado: float = 0.1
    subamostra: float = 0.8
    subamostra_colunas: float = 0.8
    semente_aleatoria: int = 42
    metrica_avaliacao: str = 'mlogloss'

@dataclass
class ConfiguracaoRegrasNegocio:
    """Configurações das regras de negócio."""
    # Limites para classificações
    lfi_minimo_parcelas: int = 2  # Limpeza Financeira: ≥2 parcelas
    nc_minimo_faltas: int = 5     # Nunca Compareceu: ≥5 faltas
    lfr_minimo_faltas: int = 12   # Limpeza Frequência: ≥12 faltas
    mt_maximo_faltas: int = 4     # Matriculado: <5 faltas
    
    # Probabilidades das regras
    probabilidade_nc: float = 0.95
    probabilidade_lfi: float = 0.90
    probabilidade_lfr: float = 0.90
    probabilidade_lac: float = 0.85
    probabilidade_nf: float = 0.80
    probabilidade_mt: float = 0.85
    
    # Mapeamento de prefixos para cursos
    prefixos_cursos: Dict[str, str] = None
    
    def __post_init__(self):
        if self.prefixos_cursos is None:
            self.prefixos_cursos = {
                'ELT': 'Eletrotécnica',
                'ENF': 'Enfermagem',
                'FMC': 'Farmácia',
                'RAD': 'Radiologia',
                'STB': 'Segurança do Trabalho',
                'ADM': 'Administração'
            }

@dataclass
class ConfiguracaoDados:
    """Configurações de dados."""
    # Diretórios
    diretorio_dados_brutos: Path = RAIZ_PROJETO / "data" / "raw"
    diretorio_dados_processados: Path = RAIZ_PROJETO / "data" / "processed"
    diretorio_modelos: Path = RAIZ_PROJETO / "data" / "models"
    diretorio_saida: Path = RAIZ_PROJETO / "output"
    
    # Arquivos de entrada
    arquivo_alunos: str = "alunos_ativos_atual.xlsx"
    arquivo_dados_treinamento: str = "Planilhabasedados.xlsx"
    arquivo_disciplinas: str = "disciplinas.xlsx"
    arquivo_cursos: str = "cursos.xlsx"
    
    # Arquivos de modelo
    arquivo_modelo: str = "modelo_xgboost_sem_classes_criticas.pkl"
    arquivo_mapeamento_classes: str = "class_mapping_otimizado.pkl"
    
    # Features esperadas
    caracteristicas_esperadas: List[str] = None
    
    def __post_init__(self):
        if self.caracteristicas_esperadas is None:
            self.caracteristicas_esperadas = [
                'Pend. Financ.', 'Faltas Consecutivas', 'Pend. Acad.', 'Módulo atual',
                'Cód.Curso', 'Curso', 'Currículo', 'Sexo', 'Identidade',
                'Turma Atual', 'Cód.Disc. atual', 'Disciplina atual'
            ]
        
        # Criar diretórios se não existirem
        for diretorio in [self.diretorio_dados_brutos, self.diretorio_dados_processados, 
                         self.diretorio_modelos, self.diretorio_saida]:
            diretorio.mkdir(parents=True, exist_ok=True)

@dataclass
class ConfiguracaoLogs:
    """Configurações de logging."""
    nivel: str = "INFO"
    formato: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    arquivo_handler: bool = True
    console_handler: bool = True
    arquivo_log: str = "sistema_predicao_evasao.log"

class Configuracoes:
    """Classe principal de configurações."""
    
    def __init__(self):
        self.modelo = ConfiguracaoModelo()
        self.regras_negocio = ConfiguracaoRegrasNegocio()
        self.dados = ConfiguracaoDados()
        self.logs = ConfiguracaoLogs()
        
        # Classes mantidas após otimização
        self.classes_mantidas = [
            'Cancelamento Comercial', 'Cancelamento Unidade', 'Não Formados',
            'Limpeza Academica', 'Limpeza Financeira', 'Limpeza de Frequencia',
            'Matriculado', 'Nunca Compareceu'
        ]
        
        # Situações de evasão (excluindo Matriculado)
        self.situacoes_evasao = [
            'Cancelamento Comercial', 'Cancelamento Unidade', 'Não Formados',
            'Limpeza Academica', 'Limpeza Financeira', 'Limpeza de Frequencia',
            'Nunca Compareceu'
        ]
        
        # Códigos de situação para mapeamento
        self.codigos_situacao = {
            'MT': 'Matriculado',
            'LFI': 'Limpeza Financeira',
            'LFR': 'Limpeza de Frequencia',
            'LAC': 'Limpeza Academica',
            'NC': 'Nunca Compareceu',
            'NF': 'Não Formados',
            'CAC': 'Cancelamento Comercial',
            'CAU': 'Cancelamento Unidade',
            'TR': 'Transferido',
            'TF': 'Transferido para outra turma',
            'FO': 'Formado'
        }
    
    def obter_caminho_disciplinas(self) -> Path:
        """Retorna caminho do arquivo de disciplinas."""
        return self.dados.diretorio_dados_brutos / self.dados.arquivo_disciplinas
    
    def obter_caminho_cursos(self) -> Path:
        """Retorna caminho do arquivo de cursos."""
        return self.dados.diretorio_dados_brutos / self.dados.arquivo_cursos
    
    def obter_caminho_modelo(self) -> Path:
        """Retorna caminho do arquivo de modelo."""
        return self.dados.diretorio_modelos / self.dados.arquivo_modelo
    
    def obter_caminho_mapeamento_classes(self) -> Path:
        """Retorna caminho do arquivo de mapeamento de classes."""
        return self.dados.diretorio_modelos / self.dados.arquivo_mapeamento_classes

# Instância global de configurações
configuracoes = Configuracoes()