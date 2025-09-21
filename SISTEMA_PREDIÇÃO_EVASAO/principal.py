#!/usr/bin/env python3
"""
Sistema de Predição de Evasão Estudantil - Versão em Português

Este é o arquivo principal do sistema híbrido que combina Machine Learning
com regras de negócio para identificar alunos em risco de evasão escolar.

Desenvolvido para Grau Técnico - 2025

Uso:
    python principal.py                    # Usar arquivo padrão
    python principal.py arquivo.xlsx      # Especificar arquivo
    python principal.py --verbose         # Modo detalhado
    python principal.py --ajuda          # Mostrar ajuda

Exemplo:
    python principal.py dados/brutos/alunos_ativos_atual.xlsx --verbose
"""

import sys
import argparse
from pathlib import Path
from typing import List
import csv

from codigo_fonte.utilitarios import obter_registrador
from codigo_fonte.configuracao import configuracoes
from codigo_fonte.nucleo import SistemaPredicaoEvasao, PredicaoAluno

def configurar_argumentos() -> argparse.ArgumentParser:
    """
    Configura os argumentos da linha de comando.
    
    Returns:
        Parser configurado
    """
    parser = argparse.ArgumentParser(
        description='Sistema de Predição de Evasão Estudantil',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Exemplos:
  python principal.py                              # Arquivo padrão
  python principal.py arquivo_alunos.xlsx         # Arquivo específico
  python principal.py --verboso                   # Modo detalhado
  python principal.py arquivo.xlsx --verboso      # Arquivo específico + verbose
        """
    )
    
    parser.add_argument(
        'arquivo_alunos',
        nargs='?',
        help='Arquivo Excel com dados dos alunos (padrão: data/raw/alunos_ativos_atual.xlsx)'
    )
    
    parser.add_argument(
        '--verboso', '-v',
        action='store_true',
        help='Modo verboso para debugging'
    )
    
    return parser

def salvar_predicoes_em_csv(predicoes: List[PredicaoAluno], arquivo_saida: Path) -> None:
    """
    Salva as predições em arquivo CSV.
    
    Args:
        predicoes: Lista de predições dos alunos
        arquivo_saida: Caminho do arquivo de saída
    """
    with open(arquivo_saida, 'w', newline='', encoding='utf-8') as csvfile:
        # Definir cabeçalhos
        cabecalhos = [
            'Nome', 'Matricula', 'Situacao_Atual_Sistema', 'Curso', 'Sexo', 'Turma',
            'Status_Predicao', 'Situacao_Predita', 'Probabilidade_Situacao',
            'Probabilidade_Evasao_Total', 'Nivel_Urgencia', 'Fator_Principal',
            'Valor_Importancia', 'Confianca_Predicao', 'Fonte_Predicao',
            'Predicao_ML_Original', 'Prob_ML_Original',
            'Top_1_Situacao_ML', 'Top_1_Probabilidade_ML',
            'Top_2_Situacao_ML', 'Top_2_Probabilidade_ML',
            'Top_3_Situacao_ML', 'Top_3_Probabilidade_ML'
        ]
        
        escritor = csv.writer(csvfile)
        escritor.writerow(cabecalhos)
        
        # Escrever dados
        for predicao in predicoes:
            linha = [
                predicao.nome, predicao.matricula, predicao.situacao_atual,
                predicao.curso, predicao.sexo, predicao.turma,
                predicao.status_predicao, predicao.situacao_predita,
                predicao.probabilidade_situacao, predicao.probabilidade_evasao_total,
                predicao.nivel_urgencia, predicao.fator_principal,
                predicao.valor_importancia, predicao.confianca_predicao,
                predicao.fonte_predicao, predicao.predicao_ml_original,
                predicao.prob_ml_original, predicao.top_1_situacao_ml,
                predicao.top_1_probabilidade_ml, predicao.top_2_situacao_ml,
                predicao.top_2_probabilidade_ml, predicao.top_3_situacao_ml,
                predicao.top_3_probabilidade_ml
            ]
            escritor.writerow(linha)

def imprimir_relatorio_resumo(predicoes: List[PredicaoAluno], estatisticas: dict) -> None:
    """
    Imprime relatório resumo dos resultados.
    
    Args:
        predicoes: Lista de predições
        estatisticas: Estatísticas compiladas
    """
    print("=" * 80)
    print("RELATÓRIO DE PREDIÇÃO DE EVASÃO ESTUDANTIL")
    print("=" * 80)
    
    print(f"\nVISÃO GERAL:")
    print(f"Total de alunos analisados: {estatisticas['total_students']}")
    print(f"Matriculados: {estatisticas['enrolled_students']} ({estatisticas['enrolled_percentage']:.1f}%)")
    print(f"Em risco de evasão: {estatisticas['dropout_risk_students']} ({estatisticas['dropout_risk_percentage']:.1f}%)")
    
    # Distribuição por urgência
    alunos_risco = [p for p in predicoes if p.status_predicao == 'RISCO_EVASAO']
    if alunos_risco:
        niveis_urgencia = {}
        for aluno in alunos_risco:
            nivel = aluno.nivel_urgencia
            niveis_urgencia[nivel] = niveis_urgencia.get(nivel, 0) + 1
        
        print(f"\nDISTRIBUIÇÃO POR URGÊNCIA:")
        total_risco = len(alunos_risco)
        for nivel, quantidade in niveis_urgencia.items():
            percentual = (quantidade / total_risco) * 100
            print(f"  {nivel}: {quantidade} alunos ({percentual:.1f}%)")
    
    # Casos urgentes
    casos_urgentes = [p for p in alunos_risco if p.nivel_urgencia == 'URGENTE']
    if casos_urgentes:
        print(f"\nALUNOS QUE PRECISAM DE AÇÃO IMEDIATA ({len(casos_urgentes)} alunos):")
        for i, aluno in enumerate(casos_urgentes[:5]):  # Mostrar apenas os primeiros 5
            print(f"  • {aluno.nome} (Matrícula: {aluno.matricula})")
            print(f"    Situação: {aluno.situacao_predita} - Prob: {aluno.probabilidade_situacao}")
            print(f"    Fonte: {aluno.fonte_predicao}")
    
    # Resumo das regras aplicadas
    resumo_regras = estatisticas.get('rules_summary', {})
    if resumo_regras:
        print(f"\nAPLICAÇÃO DAS REGRAS DE NEGÓCIO:")
        print(f"  Total de ajustes por regras: {resumo_regras.get('total_ajustes', 0)}")
        print(f"  NC (Nunca Compareceu): {resumo_regras.get('NC_por_regra', 0)} alunos")
        print(f"  LFI (Limpeza Financeira): {resumo_regras.get('LFI_por_regra', 0)} alunos")
        print(f"  LFR (Limpeza de Frequência): {resumo_regras.get('LFR_por_regra', 0)} alunos")
        print(f"  LAC (Limpeza Acadêmica): {resumo_regras.get('LAC_por_regra', 0)} alunos")
        print(f"  NF (Não Formados): {resumo_regras.get('NF_por_regra', 0)} alunos")
        print(f"  MT (Matriculados): {resumo_regras.get('MT_por_regra', 0)} alunos")

def principal() -> int:
    """
    Função principal do programa.
    
    Returns:
        Código de saída (0 = sucesso, 1 = erro)
    """
    try:
        # Configurar argumentos
        parser = configurar_argumentos()
        args = parser.parse_args()
        
        # Configurar logging
        nivel_log = "DEBUG" if args.verboso else "INFO"
        registrador = obter_registrador(__name__)
        
        # Determinar arquivo de entrada
        if args.arquivo_alunos:
            arquivo_alunos = Path(args.arquivo_alunos)
        else:
            arquivo_alunos = configuracoes.dados.diretorio_dados_brutos / configuracoes.dados.arquivo_alunos
        
        # Verificar se arquivo existe
        if not arquivo_alunos.exists():
            print(f"Erro: Arquivo não encontrado: {arquivo_alunos}")
            return 1
        
        # Determinar arquivo de saída
        arquivo_saida = configuracoes.dados.diretorio_saida / "analise_completa.csv"
        
        # Verificar se arquivo de entrada existe
        if not arquivo_alunos.exists():
            print(f"Erro: Arquivo não encontrado: {arquivo_alunos}")
            return 1
        
        # Inicializar sistema
        registrador.info("Inicializando sistema de predição de evasão...")
        print("Inicializando sistema de predição de evasão...")
        
        sistema = SistemaPredicaoEvasao()
        sistema.inicializar()
        
        # Fazer predições
        registrador.info(f"Processando arquivo: {arquivo_alunos}")
        print(f"Processando arquivo: {arquivo_alunos}")
        
        predicoes, estatisticas = sistema.predizer_alunos(arquivo_alunos)
        
        # Salvar resultados
        arquivo_saida.parent.mkdir(parents=True, exist_ok=True)
        salvar_predicoes_em_csv(predicoes, arquivo_saida)
        
        # Imprimir relatório
        imprimir_relatorio_resumo(predicoes, estatisticas)
        
        print(f"\nAnálise concluída com sucesso!")
        print(f"Arquivo de saída: {arquivo_saida}")
        print(f"Sistema híbrido: ML + Regras de Negócio aplicadas")
        
        registrador.info(f"Predições salvas em: {arquivo_saida}")
        
        return 0
        
    except KeyboardInterrupt:
        registrador.info("Operação cancelada pelo usuário")
        print("\nOperação cancelada pelo usuário")
        return 1
        
    except Exception as e:
        registrador.error(f"Erro durante a execução: {e}", exc_info=True)
        print(f"\nErro durante a execução: {e}")
        print("Verifique os logs para mais detalhes.")
        return 1

if __name__ == "__main__":
    sys.exit(principal())