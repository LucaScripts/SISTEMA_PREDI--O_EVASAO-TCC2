#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🎯 TESTE COMPLETO DA SUA PLANILHA ESPECÍFICA
===========================================
Lucas, este script testa especificamente sua planilha alunos_ativos_atual.xlsx
com a configuração correta (header na linha 2/índice 2).
"""

import pandas as pd
import os
import sys
from pathlib import Path

def teste_planilha_completa():
    """Testa sua planilha específica com configuração otimizada"""
    
    print("🎯 TESTE ESPECÍFICO DA SUA PLANILHA")
    print("=" * 50)
    
    # Caminho da sua planilha
    arquivo = r"c:\Users\lucas\Downloads\TCC2\alunos_ativos_atual.xlsx"
    
    if not os.path.exists(arquivo):
        print(f"❌ Arquivo não encontrado: {arquivo}")
        print("💡 Verificando outros locais possíveis...")
        
        # Tentar outros caminhos
        outros_caminhos = [
            r"C:\Users\lucas\Downloads\TCC2\SISTEMA_PREDIÇÃO_EVASAO TCC2\SISTEMA_PREDIÇÃO_EVASAO\data\raw\alunos_ativos_atual.xlsx",
            r"C:\Users\lucas\Downloads\TCC2\SISTEMA_PREDIÇÃO_EVASAO\data\raw\alunos_ativos_atual.xlsx"
        ]
        
        for caminho in outros_caminhos:
            if os.path.exists(caminho):
                arquivo = caminho
                print(f"✅ Encontrado em: {arquivo}")
                break
        else:
            print("❌ Arquivo não encontrado em nenhum local")
            return False
    
    print(f"📁 Arquivo: {os.path.basename(arquivo)}")
    print(f"📏 Tamanho: {os.path.getsize(arquivo):,} bytes")
    
    print("\n🔍 TESTANDO CONFIGURAÇÃO CORRETA:")
    print("   Header na linha 2 (índice 2 - linha 3 do Excel)")
    
    try:
        # Configuração correta baseada no seu teste
        df = pd.read_excel(arquivo, header=2, engine='openpyxl')
        
        print(f"✅ Sucesso!")
        print(f"📊 Dimensões: {len(df)} alunos × {len(df.columns)} colunas")
        
        print(f"\n📋 COLUNAS DETECTADAS:")
        for i, col in enumerate(df.columns, 1):
            print(f"   {i:2d}. {col}")
        
        print(f"\n👥 PRIMEIROS 5 ALUNOS:")
        print("=" * 80)
        
        colunas_principais = ['Matrícula', 'Nome', 'Situação', 'Curso']
        colunas_existentes = [col for col in colunas_principais if col in df.columns]
        
        if colunas_existentes:
            preview = df[colunas_existentes].head()
            print(preview.to_string(index=False))
        else:
            # Se não encontrou as colunas esperadas, mostrar todas
            preview = df.head()
            print(preview.to_string(index=False, max_cols=6))
        
        print(f"\n📈 ESTATÍSTICAS:")
        print(f"   • Total de alunos: {len(df):,}")
        print(f"   • Colunas: {len(df.columns)}")
        
        # Verificar situações
        if 'Situação' in df.columns:
            situacoes = df['Situação'].value_counts()
            print(f"   • Situações encontradas:")
            for situacao, count in situacoes.head().items():
                print(f"     - {situacao}: {count:,} alunos")
        
        # Verificar cursos
        if 'Curso' in df.columns:
            cursos = df['Curso'].value_counts()
            print(f"   • Top 3 cursos:")
            for curso, count in cursos.head(3).items():
                print(f"     - {curso}: {count:,} alunos")
        
        print(f"\n🎯 CONFIGURAÇÃO PARA A INTERFACE:")
        print(f"   📝 Arquivo: {arquivo}")
        print(f"   🔢 Header: linha 2 (índice 2)")
        print(f"   ⚙️  Engine: openpyxl")
        print(f"   ✅ Resultado: {len(df):,} alunos carregados")
        
        return True
        
    except Exception as e:
        print(f"❌ Erro: {str(e)}")
        print(f"\n🔧 Tentando estratégias alternativas...")
        
        # Tentar outras estratégias
        estrategias = [
            {"header": 1, "engine": "openpyxl"},
            {"header": 3, "engine": "openpyxl"},
            {"header": 2},  # Sem engine específico
            {"header": None, "skiprows": 2},
        ]
        
        for i, kwargs in enumerate(estrategias, 1):
            try:
                print(f"   Tentativa {i}: {kwargs}... ", end="")
                df_alt = pd.read_excel(arquivo, **kwargs)
                print(f"✅ {len(df_alt)} linhas")
                
                if len(df_alt) > 100:  # Se tem muitos dados
                    print(f"   → Colunas: {list(df_alt.columns)[:3]}")
                    
            except Exception as e2:
                print(f"❌ {str(e2)[:40]}...")
        
        return False

def main():
    """Função principal"""
    
    print("🚀 Executando teste completo da planilha...")
    print()
    
    if teste_planilha_completa():
        print("\n🎉 TESTE CONCLUÍDO COM SUCESSO!")
        print("💡 A planilha está pronta para usar na interface web!")
    else:
        print("\n⚠️ Problemas encontrados.")
        print("💡 Verifique o caminho do arquivo ou entre em contato.")
    
    print("\n" + "="*50)
    print("Pressione Enter para finalizar...")
    input()

if __name__ == "__main__":
    main()