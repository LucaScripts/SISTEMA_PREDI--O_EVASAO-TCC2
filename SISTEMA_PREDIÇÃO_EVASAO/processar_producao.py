#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Script de produção para processar automaticamente arquivos na pasta input
"""
import sys
import os
import glob
from pathlib import Path
from datetime import datetime

# Adicionar o caminho do projeto
sys.path.insert(0, os.getcwd())

from codigo_fonte.nucleo import SistemaPredicaoEvasao
from codigo_fonte.configuracao import configuracoes
from codigo_fonte.utilitarios import registrador

def processar_arquivo_automatico():
    """Processa automaticamente arquivos da pasta input"""
    
    # Criar diretórios se não existirem
    input_dir = Path("input")
    output_dir = Path("output")
    input_dir.mkdir(exist_ok=True)
    output_dir.mkdir(exist_ok=True)
    
    try:
        print("🔍 Procurando arquivos Excel na pasta 'input'...")
        
        # Buscar arquivos Excel
        arquivos_excel = list(input_dir.glob("*.xlsx"))
        
        if not arquivos_excel:
            print("❌ Nenhum arquivo Excel encontrado na pasta 'input'")
            print("\n📋 INSTRUÇÕES:")
            print("1. Coloque seu arquivo Excel (.xlsx) na pasta 'input'")
            print("2. Execute este script novamente")
            return False
        
        # Processar o primeiro arquivo encontrado
        arquivo_entrada = arquivos_excel[0]
        print(f"📁 Processando: {arquivo_entrada.name}")
        
        # Inicializar sistema
        print("🤖 Inicializando sistema de predição...")
        sistema = SistemaPredicaoEvasao()
        sistema.inicializar()
        print("✅ Sistema inicializado com sucesso")
        
        # Fazer predições
        print("🧠 Processando predições...")
        predicoes, estatisticas = sistema.predizer_alunos(arquivo_entrada)
        
        # Gerar nome do arquivo de saída
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        nome_arquivo_saida = f"predicao_evasao_{timestamp}.csv"
        arquivo_saida = output_dir / nome_arquivo_saida
        
        # Salvar CSV
        print("💾 Salvando resultados...")
        import csv
        
        with open(arquivo_saida, 'w', newline='', encoding='utf-8-sig') as arquivo_csv:
            escritor = csv.writer(arquivo_csv)
            
            # Cabeçalho
            escritor.writerow([
                'Nome', 'Matricula', 'Situacao_Atual_Sistema', 'Curso', 'Sexo', 'Turma',
                'Status_Predicao', 'Situacao_Predita', 'Probabilidade_Situacao',
                'Probabilidade_Evasao_Total', 'Nivel_Urgencia', 'Fator_Principal',
                'Valor_Importancia', 'Confianca_Predicao', 'Fonte_Predicao',
                'Data_Processamento'
            ])
            
            # Dados
            for predicao in predicoes:
                escritor.writerow([
                    predicao.nome, predicao.matricula, predicao.situacao_atual,
                    predicao.curso, predicao.sexo, predicao.turma,
                    predicao.status_predicao, predicao.situacao_predita,
                    predicao.probabilidade_situacao, predicao.probabilidade_evasao_total,
                    predicao.nivel_urgencia, predicao.fator_principal,
                    abs(predicao.valor_importancia), predicao.confianca_predicao,
                    predicao.fonte_predicao, datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                ])
        
        # Estatísticas finais
        total_alunos = len(predicoes)
        matriculados = len([p for p in predicoes if p.status_predicao == 'MATRICULADO'])
        em_risco = len([p for p in predicoes if p.status_predicao == 'RISCO_EVASAO'])
        urgentes = len([p for p in predicoes if p.nivel_urgencia == 'URGENTE'])
        
        print("\n" + "="*50)
        print("📊 RESUMO DOS RESULTADOS:")
        print("="*50)
        print(f"📁 Arquivo processado: {arquivo_entrada.name}")
        print(f"👥 Total de alunos: {total_alunos}")
        print(f"✅ Matriculados: {matriculados} ({(matriculados/total_alunos)*100:.1f}%)")
        print(f"⚠️  Em risco: {em_risco} ({(em_risco/total_alunos)*100:.1f}%)")
        print(f"🚨 Casos urgentes: {urgentes}")
        print(f"💾 Arquivo gerado: {arquivo_saida}")
        print("="*50)
        
        # Mover arquivo processado para subpasta
        processed_dir = input_dir / "processados"
        processed_dir.mkdir(exist_ok=True)
        novo_nome = processed_dir / f"{arquivo_entrada.stem}_processado_{timestamp}.xlsx"
        arquivo_entrada.rename(novo_nome)
        print(f"📁 Arquivo original movido para: {novo_nome}")
        
        return True
        
    except Exception as e:
        print(f"\n❌ ERRO durante processamento:")
        print(f"   {str(e)}")
        registrador.error(f"Erro no processamento automático: {e}")
        return False

if __name__ == "__main__":
    sucesso = processar_arquivo_automatico()
    if not sucesso:
        sys.exit(1)