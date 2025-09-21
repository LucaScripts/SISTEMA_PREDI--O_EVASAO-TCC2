#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Script para debugar a diversidade dos valores SHAP
"""
import sys
import os
sys.path.insert(0, os.getcwd())

from codigo_fonte.nucleo import SistemaPredicaoEvasao
from codigo_fonte.configuracao import configuracoes
from codigo_fonte.utilitarios.carregador_dados import CarregadorDados
import pandas as pd
import numpy as np

def debug_diversidade_shap():
    print("🔍 DEBUGANDO DIVERSIDADE DOS VALORES SHAP")
    print("="*60)
    
    try:
        # Inicializar sistema
        sistema = SistemaPredicaoEvasao()
        sistema.inicializar()
        print("✅ Sistema inicializado")
        
        # Carregar dados
        caminho_arquivo = configuracoes.dados.diretorio_dados_brutos / configuracoes.dados.arquivo_alunos
        df = CarregadorDados.carregar_excel_com_deteccao_cabecalho(caminho_arquivo)
        print(f"✅ Dados carregados: {len(df)} alunos")
        
        # Testar 5 alunos diferentes
        df_teste = df.head(10).copy()
        
        # Preprocessar dados
        df_processado = sistema.preditor_ml.preprocessar_dados(df_teste)
        print(f"✅ Dados processados: {df_processado.shape}")
        print(f"Features: {list(df_processado.columns)}")
        
        # Fazer predições ML
        predicoes_ml, probabilidades_ml, valores_shap = sistema.preditor_ml.fazer_predicoes(df_processado)
        
        print(f"\n🧪 ANÁLISE DOS VALORES SHAP:")
        print(f"Shape valores_shap: {valores_shap.shape}")
        
        # Analisar cada aluno individualmente
        nomes_features = df_processado.columns.tolist()
        
        for indice_aluno in range(min(5, len(valores_shap))):
            print(f"\n--- ALUNO {indice_aluno + 1}: {df_teste.iloc[indice_aluno]['Nome']} ---")
            
            valores_aluno = valores_shap[indice_aluno]  # Shape (n_features, n_classes)
            print(f"Shape valores_aluno: {valores_aluno.shape}")
            
            # Calcular importância por feature (máximo absoluto entre todas as classes)
            importancias_features = np.max(np.abs(valores_aluno), axis=1)
            
            print("Top 3 features mais importantes:")
            indices_ordenados = np.argsort(importancias_features)[::-1]
            
            for i, idx in enumerate(indices_ordenados[:3]):
                feature_name = nomes_features[idx]
                importancia = importancias_features[idx]
                # Encontrar a classe com maior valor absoluto para esta feature
                classe_max = np.argmax(np.abs(valores_aluno[idx]))
                valor_original = valores_aluno[idx, classe_max]
                
                print(f"  {i+1}. {feature_name}: {importancia:.4f} (valor={valor_original:.4f})")
            
            # Verificar se sempre a primeira feature é selecionada
            indice_max = np.argmax(importancias_features)
            fator_principal = nomes_features[indice_max]
            valor_importancia = importancias_features[indice_max]
            
            print(f"🎯 Fator Principal: {fator_principal} (valor: {valor_importancia:.4f})")
            
        # Analisar a distribuição geral
        print(f"\n📊 ANÁLISE GERAL DOS VALORES SHAP:")
        
        all_importances = []
        feature_selections = []
        
        for i in range(len(valores_shap)):
            valores_aluno = valores_shap[i]
            importancias_features = np.max(np.abs(valores_aluno), axis=1)
            all_importances.append(importancias_features)
            
            indice_max = np.argmax(importancias_features)
            feature_selections.append(nomes_features[indice_max])
        
        # Contar seleções por feature
        from collections import Counter
        contador_features = Counter(feature_selections)
        
        print("Distribuição de features selecionadas:")
        for feature, count in contador_features.most_common():
            percentage = (count / len(feature_selections)) * 100
            print(f"  {feature}: {count} vezes ({percentage:.1f}%)")
        
        # Verificar se os valores são muito similares
        all_importances = np.array(all_importances)
        print(f"\nEstatísticas das importâncias:")
        for i, feature in enumerate(nomes_features):
            valores_feature = all_importances[:, i]
            print(f"  {feature}: média={np.mean(valores_feature):.4f}, std={np.std(valores_feature):.4f}")
            
    except Exception as e:
        print(f"❌ Erro: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    debug_diversidade_shap()