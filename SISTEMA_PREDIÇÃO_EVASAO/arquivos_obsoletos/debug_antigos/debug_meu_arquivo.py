#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Debug específico do arquivo Excel do Lucas
"""

import pandas as pd
import os
import sys

def debug_arquivo_excel():
    """Debugar arquivo Excel específico"""
    
    # Localizar arquivo
    data_dir = "data/raw"
    arquivos_excel = [f for f in os.listdir(data_dir) if f.endswith(('.xlsx', '.xls'))]
    
    print("🔍 ARQUIVOS ENCONTRADOS:")
    for i, arquivo in enumerate(arquivos_excel):
        print(f"{i+1}. {arquivo}")
    
    # Usar o primeiro arquivo encontrado
    if arquivos_excel:
        arquivo_path = os.path.join(data_dir, arquivos_excel[0])
        print(f"\n📁 TESTANDO: {arquivo_path}")
        
        try:
            # Tentar ler como AcadWeb (formato que funciona)
            df = pd.read_excel(arquivo_path, skiprows=2, header=0, engine='openpyxl')
            print(f"✅ ARQUIVO CARREGADO: {len(df)} linhas, {len(df.columns)} colunas")
            
            print("\n📋 COLUNAS PRESENTES:")
            for i, col in enumerate(df.columns):
                print(f"{i+1:2d}. '{col}'")
            
            # Colunas que o modelo precisa
            colunas_modelo = [
                'Curso', 'Currículo', 'Sexo', 'Turma Atual', 'Cód.Disc. atual', 
                'Disciplina atual', 'Pend. Acad.', 'Pend. Financ.', 'Faltas Consecutivas', 
                'Cód.Curso', 'Identidade', 'Módulo atual'
            ]
            
            print(f"\n🤖 ANÁLISE PARA MODELO ML (precisa de {len(colunas_modelo)} colunas):")
            
            presentes = []
            faltantes = []
            
            for col in colunas_modelo:
                if col in df.columns:
                    presentes.append(col)
                    print(f"✅ '{col}' - PRESENTE")
                else:
                    faltantes.append(col)
                    print(f"❌ '{col}' - FALTANTE")
            
            print(f"\n📊 RESUMO:")
            print(f"✅ Presentes: {len(presentes)}/{len(colunas_modelo)} ({len(presentes)/len(colunas_modelo)*100:.1f}%)")
            print(f"❌ Faltantes: {len(faltantes)}/{len(colunas_modelo)}")
            
            if faltantes:
                print(f"\n💡 COLUNAS QUE PRECISAM SER CRIADAS:")
                for col in faltantes:
                    print(f"   • {col}")
            
            # Verificar possíveis variações
            print(f"\n🔍 BUSCANDO VARIAÇÕES:")
            
            # Mapeamento de variações
            variações = {
                'Currículo': ['Curriculo', 'Currículo', 'CURRÍCULO', 'CURRICULO'],
                'Pend. Acad.': ['Pend.Acad.', 'Pend. Acad', 'Pendências Acadêmicas', 'Pend Acad'],
                'Pend. Financ.': ['Pend.Financ.', 'Pend. Financ', 'Pendências Financeiras', 'Pend Financ'],
                'Faltas Consecutivas': ['Faltas', 'Faltas Consec.', 'Faltas Consecutivas'],
                'Sexo': ['Gênero', 'Genero', 'SEXO'],
                'Turma Atual': ['Turma', 'Turma Atual'],
                'Cód.Disc. atual': ['Cod.Disc.atual', 'Código Disciplina Atual', 'Cód Disc atual'],
                'Disciplina atual': ['Disciplina Atual', 'Disciplina'],
                'Cód.Curso': ['Cod.Curso', 'Código Curso', 'Cód Curso'],
                'Módulo atual': ['Modulo atual', 'Módulo Atual', 'Modulo Atual']
            }
            
            for col_modelo, possíveis in variações.items():
                if col_modelo not in presentes:  # só verificar se não está presente
                    for possível in possíveis:
                        if possível in df.columns:
                            print(f"🔄 '{col_modelo}' pode ser mapeado de '{possível}'")
                            break
            
            print(f"\n🎯 PRIMEIRAS 3 LINHAS:")
            print(df.head(3).to_string())
            
        except Exception as e:
            print(f"❌ ERRO: {e}")
            
            # Tentar ler só as primeiras linhas para ver a estrutura
            try:
                print(f"\n🔍 TENTANDO LER PRIMEIRAS 10 LINHAS SEM SKIPROWS:")
                df_raw = pd.read_excel(arquivo_path, nrows=10, engine='openpyxl')
                print(df_raw.to_string())
            except Exception as e2:
                print(f"❌ ERRO TAMBÉM: {e2}")

if __name__ == "__main__":
    debug_arquivo_excel()