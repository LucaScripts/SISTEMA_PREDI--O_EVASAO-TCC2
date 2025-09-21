#!/usr/bin/env python3
"""
Script para testar qualquer arquivo Excel que você queira importar
"""

import pandas as pd
import os
import sys
from pathlib import Path

def testar_arquivo_usuario():
    """
    Teste interativo para qualquer arquivo Excel
    """
    print("🔍 TESTE DE ARQUIVO EXCEL PERSONALIZADO")
    print("="*50)
    
    # Pedir caminho do arquivo
    while True:
        arquivo = input("\n📁 Digite o caminho completo do arquivo Excel: ").strip().strip('"')
        
        if not arquivo:
            print("❌ Caminho vazio. Tente novamente.")
            continue
            
        if not os.path.exists(arquivo):
            print(f"❌ Arquivo não encontrado: {arquivo}")
            print("💡 Dica: Arraste o arquivo para esta janela para obter o caminho completo")
            continue
        
        break
    
    # Análise básica
    tamanho = os.path.getsize(arquivo)
    print(f"\n📏 Tamanho: {tamanho:,} bytes")
    
    # Verificar header
    with open(arquivo, 'rb') as f:
        header = f.read(16)
    
    print(f"🔢 Header: {header.hex()}")
    
    # Detectar formato
    if header.startswith(b'PK\x03\x04'):
        formato = "XLSX (ZIP válido)"
        cor = "✅"
    elif header.startswith(b'\xd0\xcf\x11\xe0'):
        formato = "XLS (OLE2 válido)" 
        cor = "✅"
    else:
        formato = "❌ FORMATO NÃO RECONHECIDO"
        cor = "❌"
    
    print(f"{cor} Formato detectado: {formato}")
    
    if formato.startswith("❌"):
        print("\n🚨 ARQUIVO COM PROBLEMA DETECTADO!")
        print("💡 Soluções:")
        print("   1. Abra no Excel e salve como .xlsx")
        print("   2. Verifique se não é um CSV renomeado")
        print("   3. Baixe novamente o arquivo original")
        return False
    
    # Tentar leitura com diferentes estratégias
    print(f"\n📊 TENTATIVAS DE LEITURA:")
    
    estrategias = [
        {"nome": "Pandas padrão", "kwargs": {}},
        {"nome": "Engine openpyxl", "kwargs": {"engine": "openpyxl"}},
        {"nome": "Engine xlrd", "kwargs": {"engine": "xlrd"}},
        {"nome": "Header linha 1", "kwargs": {"header": 1}},
        {"nome": "Header linha 2", "kwargs": {"header": 2}},
        {"nome": "Header linha 3", "kwargs": {"header": 3}},
        {"nome": "Sem header", "kwargs": {"header": None}},
    ]
    
    sucessos = []
    
    for i, estrategia in enumerate(estrategias, 1):
        try:
            print(f"   {i}. {estrategia['nome']}... ", end="")
            df = pd.read_excel(arquivo, nrows=3, **estrategia['kwargs'])
            print(f"✅ {len(df)} linhas, {len(df.columns)} colunas")
            
            # Mostrar preview das colunas
            colunas = list(df.columns)[:5]
            print(f"      Colunas: {colunas}")
            
            # Se tem dados válidos, guardar
            if len(df) > 0 and len(df.columns) > 2:
                sucessos.append((estrategia, df))
                
        except Exception as e:
            print(f"❌ {str(e)[:60]}...")
    
    # Mostrar melhor resultado
    if sucessos:
        print(f"\n🎉 SUCESSOS ENCONTRADOS: {len(sucessos)}")
        
        melhor = sucessos[0]
        estrategia, df = melhor
        
        print(f"\n✅ MELHOR RESULTADO ({estrategia['nome']}):")
        print(f"📊 Dimensões: {len(df)} linhas × {len(df.columns)} colunas")
        print(f"📋 Colunas: {list(df.columns)}")
        
        if len(df) > 0:
            print(f"\n📄 PRIMEIRA LINHA:")
            for col in df.columns[:8]:  # Mostrar primeiras 8 colunas
                valor = df.iloc[0][col]
                print(f"   {col}: {valor}")
        
        # Sugerir configuração para a interface
        print(f"\n💡 CONFIGURAÇÃO SUGERIDA PARA A INTERFACE:")
        if estrategia['kwargs']:
            for key, value in estrategia['kwargs'].items():
                print(f"   {key}: {value}")
        
        return True
    else:
        print(f"\n❌ NENHUMA ESTRATÉGIA FUNCIONOU")
        print("🔧 O arquivo pode estar severamente corrompido")
        print("💡 Tente:")
        print("   1. Abrir no Excel manualmente")
        print("   2. Salvar como novo arquivo .xlsx")
        print("   3. Verificar se há dados na primeira aba")
        return False

if __name__ == "__main__":
    print("📋 Este script testa qualquer arquivo Excel")
    print("💡 Arraste o arquivo para a janela ou digite o caminho completo")
    
    try:
        testar_arquivo_usuario()
    except KeyboardInterrupt:
        print("\n\n🔴 Teste cancelado pelo usuário")
    except Exception as e:
        print(f"\n❌ Erro inesperado: {e}")
    
    input("\n⏸️ Pressione Enter para sair...")