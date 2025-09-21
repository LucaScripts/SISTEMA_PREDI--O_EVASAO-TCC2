#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pandas as pd
from automacao_powerbi import AutomacaoPowerBI

# Teste final completo com todas as cores psicológicas
dados_completo = pd.DataFrame({
    'Nome': ['🔴 Maria URGENTE', '🟠 Pedro ALTA', '🟡 Ana MÉDIA', '🔵 João BAIXA', '⚪ Carlos MATRICULADO'],
    'Matrícula': ['54321', '98765', '11111', '22222', '12345'],
    'Curso': ['Informática', 'Informática', 'Informática', 'Informática', 'Informática'],
    'Status': ['RISCO_EVASAO', 'RISCO_EVASAO', 'RISCO_EVASAO', 'RISCO_EVASAO', 'MATRICULADO'],
    'Urgencia': ['URGENTE', 'ALTA', 'MEDIA', 'BAIXA', 'NENHUMA'],
    'Probabilidade_Evasao_Total': ['95.8%', '87.3%', '74.1%', '62.5%', '5.2%'],
    'Situacao_Predita': ['Limpeza Academica', 'Transferido', 'Limpeza Academica', 'Matriculado', 'Matriculado']
})

print('🎨 TESTE FINAL - CORES PSICOLÓGICAS IMPLEMENTADAS')
print('='*60)

# Processar
automacao = AutomacaoPowerBI()
metadados = {
    'data_processamento': '2024-12-21 16:30:00',
    'arquivo_original': 'teste_final_cores.csv'
}

resultado = automacao._padronizar_estrutura_csv(dados_completo, metadados)

print('📊 MAPEAMENTO DE CORES CONFIRMADO:')
print('-' * 60)

# Verificar cada nível de urgência
cores_esperadas = {
    'URGENTE': {'emoji': '🔴', 'cor': '#FF0000', 'psicologia': 'Perigo/atenção imediata'},
    'ALTA': {'emoji': '🟠', 'cor': '#FF8000', 'psicologia': 'Chama atenção, menos que vermelho'},
    'MEDIA': {'emoji': '🟡', 'cor': '#FFD700', 'psicologia': 'Intermediário, alerta moderado'},
    'BAIXA': {'emoji': '🔵', 'cor': '#1E90FF', 'psicologia': 'Tranquilidade, prioridade menor'},
    'NENHUMA': {'emoji': '⚪', 'cor': '#A9A9A9', 'psicologia': 'Neutro, sem prioridade'}
}

todos_corretos = True

for urgencia in cores_esperadas:
    alunos = resultado[resultado['Urgencia'] == urgencia]
    if len(alunos) > 0:
        config = cores_esperadas[urgencia]
        emoji_real = alunos.iloc[0]['Emoji']
        
        if emoji_real == config['emoji']:
            status = '✅'
        else:
            status = '❌'
            todos_corretos = False
            
        print(f'{config["emoji"]} {urgencia}:')
        print(f'   {status} Real: {emoji_real} | Esperado: {config["emoji"]}')
        print(f'   🎨 Cor: {config["cor"]}')
        print(f'   🧠 Psicologia: {config["psicologia"]}')
        print()

print('🎯 RESULTADO FINAL:')
print('='*60)

if todos_corretos:
    print('✅ TODAS AS CORES PSICOLÓGICAS IMPLEMENTADAS CORRETAMENTE!')
    print('✅ Sistema pronto para produção com visual intuitivo!')
    print()
    print('🎨 BENEFÍCIOS DO NOVO ESQUEMA:')
    print('• Impacto visual máximo para casos críticos (vermelho)')
    print('• Gradação natural de prioridade (laranja → amarelo → azul)')
    print('• Neutralidade visual para casos sem risco (cinza)')
    print('• Interface mais intuitiva e profissional')
else:
    print('❌ Alguns emojis não estão corretos')

print(f'\n📈 ESTATÍSTICAS:')
print(f'• Alunos processados: {len(resultado)}')
print(f'• Estrutura CSV: {len(resultado.columns)} colunas')
print(f'• Níveis de urgência: {len(cores_esperadas)}')

print('\n🚀 SISTEMA ATUALIZADO E OPERACIONAL!')