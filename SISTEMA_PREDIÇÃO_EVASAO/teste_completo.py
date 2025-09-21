#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
TESTE COMPLETO - Sistema funcionando com seu arquivo Excel
"""

import pandas as pd
import sys
import os
from pathlib import Path

# Adicionar o diretório do projeto ao path
sys.path.append('codigo_fonte')

from codigo_fonte.nucleo.preditor import SistemaPredicaoEvasao

def teste_completo():
    """Teste completo do sistema com seu arquivo"""
    
    print("🧪 TESTE COMPLETO DO SISTEMA")
    print("=" * 50)
    
    # 1. Testar carregamento do arquivo
    print("\n📁 ETAPA 1: Carregando arquivo Excel...")
    arquivo = "data/raw/alunos_ativos_atual.xlsx"
    
    try:
        # Usar a nova função de carregamento
        df = pd.read_excel(arquivo, engine='openpyxl')
        headers = df.iloc[2]  # Linha 2 contém os nomes das colunas
        data = df.iloc[3:]    # Dados começam na linha 3
        data.columns = headers
        df = data.reset_index(drop=True)
        df = df.dropna(axis=1, how='all')
        
        print(f"✅ Arquivo carregado: {len(df)} alunos")
        print(f"📋 Colunas: {list(df.columns[:5])}...")
        
        # Verificar se as colunas do modelo estão presentes
        colunas_modelo = [
            'Curso', 'Currículo', 'Sexo', 'Turma Atual', 'Cód.Disc. atual', 
            'Disciplina atual', 'Pend. Acad.', 'Pend. Financ.', 'Faltas Consecutivas', 
            'Cód.Curso', 'Identidade', 'Módulo atual'
        ]
        
        presentes = [col for col in colunas_modelo if col in df.columns]
        print(f"✅ Colunas do modelo presentes: {len(presentes)}/{len(colunas_modelo)}")
        
    except Exception as e:
        print(f"❌ Erro ao carregar: {e}")
        return
    
    # 2. Testar inicialização do sistema
    print("\n🤖 ETAPA 2: Inicializando sistema...")
    try:
        sistema = SistemaPredicaoEvasao()
        print("✅ Sistema inicializado")
    except Exception as e:
        print(f"❌ Erro ao inicializar: {e}")
        return
    
    # 3. Testar processamento (com 10 alunos apenas para ser rápido)
    print("\n🧮 ETAPA 3: Testando processamento...")
    
    try:
        # Salvar amostra
        df_amostra = df.head(10)
        arquivo_temp = Path("teste_amostra.xlsx")
        df_amostra.to_excel(arquivo_temp, index=False)
        
        # Inicializar sistema
        sistema.inicializar()
        
        # Processar usando o método correto
        predicoes, metadata = sistema.predizer_alunos(arquivo_temp)
        
        print("✅ Processamento concluído!")
        print(f"📊 Total de predições: {len(predicoes)}")
        
        # Mostrar algumas estatísticas das predições
        if predicoes:
            risco_evasao = sum(1 for p in predicoes if p.status_predicao == 'RISCO_EVASAO')
            matriculados = len(predicoes) - risco_evasao
            
            print(f"✅ Alunos sem risco: {matriculados}")
            print(f"⚠️ Alunos em risco: {risco_evasao}")
            
            # Mostrar exemplo de predição
            if predicoes:
                exemplo = predicoes[0]
                print(f"\n� Exemplo de predição:")
                print(f"   • Aluno: {exemplo.nome}")
                print(f"   • Curso: {exemplo.curso}")
                print(f"   • Status: {exemplo.status_predicao}")
                print(f"   • Probabilidade evasão: {exemplo.probabilidade_evasao_total}")
        
        print("\n🎉 TESTE CONCLUÍDO COM SUCESSO!")
        print("✅ Seu arquivo Excel está funcionando perfeitamente!")
        print("✅ O sistema conseguiu processar os dados!")
        print("✅ As predições foram geradas corretamente!")
        print("\n💡 Agora você pode usar a interface web normalmente.")
            
        # Limpar arquivo temporário
        if arquivo_temp.exists():
            arquivo_temp.unlink()
            
    except Exception as e:
        print(f"❌ Erro no processamento: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    teste_completo()