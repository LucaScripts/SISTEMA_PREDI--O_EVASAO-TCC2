#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🎯 CONFIGURAÇÃO ESPECÍFICA PARA A PLANILHA DO LUCAS
==================================================
Este arquivo contém a configuração otimizada para carregar
a planilha alunos_ativos_atual.xlsx corretamente.
"""

def carregar_planilha_lucas(arquivo_path):
    """
    Carrega a planilha do Lucas com configuração específica
    
    Args:
        arquivo_path: Caminho para alunos_ativos_atual.xlsx
        
    Returns:
        DataFrame com os dados carregados corretamente
    """
    import pandas as pd
    
    # Configuração específica baseada nos testes
    df = pd.read_excel(
        arquivo_path,
        engine='openpyxl',
        skiprows=2,  # Pula as 2 primeiras linhas (título e vazia)
        header=0     # Primeira linha após skiprows é o header
    )
    
    # Remover colunas completamente vazias
    df = df.dropna(axis=1, how='all')
    
    # Renomear colunas se necessário (mapear para nomes corretos)
    mapeamento_colunas = {
        # Mapeamento baseado na estrutura observada
        0: 'Matrícula',
        1: 'Nome', 
        2: 'Situação',
        3: 'Descrição',
        4: 'Pré-matrícula',
        5: 'Turma',
        6: 'Pend_Acad',
        7: 'Cod_Curso',
        8: 'Curso',
        9: 'Cod_Disc_atual',
        10: 'Disciplina_atual',
        11: 'Curriculo',
        12: 'Modulo'
        # Adicionar mais conforme necessário
    }
    
    # Aplicar mapeamento se as colunas estão como números
    if all(isinstance(col, int) or str(col).startswith('Unnamed') for col in df.columns):
        # Se temos colunas sem nome, usar os índices
        novas_colunas = []
        for i, col in enumerate(df.columns):
            if i in mapeamento_colunas:
                novas_colunas.append(mapeamento_colunas[i])
            else:
                novas_colunas.append(f'Coluna_{i+1}')
        df.columns = novas_colunas
    
    return df

def testar_configuracao():
    """Testa a configuração específica"""
    import os
    
    arquivo = r"c:\Users\lucas\Downloads\TCC2\alunos_ativos_atual.xlsx"
    
    if not os.path.exists(arquivo):
        print(f"❌ Arquivo não encontrado: {arquivo}")
        return False
    
    print("🎯 TESTANDO CONFIGURAÇÃO ESPECÍFICA")
    print("=" * 50)
    
    try:
        df = carregar_planilha_lucas(arquivo)
        
        print(f"✅ Sucesso!")
        print(f"📊 Dimensões: {len(df)} alunos × {len(df.columns)} colunas")
        
        print(f"\n📋 COLUNAS CORRIGIDAS:")
        for i, col in enumerate(df.columns, 1):
            print(f"   {i:2d}. {col}")
        
        print(f"\n👥 PRIMEIROS 3 ALUNOS:")
        print("=" * 80)
        
        # Mostrar apenas colunas principais
        colunas_principais = ['Matrícula', 'Nome', 'Situação', 'Curso']
        colunas_existentes = [col for col in colunas_principais if col in df.columns]
        
        if colunas_existentes:
            preview = df[colunas_existentes].head(3)
            print(preview.to_string(index=False))
        else:
            # Mostrar primeiras 6 colunas
            preview = df.iloc[:3, :6]
            print(preview.to_string(index=False))
        
        return True, df
        
    except Exception as e:
        print(f"❌ Erro: {str(e)}")
        return False, None

if __name__ == "__main__":
    success, df = testar_configuracao()
    if success:
        print(f"\n🎉 CONFIGURAÇÃO FUNCIONANDO!")
        print(f"💡 Use esta função na interface web!")
    else:
        print(f"\n⚠️ Ajustes necessários")
    
    input("\nPressione Enter para continuar...")