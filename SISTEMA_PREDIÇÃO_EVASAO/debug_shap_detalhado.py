#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Script para debugar especificamente o processamento SHAP
"""
import sys
import os
sys.path.insert(0, os.getcwd())

from codigo_fonte.nucleo import SistemaPredicaoEvasao
from codigo_fonte.configuracao import configuracoes
from codigo_fonte.utilitarios.carregador_dados import CarregadorDados
import pandas as pd
import numpy as np

def debug_shap_processamento():
    print("🔍 DEBUGANDO PROCESSAMENTO SHAP DETALHADO")
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
        
        # Testar apenas 1 aluno para debug detalhado
        df_teste = df.head(1).copy()
        
        # Preprocessar dados
        df_processado = sistema.preditor_ml.preprocessar_dados(df_teste)
        print(f"✅ Dados processados: {df_processado.shape}")
        print(f"Colunas processadas: {list(df_processado.columns)}")
        
        # Fazer predições ML
        predicoes_ml, probabilidades_ml, valores_shap = sistema.preditor_ml.fazer_predicoes(df_processado)
        
        print(f"\n🧪 ANÁLISE DOS VALORES SHAP:")
        print(f"Tipo valores_shap: {type(valores_shap)}")
        print(f"Shape valores_shap: {valores_shap.shape if hasattr(valores_shap, 'shape') else 'Sem shape'}")
        
        if hasattr(valores_shap, '__len__'):
            print(f"Número de elementos: {len(valores_shap)}")
            
            # Testar acesso ao primeiro aluno (índice 0)
            indice_aluno = 0
            nomes_features = df_processado.columns.tolist()
            
            print(f"\n🔍 DEBUGANDO ALUNO ÍNDICE {indice_aluno}:")
            print(f"len(valores_shap) = {len(valores_shap)}")
            print(f"indice_aluno = {indice_aluno}")
            print(f"len(nomes_features) = {len(nomes_features)}")
            
            # Verificação 1: len(valores_shap) > indice_aluno
            condicao1 = len(valores_shap) > indice_aluno
            print(f"Condição 1 - len(valores_shap) > indice_aluno: {condicao1}")
            
            # Verificação 2: len(nomes_features) > 0
            condicao2 = len(nomes_features) > 0
            print(f"Condição 2 - len(nomes_features) > 0: {condicao2}")
            
            if condicao1 and condicao2:
                print(f"✅ Condições atendidas, acessando valores_shap[{indice_aluno}]...")
                
                valores_aluno_original = valores_shap[indice_aluno]
                print(f"Tipo valores_aluno_original: {type(valores_aluno_original)}")
                print(f"Shape valores_aluno_original: {valores_aluno_original.shape if hasattr(valores_aluno_original, 'shape') else 'Sem shape'}")
                
                # Verificar se tem __len__
                tem_len = hasattr(valores_aluno_original, '__len__')
                print(f"hasattr(__len__): {tem_len}")
                
                if tem_len:
                    valores_aluno = valores_aluno_original
                    print(f"len(valores_aluno): {len(valores_aluno)}")
                    
                    if len(valores_aluno) > 0:
                        print(f"✅ valores_aluno tem elementos, convertendo para array...")
                        
                        # Converter para numpy array
                        valores_array = np.array(valores_aluno)
                        print(f"valores_array shape: {valores_array.shape}")
                        print(f"valores_array[:5]: {valores_array[:5]}")
                        
                        # Encontrar índice de maior importância absoluta
                        indice_max = np.abs(valores_array).argmax()
                        print(f"indice_max: {indice_max}")
                        print(f"len(nomes_features): {len(nomes_features)}")
                        
                        if indice_max < len(nomes_features):
                            fator_principal = nomes_features[indice_max]
                            valor_importancia = float(valores_array[indice_max])
                            
                            print(f"🎯 RESULTADO:")
                            print(f"Fator Principal: {fator_principal}")
                            print(f"Valor Importância: {valor_importancia}")
                            print(f"Valor absoluto: {abs(valor_importancia)}")
                        else:
                            print(f"❌ indice_max ({indice_max}) >= len(nomes_features) ({len(nomes_features)})")
                    else:
                        print(f"❌ valores_aluno tem 0 elementos")
                else:
                    print(f"❌ valores_aluno_original não tem __len__")
            else:
                print(f"❌ Condições não atendidas")
            
        else:
            print(f"❌ valores_shap não tem __len__")
            
    except Exception as e:
        print(f"❌ Erro: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    debug_shap_processamento()