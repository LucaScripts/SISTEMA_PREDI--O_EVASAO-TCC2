#!/usr/bin/env python3
"""
Teste específico para problemas de leitura de Excel com erros BOF
"""

import pandas as pd
import os
import tempfile
from interface_web import ler_excel_seguro, verificar_arquivo_excel

def testar_arquivo_problematico():
    """Testa a leitura com arquivo que pode estar dando problema"""
    
    arquivo_teste = "data/raw/alunos_ativos_atual.xlsx"
    
    print("🧪 TESTE ESPECÍFICO PARA PROBLEMA BOF")
    print("="*50)
    
    # 1. Verificar se o arquivo existe
    if not os.path.exists(arquivo_teste):
        print(f"❌ Arquivo não encontrado: {arquivo_teste}")
        return
    
    print(f"📁 Arquivo encontrado: {arquivo_teste}")
    print(f"📏 Tamanho: {os.path.getsize(arquivo_teste)} bytes")
    
    # 2. Análise de integridade
    print("\n🔍 ANÁLISE DE INTEGRIDADE:")
    info = verificar_arquivo_excel(arquivo_teste)
    print(f"   Válido: {info['valido']}")
    print(f"   Formato: {info['formato']}")
    if info['erro']:
        print(f"   Erro: {info['erro']}")
    if info['sugestoes']:
        print("   Sugestões:")
        for sugestao in info['sugestoes']:
            print(f"   - {sugestao}")
    
    # 3. Tentar leitura com nossa função robusta
    print("\n📊 TESTE DE LEITURA:")
    try:
        df = ler_excel_seguro(arquivo_teste, nrows=5)
        print(f"✅ Sucesso: {len(df)} linhas, {len(df.columns)} colunas")
        print(f"📋 Primeiras colunas: {list(df.columns[:5])}")
        print(f"📄 Primeira linha: {df.iloc[0].head(3).to_dict()}")
        
    except Exception as e:
        print(f"❌ Erro na leitura robusta: {str(e)}")
        
        # 4. Testes diretos com engines específicos
        print("\n🔧 TESTES DIRETOS:")
        
        engines = ['openpyxl', 'xlrd', None]
        for engine in engines:
            try:
                if engine:
                    df_test = pd.read_excel(arquivo_teste, engine=engine, nrows=2)
                    print(f"✅ Engine {engine}: {len(df_test.columns)} colunas")
                else:
                    df_test = pd.read_excel(arquivo_teste, nrows=2)
                    print(f"✅ Engine auto: {len(df_test.columns)} colunas")
            except Exception as e:
                print(f"❌ Engine {engine or 'auto'}: {str(e)}")
        
        # 5. Análise de headers
        print("\n📝 ANÁLISE DE HEADERS:")
        try:
            df_headers = pd.read_excel(arquivo_teste, header=None, nrows=5)
            for i in range(len(df_headers)):
                linha = df_headers.iloc[i]
                valores = [str(v) for v in linha.head(5) if pd.notna(v)]
                print(f"   Linha {i}: {' | '.join(valores)}")
        except Exception as e:
            print(f"❌ Erro na análise de headers: {str(e)}")

def testar_com_arquivo_temporario():
    """Testa criando arquivo temporário como na interface"""
    print("\n🔧 TESTE COM ARQUIVO TEMPORÁRIO:")
    print("-" * 30)
    
    arquivo_original = "data/raw/alunos_ativos_atual.xlsx"
    
    try:
        # Simular o que a interface faz
        with open(arquivo_original, 'rb') as f:
            dados = f.read()
        
        with tempfile.NamedTemporaryFile(delete=False, suffix='.xlsx') as tmp:
            tmp.write(dados)
            arquivo_temp = tmp.name
        
        print(f"📁 Arquivo temporário: {arquivo_temp}")
        
        # Testar leitura
        df = ler_excel_seguro(arquivo_temp, nrows=3)
        print(f"✅ Leitura temporária: {len(df)} linhas, {len(df.columns)} colunas")
        
        # Limpar
        os.unlink(arquivo_temp)
        
    except Exception as e:
        print(f"❌ Erro com arquivo temporário: {str(e)}")
        # Tentar limpar mesmo assim
        try:
            os.unlink(arquivo_temp)
        except:
            pass

if __name__ == "__main__":
    testar_arquivo_problematico()
    testar_com_arquivo_temporario()
    print("\n✅ TESTE CONCLUÍDO")