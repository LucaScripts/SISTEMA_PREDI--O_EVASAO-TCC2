#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Script para debugar os valores SHAP no sistema de predição
"""
import sys
import os
sys.path.insert(0, os.getcwd())

from codigo_fonte.nucleo import SistemaPredicaoEvasao
from codigo_fonte.configuracao import configuracoes
from codigo_fonte.utilitarios import registrador
import pandas as pd

def debug_shap():
    print("🔍 DEBUGANDO VALORES SHAP")
    print("="*50)
    
    try:
        # Inicializar sistema
        sistema = SistemaPredicaoEvasao()
        sistema.inicializar()
        print("✅ Sistema inicializado")
        
        # Carregar dados usando o carregador correto
        from codigo_fonte.utilitarios.carregador_dados import CarregadorDados
        caminho_arquivo = configuracoes.dados.diretorio_dados_brutos / configuracoes.dados.arquivo_alunos
        df_original = CarregadorDados.carregar_excel_com_deteccao_cabecalho(caminho_arquivo)
        print(f"✅ Dados carregados: {len(df_original)} alunos")
        print(f"Colunas disponíveis: {list(df_original.columns)[:10]}...")  # Primeiras 10 colunas
        
        # Processar apenas alguns alunos para debug
        df_teste = df_original.head(3).copy()
        
        print("\n🎯 Testando função completa do sistema...")
        predicoes, estatisticas = sistema.predizer_alunos(caminho_arquivo)
        
        for i, resultado in enumerate(predicoes[:3]):
            print(f"\n--- Aluno {i+1} ---")
            print(f"Nome: {resultado.nome}")
            print(f"Fator Principal: {resultado.fator_principal}")
            print(f"Valor Importância: {resultado.valor_importancia}")
            print(f"Fonte: {resultado.fonte_predicao}")
            
    except Exception as e:
        print(f"❌ Erro: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    debug_shap()