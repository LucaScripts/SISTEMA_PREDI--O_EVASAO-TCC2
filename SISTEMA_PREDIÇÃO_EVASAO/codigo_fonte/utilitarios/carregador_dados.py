"""
Utilitários para carregamento e manipulação de dados.
"""

import pandas as pd
import numpy as np
from pathlib import Path
from typing import Tuple, Optional, Dict, Any

from .registrador import obter_registrador
from ..configuracao import configuracoes

registrador = obter_registrador(__name__)

class CarregadorDados:
    """Classe para carregamento e manipulação de dados."""
    
    @staticmethod
    def detectar_linha_cabecalho(df: pd.DataFrame, palavras_chave: list = None) -> int:
        """
        Detecta automaticamente a linha do header em um DataFrame.
        
        Args:
            df: DataFrame para análise
            palavras_chave: Palavras-chave para identificar o header
            
        Returns:
            Índice da linha do header
        """
        if palavras_chave is None:
            palavras_chave = ['MATRÍCULA', 'MATRICULA', 'NOME', 'CURSO', 'SITUAÇÃO']
        
        for i in range(min(5, len(df))):
            linha = df.iloc[i]
            texto_linha = ' '.join([str(valor) for valor in linha.values if pd.notna(valor)]).upper()
            if any(palavra in texto_linha for palavra in palavras_chave):
                registrador.debug(f"Header detectado na linha {i}")
                return i
        
        registrador.warning("Header não detectado automaticamente, usando linha 0")
        return 0
    
    @staticmethod
    def carregar_excel_com_deteccao_cabecalho(caminho_arquivo: Path, 
                                            palavras_chave: list = None) -> pd.DataFrame:
        """
        Carrega arquivo Excel com detecção automática de header.
        
        Args:
            caminho_arquivo: Caminho para o arquivo Excel
            palavras_chave: Palavras-chave para detectar header
            
        Returns:
            DataFrame carregado
            
        Raises:
            FileNotFoundError: Se o arquivo não for encontrado
        """
        if not caminho_arquivo.exists():
            raise FileNotFoundError(f"Arquivo não encontrado: {caminho_arquivo}")
        
        registrador.info(f"Carregando arquivo: {caminho_arquivo}")
        
        # Carregar sem header para detectar
        df_bruto = pd.read_excel(caminho_arquivo, header=None)
        
        # Detectar header
        linha_cabecalho = CarregadorDados.detectar_linha_cabecalho(df_bruto, palavras_chave)
        
        # Recarregar com header correto
        df = pd.read_excel(caminho_arquivo, header=linha_cabecalho)
        
        registrador.info(f"Dados carregados: {df.shape[0]} linhas, {df.shape[1]} colunas")
        return df
    
    @staticmethod
    def carregar_dados_curriculares() -> Tuple[Optional[pd.DataFrame], Optional[pd.DataFrame]]:
        """
        Carrega dados da grade curricular (disciplinas e cursos).
        
        Returns:
            Tuple com DataFrames de disciplinas e cursos
        """
        df_disciplinas = None
        df_cursos = None
        
        try:
            # Carregar disciplinas
            caminho_disciplinas = configuracoes.obter_caminho_disciplinas()
            if caminho_disciplinas.exists():
                df_bruto = pd.read_excel(caminho_disciplinas)
                # Usar linha 1 como header (que contém: Código, Disciplina, etc.)
                cabecalho = df_bruto.iloc[1].values
                df_disciplinas = pd.read_excel(caminho_disciplinas, skiprows=2)
                df_disciplinas.columns = cabecalho
                registrador.info(f"Disciplinas carregadas: {len(df_disciplinas)} registros")
            
            # Carregar cursos
            caminho_cursos = configuracoes.obter_caminho_cursos()
            if caminho_cursos.exists():
                df_cursos = pd.read_excel(caminho_cursos)
                registrador.info(f"Cursos carregados: {len(df_cursos)} registros")
            
        except Exception as e:
            registrador.error(f"Erro ao carregar dados curriculares: {e}")
        
        return df_disciplinas, df_cursos
    
    @staticmethod
    def limpar_identificador_aluno(dados_aluno: Dict[str, Any]) -> str:
        """
        Limpa e padroniza o identificador do aluno.
        
        Args:
            dados_aluno: Dados do aluno
            
        Returns:
            Identificador limpo
        """
        identificadores_possiveis = ['Matrícula', 'Matricula', 'ID', 'Código']
        
        for campo in identificadores_possiveis:
            if campo in dados_aluno:
                valor = dados_aluno[campo]
                if pd.notna(valor):
                    return str(valor).strip()
        
        # Se não encontrar, usar nome como fallback
        nome = dados_aluno.get('Nome', 'Desconhecido')
        return f"NOME_{str(nome).replace(' ', '_')}"
    
    @staticmethod
    def validar_dados_aluno(dados_aluno: pd.Series) -> bool:
        """
        Valida se os dados do aluno são válidos.
        
        Args:
            dados_aluno: Série com dados do aluno
            
        Returns:
            True se válido, False caso contrário
        """
        # Verificar campos obrigatórios
        campos_obrigatorios = ['Nome', 'Matrícula']
        
        for campo in campos_obrigatorios:
            if campo not in dados_aluno or pd.isna(dados_aluno[campo]):
                return False
        
        # Verificar se pelo menos uma feature está presente
        features_necessarias = configuracoes.dados.caracteristicas_esperadas
        features_presentes = [f for f in features_necessarias if f in dados_aluno.index]
        
        return len(features_presentes) > 0
    
    @staticmethod
    def preprocessar_dados_para_modelo(df: pd.DataFrame) -> pd.DataFrame:
        """
        Preprocessa dados para o modelo de ML.
        
        Args:
            df: DataFrame com dados brutos
            
        Returns:
            DataFrame processado
        """
        # Fazer uma cópia para não alterar o original
        df_processado = df.copy()
        
        # Remover linhas completamente vazias
        df_processado = df_processado.dropna(how='all')
        
        # Preencher valores NaN com valores padrão
        colunas_numericas = df_processado.select_dtypes(include=[np.number]).columns
        df_processado[colunas_numericas] = df_processado[colunas_numericas].fillna(0)
        
        colunas_texto = df_processado.select_dtypes(include=['object']).columns
        df_processado[colunas_texto] = df_processado[colunas_texto].fillna('')
        
        registrador.debug(f"Dados preprocessados: {df_processado.shape}")
        return df_processado