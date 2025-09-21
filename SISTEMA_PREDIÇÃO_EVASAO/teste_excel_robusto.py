#!/usr/bin/env python3
"""
Teste da função de leitura Excel robusta
"""

import sys
import os
from pathlib import Path

# Adicionar o diretório do projeto ao path
sys.path.append(str(Path(__file__).parent))

from interface_web import ler_excel_seguro, limpar_dataframe_para_streamlit

def testar_leitura_excel():
    """Testa a leitura de diferentes tipos de arquivo Excel"""
    
    # Arquivo de teste conhecido
    arquivo_teste = Path("data/raw/alunos_ativos_atual.xlsx")
    
    if not arquivo_teste.exists():
        print("❌ Arquivo de teste não encontrado:", arquivo_teste)
        return False
    
    print("🧪 Testando leitura Excel robusta...")
    
    try:
        # Testar leitura normal
        print("📊 1. Leitura completa...")
        df_completo = ler_excel_seguro(arquivo_teste)
        print(f"✅ Sucesso: {len(df_completo)} linhas, {len(df_completo.columns)} colunas")
        
        # Testar leitura com limite
        print("📊 2. Leitura com limite (5 linhas)...")
        df_limitado = ler_excel_seguro(arquivo_teste, nrows=5)
        print(f"✅ Sucesso: {len(df_limitado)} linhas, {len(df_limitado.columns)} colunas")
        
        # Testar limpeza para Streamlit
        print("📊 3. Limpeza para Streamlit...")
        df_limpo = limpar_dataframe_para_streamlit(df_limitado)
        print(f"✅ Sucesso: {len(df_limpo)} linhas, {len(df_limpo.columns)} colunas")
        
        # Mostrar informações das colunas
        print("\n📋 Colunas encontradas:")
        for i, col in enumerate(df_limpo.columns, 1):
            print(f"   {i:2d}. {col}")
            
        # Verificar tipos problemáticos
        print(f"\n🔍 Análise de tipos:")
        for col in df_limpo.columns:
            tipo = df_limpo[col].dtype
            valores_nulos = df_limpo[col].isnull().sum()
            print(f"   {col}: {tipo} (nulos: {valores_nulos})")
        
        print("\n🎉 Todos os testes passaram!")
        return True
        
    except Exception as e:
        print(f"❌ Erro nos testes: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("=" * 50)
    print("🧪 TESTE DE LEITURA EXCEL ROBUSTA")
    print("=" * 50)
    
    sucesso = testar_leitura_excel()
    
    if sucesso:
        print("\n✅ TESTE CONCLUÍDO COM SUCESSO")
    else:
        print("\n❌ TESTE FALHOU")
        sys.exit(1)