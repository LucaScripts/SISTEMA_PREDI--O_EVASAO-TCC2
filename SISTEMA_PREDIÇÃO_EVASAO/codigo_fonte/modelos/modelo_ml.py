"""
Modelo de Machine Learning para predição de evasão estudantil.
"""

import joblib
import shap
import numpy as np
import pandas as pd
from pathlib import Path
from typing import Tuple, List, Optional, Dict, Any
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import LabelEncoder

from ..utilitarios import obter_registrador
from ..configuracao import configuracoes

registrador = obter_registrador(__name__)

class PreditorEvasaoEstudantil:
    """Preditor de evasão estudantil usando XGBoost."""
    
    def __init__(self):
        """Inicializa o preditor."""
        self.modelo = None
        self.explicador = None
        self.info_classes = None
        self.codificadores_rotulos = {}
        self.imputadores = {}
        self._carregado = False
    
    def carregar_modelo(self, caminho_modelo: Optional[Path] = None, 
                       caminho_mapeamento_classes: Optional[Path] = None) -> None:
        """
        Carrega o modelo treinado e configurações.
        
        Args:
            caminho_modelo: Caminho para o arquivo do modelo
            caminho_mapeamento_classes: Caminho para o mapeamento de classes
            
        Raises:
            FileNotFoundError: Se os arquivos não forem encontrados
            Exception: Se houver erro no carregamento
        """
        try:
            # Usar caminhos padrão se não especificados
            if caminho_modelo is None:
                caminho_modelo = configuracoes.obter_caminho_modelo()
            if caminho_mapeamento_classes is None:
                caminho_mapeamento_classes = configuracoes.obter_caminho_mapeamento_classes()
            
            registrador.info("Carregando modelo de machine learning...")
            
            # Verificar se arquivos existem
            if not caminho_modelo.exists():
                raise FileNotFoundError(f"Modelo não encontrado: {caminho_modelo}")
            
            # Carregar modelo
            self.modelo = joblib.load(caminho_modelo)
            registrador.info(f"Modelo carregado: {type(self.modelo).__name__}")
            
            # Carregar mapeamento de classes
            if caminho_mapeamento_classes.exists():
                self.info_classes = joblib.load(caminho_mapeamento_classes)
                registrador.info("Mapeamento de classes carregado")
            
            # Carregar artifacts de treinamento
            caminho_artifacts = configuracoes.dados.diretorio_modelos / "training_artifacts.pkl"
            if caminho_artifacts.exists():
                artifacts = joblib.load(caminho_artifacts)
                self.codificadores_rotulos = artifacts.get('label_encoders', {})
                self.imputadores = artifacts.get('imputers', {})
            
            # Inicializar explicador SHAP
            registrador.info("Inicializando explainer SHAP...")
            self.explicador = shap.TreeExplainer(self.modelo)
            
            self._carregado = True
            registrador.info("Modelo carregado com sucesso")
            
        except Exception as e:
            registrador.error(f"Erro ao carregar modelo: {e}")
            raise
    
    def preprocessar_dados(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Pré-processa os dados para o modelo.
        
        Args:
            df: DataFrame com dados brutos
            
        Returns:
            DataFrame processado para o modelo
        """
        if not self._carregado:
            raise RuntimeError("Modelo não foi carregado. Chame carregar_modelo() primeiro.")
        
        registrador.info(f"Pré-processando dados: {df.shape}")
        
        # Selecionar features esperadas
        features_disponives = []
        for feature in configuracoes.dados.caracteristicas_esperadas:
            if feature in df.columns:
                features_disponives.append(feature)
        
        registrador.info(f"Features disponíveis: {len(features_disponives)}/{len(configuracoes.dados.caracteristicas_esperadas)}")
        
        if len(features_disponives) == 0:
            raise ValueError("Nenhuma feature esperada encontrada nos dados")
        
        df_processado = df[features_disponives].copy()
        
        # Aplicar label encoders
        for coluna, encoder in self.codificadores_rotulos.items():
            if coluna in df_processado.columns:
                # Primeiro, preencher valores NaN com valor padrão
                valor_default = encoder.classes_[0] if len(encoder.classes_) > 0 else 'DESCONHECIDO'
                df_processado[coluna] = df_processado[coluna].fillna(valor_default)
                
                # Converter para string e tratar 'nan' string
                df_processado[coluna] = df_processado[coluna].astype(str)
                df_processado[coluna] = df_processado[coluna].replace('nan', valor_default)
                
                # Verificar valores únicos após tratamento
                valores_unicos = df_processado[coluna].unique()
                valores_novos = set(valores_unicos) - set(encoder.classes_)
                
                if valores_novos:
                    registrador.warning(f"Valores novos em {coluna}: {valores_novos}")
                    # Substituir valores desconhecidos por valor padrão
                    mask = ~df_processado[coluna].isin(encoder.classes_)
                    df_processado.loc[mask, coluna] = valor_default
                
                df_processado[coluna] = encoder.transform(df_processado[coluna])
        
        # Aplicar imputadores
        for coluna, imputador in self.imputadores.items():
            if coluna in df_processado.columns:
                valores_originais = df_processado[coluna].values.reshape(-1, 1)
                valores_imputados = imputador.transform(valores_originais)
                df_processado[coluna] = valores_imputados.flatten()
        
        # Garantir que todas as colunas estejam em formato numérico
        # Tratar colunas que ainda são objeto (string)
        for coluna in df_processado.columns:
            if df_processado[coluna].dtype == 'object':
                registrador.warning(f"Coluna {coluna} ainda é tipo object. Convertendo para numérico.")
                # Tentar converter diretamente para numérico
                try:
                    df_processado[coluna] = pd.to_numeric(df_processado[coluna], errors='coerce')
                    # Se houve valores NaN após conversão, preencher com 0
                    if df_processado[coluna].isnull().any():
                        df_processado[coluna] = df_processado[coluna].fillna(0)
                except:
                    # Se falhou, usar label encoder simples
                    from sklearn.preprocessing import LabelEncoder
                    le = LabelEncoder()
                    df_processado[coluna] = df_processado[coluna].fillna('DESCONHECIDO')
                    df_processado[coluna] = le.fit_transform(df_processado[coluna].astype(str))
        
        registrador.info(f"Dados pré-processados: {df_processado.shape}")
        return df_processado
    
    def fazer_predicoes(self, df: pd.DataFrame) -> Tuple[List[str], List[List[float]], np.ndarray]:
        """
        Faz predições para um DataFrame.
        
        Args:
            df: DataFrame com dados processados
            
        Returns:
            Tuple com (predições, probabilidades, valores SHAP)
        """
        if not self._carregado:
            raise RuntimeError("Modelo não foi carregado. Chame carregar_modelo() primeiro.")
        
        registrador.info(f"Fazendo predições para {len(df)} amostras...")
        
        # Fazer predições
        predicoes_indices = self.modelo.predict(df)
        probabilidades = self.modelo.predict_proba(df)
        
        # Converter índices para nomes de classes
        nomes_classes = self.modelo.classes_
        predicoes = [nomes_classes[idx] for idx in predicoes_indices]
        
        # Calcular valores SHAP
        registrador.info("Calculando valores SHAP...")
        valores_shap = self.explicador.shap_values(df)
        
        registrador.info("Predições concluídas")
        
        return predicoes, probabilidades.tolist(), valores_shap
    
    def obter_feature_importance(self) -> Dict[str, float]:
        """
        Obtém a importância das features do modelo.
        
        Returns:
            Dicionário com importância das features
        """
        if not self._carregado or self.modelo is None:
            return {}
        
        importancias = self.modelo.feature_importances_
        nomes_features = configuracoes.dados.caracteristicas_esperadas
        
        return dict(zip(nomes_features[:len(importancias)], importancias))
    
    def esta_carregado(self) -> bool:
        """Verifica se o modelo foi carregado."""
        return self._carregado