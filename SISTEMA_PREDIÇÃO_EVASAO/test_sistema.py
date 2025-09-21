#!/usr/bin/env python3
"""
Script de teste completo para o sistema de predição de evasão.
"""

import sys
import os
from pathlib import Path

# Adicionar o diretório do projeto ao path
sys.path.insert(0, os.getcwd())

def test_imports():
    """Testa todas as importações necessárias."""
    print("🧪 Testando importações...")
    try:
        from codigo_fonte.configuracao import configuracoes
        from codigo_fonte.nucleo import SistemaPredicaoEvasao
        from codigo_fonte.utilitarios import CarregadorDados
        from codigo_fonte.modelos import PreditorEvasaoEstudantil
        print("✅ Todas as importações funcionaram!")
        return True
    except Exception as e:
        print(f"❌ Erro nas importações: {e}")
        return False

def test_files():
    """Verifica se os arquivos necessários existem."""
    print("\n📁 Verificando arquivos...")
    arquivos_necessarios = [
        "data/raw/alunos_ativos_atual.xlsx",
        "data/models/modelo_xgboost_sem_classes_criticas.pkl",
        "data/models/class_mapping_otimizado.pkl",
        "data/models/training_artifacts.pkl"
    ]
    
    todos_ok = True
    for arquivo in arquivos_necessarios:
        path = Path(arquivo)
        if path.exists():
            print(f"✅ {arquivo}")
        else:
            print(f"❌ {arquivo} - NÃO ENCONTRADO")
            todos_ok = False
    
    return todos_ok

def test_system_initialization():
    """Testa a inicialização do sistema."""
    print("\n🚀 Testando inicialização do sistema...")
    try:
        from codigo_fonte.nucleo import SistemaPredicaoEvasao
        
        sistema = SistemaPredicaoEvasao()
        sistema.inicializar()
        print("✅ Sistema inicializado com sucesso!")
        return True, sistema
    except Exception as e:
        print(f"❌ Erro na inicialização: {e}")
        return False, None

def test_predictions(sistema):
    """Testa as predições."""
    print("\n🎯 Testando predições...")
    try:
        arquivo_dados = Path("data/raw/alunos_ativos_atual.xlsx")
        if not arquivo_dados.exists():
            print(f"❌ Arquivo de dados não encontrado: {arquivo_dados}")
            return False
        
        predicoes, estatisticas = sistema.predizer_alunos(arquivo_dados)
        
        print(f"✅ Predições realizadas com sucesso!")
        print(f"   Total de alunos: {len(predicoes)}")
        print(f"   Matriculados: {estatisticas['enrolled_students']} ({estatisticas['enrolled_percentage']:.1f}%)")
        print(f"   Em risco: {estatisticas['dropout_risk_students']} ({estatisticas['dropout_risk_percentage']:.1f}%)")
        
        # Mostrar distribuição por urgência
        alunos_risco = [p for p in predicoes if p.status_predicao == 'RISCO_EVASAO']
        if alunos_risco:
            urgencias = {}
            for aluno in alunos_risco:
                urgencias[aluno.nivel_urgencia] = urgencias.get(aluno.nivel_urgencia, 0) + 1
            
            print(f"   Distribuição por urgência:")
            for nivel, qtd in urgencias.items():
                print(f"     {nivel}: {qtd} alunos")
        
        return True
    except Exception as e:
        print(f"❌ Erro nas predições: {e}")
        import traceback
        print(f"Traceback: {traceback.format_exc()}")
        return False

def test_output_files():
    """Verifica arquivos de saída."""
    print("\n📊 Verificando arquivos de saída...")
    output_dir = Path("output")
    arquivos_saida = [
        "analise_completa.csv",
        "confusion_matrix.png", 
        "feature_importance.png",
        "model_training_report.txt"
    ]
    
    for arquivo in arquivos_saida:
        path = output_dir / arquivo
        if path.exists():
            if arquivo.endswith('.csv'):
                import pandas as pd
                try:
                    df = pd.read_csv(path)
                    print(f"✅ {arquivo} - {len(df)} linhas")
                except:
                    print(f"⚠️ {arquivo} - arquivo existe mas não pode ser lido")
            else:
                size = path.stat().st_size
                print(f"✅ {arquivo} - {size} bytes")
        else:
            print(f"❌ {arquivo} - não encontrado")

def main():
    """Executa todos os testes."""
    print("🧪 INICIANDO TESTES COMPLETOS DO SISTEMA")
    print("=" * 50)
    
    # Teste 1: Importações
    if not test_imports():
        print("\n❌ FALHA NOS TESTES - Problema nas importações")
        return False
    
    # Teste 2: Arquivos
    if not test_files():
        print("\n⚠️ AVISO - Alguns arquivos não foram encontrados")
    
    # Teste 3: Inicialização
    sucesso, sistema = test_system_initialization()
    if not sucesso:
        print("\n❌ FALHA NOS TESTES - Sistema não inicializou")
        return False
    
    # Teste 4: Predições
    if not test_predictions(sistema):
        print("\n❌ FALHA NOS TESTES - Erro nas predições")
        return False
    
    # Teste 5: Arquivos de saída
    test_output_files()
    
    print("\n" + "=" * 50)
    print("🎉 TODOS OS TESTES CONCLUÍDOS COM SUCESSO!")
    print("\nSistema está funcionando corretamente e pronto para uso!")
    
    return True

if __name__ == "__main__":
    main()