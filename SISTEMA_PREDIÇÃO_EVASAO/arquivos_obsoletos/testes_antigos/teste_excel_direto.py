#!/usr/bin/env python3
"""
Teste direto do problema do Excel
"""

import pandas as pd
import sys
from pathlib import Path

def testar_leitura_direta():
    arquivo = "data/raw/alunos_ativos_atual.xlsx"
    
    print("🧪 Testando diferentes formas de ler o Excel...")
    
    try:
        # 1. Leitura padrão
        print("\n📊 1. Leitura padrão (header=0):")
        df1 = pd.read_excel(arquivo, nrows=3)
        print(f"   Colunas: {list(df1.columns[:3])}")
        print(f"   Linha 0: {df1.iloc[0].head(3).to_dict()}")
        
        # 2. Com header=3 
        print("\n📊 2. Com header=3:")
        df3 = pd.read_excel(arquivo, header=3, nrows=3)
        print(f"   Colunas: {list(df3.columns[:3])}")
        print(f"   Linha 0: {df3.iloc[0].head(3).to_dict()}")
        
        return df3
        
    except Exception as e:
        print(f"❌ Erro: {e}")
        return None

if __name__ == "__main__":
    df = testar_leitura_direta()
    if df is not None:
        print(f"\n✅ Melhor resultado: {len(df)} linhas, {len(df.columns)} colunas")
        print(f"Primeiras colunas: {list(df.columns[:5])}")
    else:
        print("\n❌ Falhou")