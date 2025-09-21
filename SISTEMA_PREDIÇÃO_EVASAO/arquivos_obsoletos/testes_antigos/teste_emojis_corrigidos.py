#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pandas as pd
from automacao_powerbi import AutomacaoPowerBI

# Criar dados de teste
dados_teste = pd.DataFrame({
    'Nome': ['João Silva', 'Maria Santos', 'Pedro Costa', 'Ana Oliveira'],
    'Matrícula': ['12345', '54321', '98765', '11111'],
    'Curso': ['Info', 'Info', 'Info', 'Info'],
    'Status': ['MATRICULADO', 'RISCO_EVASAO', 'RISCO_EVASAO', 'RISCO_EVASAO'],
    'Urgencia': ['NENHUMA', 'URGENTE', 'ALTA', 'BAIXA'],
    'Probabilidade_Evasao_Total': ['10.5%', '95.2%', '82.1%', '65.0%']
})

print('📋 DADOS DE TESTE:')
print(dados_teste)
print('\n' + '='*50)

# Testar padronização
automacao = AutomacaoPowerBI()
metadados = {'data_processamento': '2024-01-20', 'arquivo_original': 'teste'}
resultado = automacao._padronizar_estrutura_csv(dados_teste, metadados)

print('✅ RESULTADO PADRONIZADO - EMOJIS CORRIGIDOS:')
print('='*50)
for i, row in resultado.iterrows():
    nome = row['Nome']
    status = row['Status']
    urgencia = row['Urgencia'] 
    emoji = row['Emoji']
    print(f'👤 {nome}:')
    print(f'   Status: {status}')
    print(f'   Urgência: {urgencia}')
    print(f'   Emoji: {emoji}')
    print()

print('✅ VERIFICAÇÃO DOS EMOJIS:')
print('='*50)
print('🔴 URGENTE  - Vermelho (ação imediata)')
print('🟡 ALTA/MÉDIA - Amarelo/Laranja (prioritário)')
print('🟢 BAIXA/NENHUMA - Verde (normal/OK)')
print()

# Teste da lógica de status MATRICULADO
matriculados = resultado[resultado['Status'] == 'MATRICULADO']
print(f'📊 ALUNOS MATRICULADOS ({len(matriculados)}):')
for _, row in matriculados.iterrows():
    print(f'   {row["Nome"]}: Urgência={row["Urgencia"]}, Emoji={row["Emoji"]}')
    
if len(matriculados) > 0:
    urgencias_matriculados = matriculados['Urgencia'].unique()
    if 'NENHUMA' in urgencias_matriculados and len(urgencias_matriculados) == 1:
        print('✅ CORRETO: Matriculados têm urgência NENHUMA')
    else:
        print('❌ ERRO: Matriculados deveriam ter urgência NENHUMA apenas')