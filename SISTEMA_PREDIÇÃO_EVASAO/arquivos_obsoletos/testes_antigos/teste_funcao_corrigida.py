#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Teste rápido da função corrigida
"""

import pandas as pd
import os

def carregar_planilha_acadweb_teste(arquivo):
    """Função de teste"""
    try:
        # Ler arquivo detectando automaticamente os cabeçalhos na linha 2 (índice 2)
        df = pd.read_excel(arquivo, engine='openpyxl')
        
        print(f"🔍 Total de linhas no arquivo: {len(df)}")
        print(f"🔍 Linha 2 (cabeçalhos): {list(df.iloc[2].values[:10])}")
        
        # Os cabeçalhos estão na linha índice 2
        headers = df.iloc[2]  # Linha 2 contém os nomes das colunas
        data = df.iloc[3:]    # Dados começam na linha 3
        
        # Aplicar cabeçalhos
        data.columns = headers
        df = data.reset_index(drop=True)
        
        print(f"📊 Dados carregados: {len(df)} linhas, {len(df.columns)} colunas")
        print(f"📋 Primeiras 10 colunas: {list(df.columns[:10])}")
        
        # Verificar colunas do modelo
        colunas_modelo = [
            'Curso', 'Currículo', 'Sexo', 'Turma Atual', 'Cód.Disc. atual', 
            'Disciplina atual', 'Pend. Acad.', 'Pend. Financ.', 'Faltas Consecutivas', 
            'Cód.Curso', 'Identidade', 'Módulo atual'
        ]
        
        presentes = [col for col in colunas_modelo if col in df.columns]
        faltantes = [col for col in colunas_modelo if col not in df.columns]
        
        print(f"✅ Colunas presentes ({len(presentes)}):")
        for col in presentes:
            print(f"   • {col}")
            
        print(f"❌ Colunas faltantes ({len(faltantes)}):")
        for col in faltantes:
            print(f"   • {col}")
        
        return df
        
    except Exception as e:
        print(f"❌ Erro: {e}")
        return None

if __name__ == "__main__":
    arquivo = "data/raw/alunos_ativos_atual.xlsx"
    df = carregar_planilha_acadweb_teste(arquivo)