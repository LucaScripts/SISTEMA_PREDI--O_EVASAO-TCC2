#!/usr/bin/env python3
"""
Utilitário para diagnosticar e tentar reparar arquivos Excel problemáticos
"""

import pandas as pd
import os
import tempfile
import zipfile
import shutil

def diagnosticar_arquivo_excel(arquivo_path):
    """
    Diagnóstico completo de arquivo Excel problemático
    """
    print(f"🔍 DIAGNÓSTICO COMPLETO: {arquivo_path}")
    print("="*60)
    
    # 1. Verificações básicas
    if not os.path.exists(arquivo_path):
        print("❌ Arquivo não existe")
        return False
        
    tamanho = os.path.getsize(arquivo_path)
    print(f"📏 Tamanho: {tamanho:,} bytes")
    
    if tamanho == 0:
        print("❌ Arquivo vazio")
        return False
    
    # 2. Análise de header
    with open(arquivo_path, 'rb') as f:
        header = f.read(16)
        
    print(f"🔢 Header (hex): {header.hex()}")
    print(f"🔤 Header (repr): {repr(header)}")
    
    # 3. Detectar formato
    if header.startswith(b'PK\x03\x04'):
        print("✅ Formato: XLSX (ZIP válido)")
        return diagnosticar_xlsx(arquivo_path)
    elif header.startswith(b'\xd0\xcf\x11\xe0'):
        print("✅ Formato: XLS (OLE2 válido)")
        return diagnosticar_xls(arquivo_path)
    else:
        print("❌ Formato não reconhecido")
        print("💡 Sugestões:")
        print("   - Abrir no Excel e salvar como .xlsx")
        print("   - Verificar se o download foi completo")
        print("   - Usar outro arquivo de origem")
        return False

def diagnosticar_xlsx(arquivo_path):
    """Diagnóstico específico para arquivos XLSX"""
    print("\n📦 ANÁLISE XLSX (ZIP):")
    
    try:
        with zipfile.ZipFile(arquivo_path, 'r') as zip_file:
            arquivos = zip_file.namelist()
            print(f"✅ ZIP válido com {len(arquivos)} arquivos internos")
            
            # Verificar arquivos essenciais
            arquivos_essenciais = ['xl/workbook.xml', 'xl/sharedStrings.xml', '[Content_Types].xml']
            for arq in arquivos_essenciais:
                if arq in arquivos:
                    print(f"   ✅ {arq}")
                else:
                    print(f"   ⚠️ {arq} (pode estar ausente)")
            
            return True
            
    except zipfile.BadZipFile:
        print("❌ ZIP corrompido")
        return False
    except Exception as e:
        print(f"❌ Erro: {e}")
        return False

def diagnosticar_xls(arquivo_path):
    """Diagnóstico específico para arquivos XLS"""
    print("\n📊 ANÁLISE XLS (OLE2):")
    
    try:
        # Tentar ler com xlrd
        df_test = pd.read_excel(arquivo_path, engine='xlrd', nrows=1)
        print("✅ XLS válido e legível")
        return True
    except Exception as e:
        print(f"❌ Erro XLS: {e}")
        return False

def tentar_reparar_excel(arquivo_path):
    """
    Tenta reparar arquivo Excel problemático
    """
    print(f"\n🔧 TENTATIVA DE REPARO: {arquivo_path}")
    print("-"*40)
    
    # Estratégias de reparo
    estrategias = [
        "Copiar byte por byte para novo arquivo",
        "Extrair e recompactar ZIP (para XLSX)", 
        "Converter via pandas intermediário",
        "Criar novo arquivo com dados extraídos"
    ]
    
    # 1. Copiar byte por byte
    try:
        print("🔄 Estratégia 1: Cópia byte por byte...")
        arquivo_reparado = arquivo_path + ".reparado.xlsx"
        
        with open(arquivo_path, 'rb') as origem:
            with open(arquivo_reparado, 'wb') as destino:
                destino.write(origem.read())
        
        # Testar se funciona
        df_test = pd.read_excel(arquivo_reparado, nrows=1)
        print(f"✅ Reparo bem-sucedido: {arquivo_reparado}")
        return arquivo_reparado
        
    except Exception as e:
        print(f"❌ Falhou: {e}")
        try:
            os.remove(arquivo_reparado)
        except:
            pass
    
    # 2. Tentar extrair dados com múltiplos engines
    print("🔄 Estratégia 2: Extração multi-engine...")
    
    engines = ['openpyxl', 'xlrd', 'calamine', 'pyxlsb']
    for engine in engines:
        try:
            print(f"   Tentando engine {engine}...")
            df = pd.read_excel(arquivo_path, engine=engine)
            
            # Salvar como novo arquivo
            arquivo_limpo = arquivo_path + ".limpo.xlsx"
            df.to_excel(arquivo_limpo, index=False, engine='openpyxl')
            
            # Testar nova leitura
            df_test = pd.read_excel(arquivo_limpo, nrows=1)
            print(f"✅ Arquivo limpo criado: {arquivo_limpo}")
            return arquivo_limpo
            
        except ImportError:
            print(f"   ⚠️ Engine {engine} não disponível")
            continue
        except Exception as e:
            print(f"   ❌ {engine}: {e}")
            continue
    
    print("❌ Todas as estratégias de reparo falharam")
    return None

if __name__ == "__main__":
    # Teste com arquivo padrão
    arquivo = "data/raw/alunos_ativos_atual.xlsx"
    
    if os.path.exists(arquivo):
        sucesso = diagnosticar_arquivo_excel(arquivo)
        
        if not sucesso:
            arquivo_reparado = tentar_reparar_excel(arquivo)
            if arquivo_reparado:
                print(f"\n✅ Use este arquivo: {arquivo_reparado}")
    else:
        print(f"❌ Arquivo não encontrado: {arquivo}")
        print("💡 Coloque um arquivo Excel problemático neste local para testar")