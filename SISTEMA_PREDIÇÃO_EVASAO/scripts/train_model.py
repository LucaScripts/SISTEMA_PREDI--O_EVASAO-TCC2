#!/usr/bin/env python3
"""
Script para treinamento do modelo XGBoost.

Este script treina um novo modelo usando os dados históricos
e salva o modelo treinado para uso no sistema de predição.

Uso:
    python scripts/train_model.py [arquivo_dados]

Exemplo:
    python scripts/train_model.py data/raw/Planilhabasedados.xlsx
"""

import sys
import argparse
from pathlib import Path
import pandas as pd
import numpy as np
import joblib
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score
from sklearn.preprocessing import LabelEncoder
from sklearn.impute import SimpleImputer
import xgboost as xgb

# Adicionar o diretório pai ao path para que possamos importar codigo_fonte
sys.path.insert(0, str(Path(__file__).parent.parent))

from codigo_fonte.utilitarios import obter_registrador, CarregadorDados
from codigo_fonte.configuracao import configuracoes

registrador = obter_registrador(__name__)

class ModelTrainer:
    """Classe para treinamento do modelo XGBoost."""
    
    def __init__(self):
        """Inicializa o treinador."""
        self.model = None
        self.label_encoders = {}
        self.imputers = {}
        self.class_mapping = {}
        
    def load_and_preprocess_data(self, data_file: Path) -> tuple:
        """
        Carrega e pré-processa os dados de treinamento.
        
        Args:
            data_file: Caminho para o arquivo de dados
            
        Returns:
            Tuple com (X, y, feature_names)
        """
        registrador.info(f"Carregando dados de treinamento: {data_file}")
        
        # Carregar dados
        df = CarregadorDados.carregar_excel_com_deteccao_cabecalho(data_file)
        registrador.info(f"Dados carregados: {df.shape}")
        
        # Remover classes problemáticas (conforme análise anterior)
        problematic_classes = ['Cancelamento Interno', 'Transferência Interna']
        df = df[~df['Situação'].isin(problematic_classes)]
        registrador.info(f"Dados após remoção de classes problemáticas: {df.shape}")
        
        # Separar features e target
        target_column = 'Situação'
        feature_columns = [col for col in configuracoes.dados.caracteristicas_esperadas if col in df.columns]
        
        registrador.info(f"Features disponíveis: {len(feature_columns)}/{len(configuracoes.dados.caracteristicas_esperadas)}")
        
        X = df[feature_columns].copy()
        y = df[target_column].copy()
        
        # Pré-processar features
        X = self._preprocess_features(X)
        
        # Codificar target
        le_target = LabelEncoder()
        y_encoded = le_target.fit_transform(y)
        
        # Salvar mapeamento de classes
        self.class_mapping = {
            'classes_mantidas': list(le_target.classes_),
            'label_encoder': le_target
        }
        
        registrador.info(f"Classes no dataset: {len(le_target.classes_)}")
        for i, class_name in enumerate(le_target.classes_):
            count = np.sum(y_encoded == i)
            registrador.info(f"  {class_name}: {count} amostras")
        
        return X, y_encoded, X.columns.tolist()
    
    def _preprocess_features(self, X: pd.DataFrame) -> pd.DataFrame:
        """Pré-processa as features."""
        # Identificar colunas numéricas automaticamente
        numeric_cols = X.select_dtypes(include=['int64', 'float64']).columns.tolist()
        
        if numeric_cols:
            # Converter para numérico
            for col in numeric_cols:
                X[col] = pd.to_numeric(X[col], errors='coerce')
            
            # Imputar valores ausentes
            self.imputers['numeric'] = SimpleImputer(strategy='median')
            X[numeric_cols] = self.imputers['numeric'].fit_transform(X[numeric_cols])
        
        # Identificar colunas categóricas automaticamente
        categorical_cols = X.select_dtypes(include=['object']).columns.tolist()
        
        if categorical_cols:
            # Imputar valores ausentes
            self.imputers['categorical'] = SimpleImputer(strategy='most_frequent')
            X[categorical_cols] = self.imputers['categorical'].fit_transform(X[categorical_cols])
            
            # Codificar variáveis categóricas
            for col in categorical_cols:
                self.label_encoders[col] = LabelEncoder()
                X[col] = self.label_encoders[col].fit_transform(X[col].astype(str))
        
        # Garantir que não há valores ausentes
        X = X.fillna(0)
        
        return X
    
    def train_model(self, X: pd.DataFrame, y: np.ndarray) -> dict:
        """
        Treina o modelo XGBoost.
        
        Args:
            X: Features de treinamento
            y: Target codificado
            
        Returns:
            Dicionário com métricas de avaliação
        """
        registrador.info("Iniciando treinamento do modelo XGBoost...")
        
        # Dividir dados em treino e teste
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42, stratify=y
        )
        
        registrador.info(f"Dados de treino: {X_train.shape}")
        registrador.info(f"Dados de teste: {X_test.shape}")
        
        # Configurar modelo XGBoost
        self.model = xgb.XGBClassifier(
            n_estimators=configuracoes.model.n_estimators,
            max_depth=configuracoes.model.max_depth,
            learning_rate=configuracoes.model.learning_rate,
            subsample=configuracoes.model.subsample,
            colsample_bytree=configuracoes.model.colsample_bytree,
            random_state=configuracoes.model.random_state,
            eval_metric=configuracoes.model.eval_metric,
            n_jobs=-1
        )
        
        # Treinar modelo
        registrador.info("Treinando modelo...")
        self.model.fit(X_train, y_train)
        
        # Avaliar modelo
        registrador.info("Avaliando modelo...")
        
        # Predições
        y_pred_train = self.model.predict(X_train)
        y_pred_test = self.model.predict(X_test)
        
        # Métricas
        train_accuracy = accuracy_score(y_train, y_pred_train)
        test_accuracy = accuracy_score(y_test, y_pred_test)
        
        # Validação cruzada
        cv_scores = cross_val_score(self.model, X_train, y_train, cv=5, scoring='accuracy')
        
        # Acurácia binária (Evasão vs Matriculado)
        binary_train_accuracy = self._calculate_binary_accuracy(y_train, y_pred_train)
        binary_test_accuracy = self._calculate_binary_accuracy(y_test, y_pred_test)
        
        metrics = {
            'train_accuracy': train_accuracy,
            'test_accuracy': test_accuracy,
            'cv_mean': cv_scores.mean(),
            'cv_std': cv_scores.std(),
            'binary_train_accuracy': binary_train_accuracy,
            'binary_test_accuracy': binary_test_accuracy,
            'X_test': X_test,
            'y_test': y_test,
            'y_pred_test': y_pred_test
        }
        
        registrador.info(f"Acurácia de treino: {train_accuracy:.4f}")
        registrador.info(f"Acurácia de teste: {test_accuracy:.4f}")
        registrador.info(f"Validação cruzada: {cv_scores.mean():.4f} ± {cv_scores.std():.4f}")
        registrador.info(f"Acurácia binária (teste): {binary_test_accuracy:.4f}")
        
        return metrics
    
    def _calculate_binary_accuracy(self, y_true: np.ndarray, y_pred: np.ndarray) -> float:
        """Calcula acurácia binária (Evasão vs Matriculado)."""
        # Converter para binário (0 = Matriculado, 1 = Evasão)
        classes = self.class_mapping['classes_mantidas']
        
        y_true_binary = np.array([0 if classes[i] == 'Matriculado' else 1 for i in y_true])
        y_pred_binary = np.array([0 if classes[i] == 'Matriculado' else 1 for i in y_pred])
        
        return accuracy_score(y_true_binary, y_pred_binary)
    
    def save_model(self) -> None:
        """Salva o modelo e artefatos relacionados."""
        models_dir = configuracoes.data.models_dir
        models_dir.mkdir(parents=True, exist_ok=True)
        
        # Salvar modelo
        model_path = models_dir / configuracoes.data.model_file
        joblib.dump(self.model, model_path)
        registrador.info(f"Modelo salvo em: {model_path}")
        
        # Salvar mapeamento de classes
        class_mapping_path = models_dir / configuracoes.data.class_mapping_file
        joblib.dump(self.class_mapping, class_mapping_path)
        registrador.info(f"Mapeamento de classes salvo em: {class_mapping_path}")
        
        # Salvar encoders e imputers
        artifacts_path = models_dir / "training_artifacts.pkl"
        artifacts = {
            'label_encoders': self.label_encoders,
            'imputers': self.imputers
        }
        joblib.dump(artifacts, artifacts_path)
        registrador.info(f"Artefatos de treinamento salvos em: {artifacts_path}")
    
    def generate_reports(self, metrics: dict, feature_names: list) -> None:
        """Gera relatórios de avaliação do modelo."""
        output_dir = configuracoes.data.output_dir
        output_dir.mkdir(parents=True, exist_ok=True)
        
        # Relatório de texto
        report_path = output_dir / "model_training_report.txt"
        with open(report_path, 'w', encoding='utf-8') as f:
            f.write("RELATÓRIO DE TREINAMENTO DO MODELO\n")
            f.write("=" * 50 + "\n\n")
            f.write(f"Acurácia de treino: {metrics['train_accuracy']:.4f}\n")
            f.write(f"Acurácia de teste: {metrics['test_accuracy']:.4f}\n")
            f.write(f"Validação cruzada: {metrics['cv_mean']:.4f} ± {metrics['cv_std']:.4f}\n")
            f.write(f"Acurácia binária (treino): {metrics['binary_train_accuracy']:.4f}\n")
            f.write(f"Acurácia binária (teste): {metrics['binary_test_accuracy']:.4f}\n\n")
            
            # Relatório de classificação
            classes = self.class_mapping['classes_mantidas']
            report = classification_report(
                metrics['y_test'], metrics['y_pred_test'], 
                target_names=classes, zero_division=0
            )
            f.write("RELATÓRIO DE CLASSIFICAÇÃO:\n")
            f.write(report)
        
        registrador.info(f"Relatório salvo em: {report_path}")
        
        # Gráfico de importância das features
        self._plot_feature_importance(feature_names, output_dir)
        
        # Matriz de confusão
        self._plot_confusion_matrix(metrics, output_dir)
    
    def _plot_feature_importance(self, feature_names: list, output_dir: Path) -> None:
        """Plota importância das features."""
        importances = self.model.feature_importances_
        indices = np.argsort(importances)[::-1]
        
        plt.figure(figsize=(12, 8))
        plt.title("Importância das Features - XGBoost")
        plt.bar(range(len(importances)), importances[indices])
        plt.xticks(range(len(importances)), [feature_names[i] for i in indices], rotation=45, ha='right')
        plt.tight_layout()
        
        plot_path = output_dir / "feature_importance.png"
        plt.savefig(plot_path, dpi=300, bbox_inches='tight')
        plt.close()
        
        registrador.info(f"Gráfico de importância salvo em: {plot_path}")
    
    def _plot_confusion_matrix(self, metrics: dict, output_dir: Path) -> None:
        """Plota matriz de confusão."""
        cm = confusion_matrix(metrics['y_test'], metrics['y_pred_test'])
        classes = self.class_mapping['classes_mantidas']
        
        plt.figure(figsize=(10, 8))
        sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', 
                   xticklabels=classes, yticklabels=classes)
        plt.title("Matriz de Confusão")
        plt.ylabel("Classe Real")
        plt.xlabel("Classe Predita")
        plt.xticks(rotation=45, ha='right')
        plt.yticks(rotation=0)
        plt.tight_layout()
        
        plot_path = output_dir / "confusion_matrix.png"
        plt.savefig(plot_path, dpi=300, bbox_inches='tight')
        plt.close()
        
        registrador.info(f"Matriz de confusão salva em: {plot_path}")

def main():
    """Função principal."""
    parser = argparse.ArgumentParser(
        description="Treinamento do modelo XGBoost para predição de evasão"
    )
    
    parser.add_argument(
        'data_file',
        nargs='?',
        default=None,
        help='Arquivo Excel com dados de treinamento (padrão: data/raw/Planilhabasedados.xlsx)'
    )
    
    parser.add_argument(
        '--verbose', '-v',
        action='store_true',
        help='Modo verboso'
    )
    
    args = parser.parse_args()
    
    # Configurar logging
    if args.verbose:
        import logging
        logging.getLogger().setLevel(logging.DEBUG)
    
    try:
        # Determinar arquivo de dados
        if args.data_file:
            data_file = Path(args.data_file)
        else:
            data_file = configuracoes.get_training_data_path()
        
        if not data_file.exists():
            registrador.error(f"Arquivo não encontrado: {data_file}")
            return 1
        
        # Inicializar treinador
        trainer = ModelTrainer()
        
        # Carregar e pré-processar dados
        X, y, feature_names = trainer.load_and_preprocess_data(data_file)
        
        # Treinar modelo
        metrics = trainer.train_model(X, y)
        
        # Salvar modelo
        trainer.save_model()
        
        # Gerar relatórios
        trainer.generate_reports(metrics, feature_names)
        
        print("\n✅ Treinamento concluído com sucesso!")
        print(f"📊 Acurácia de teste: {metrics['test_accuracy']:.4f}")
        print(f"📊 Acurácia binária: {metrics['binary_test_accuracy']:.4f}")
        print(f"📁 Modelo salvo em: {configuracoes.get_model_path()}")
        
        return 0
        
    except Exception as e:
        registrador.error(f"Erro durante o treinamento: {e}", exc_info=True)
        print(f"❌ Erro durante o treinamento: {e}")
        return 1

if __name__ == "__main__":
    sys.exit(main())


