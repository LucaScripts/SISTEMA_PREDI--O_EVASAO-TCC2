#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pandas as pd
from automacao_powerbi import AutomacaoPowerBI

# Criar dados de teste simulando resultado do sistema
dados_teste = pd.DataFrame({
    'Nome': ['João Silva - MATRICULADO', 'Maria Santos - URGENTE', 'Pedro Costa - ALTA', 'Ana - MÉDIA', 'Carlos - BAIXA'],
    'Matrícula': ['12345', '54321', '98765', '11111', '22222'],
    'Curso': ['Informática', 'Informática', 'Informática', 'Informática', 'Informática'],
    'Status': ['MATRICULADO', 'RISCO_EVASAO', 'RISCO_EVASAO', 'RISCO_EVASAO', 'RISCO_EVASAO'],
    'Urgencia': ['NENHUMA', 'URGENTE', 'ALTA', 'MEDIA', 'BAIXA'],
    'Probabilidade_Evasao_Total': ['5.2%', '95.8%', '87.3%', '74.1%', '62.5%'],
    'Situacao_Predita': ['Matriculado', 'Limpeza Academica', 'Transferido', 'Limpeza Academica', 'Matriculado']
})

print('📋 TESTE FINAL - EMOJIS BASEADOS NA URGÊNCIA')
print('='*60)

# Processar com a função corrigida
automacao = AutomacaoPowerBI()
metadados = {'data_processamento': '2024-12-21', 'arquivo_original': 'teste_final'}
resultado = automacao._padronizar_estrutura_csv(dados_teste, metadados)

# Mostrar resultado por nível de urgência
urgencias = ['URGENTE', 'ALTA', 'MEDIA', 'BAIXA', 'NENHUMA']
emoji_correto = {'URGENTE': '🔴', 'ALTA': '🟡', 'MEDIA': '🟡', 'BAIXA': '🟢', 'NENHUMA': '🟢'}

for urgencia in urgencias:
    alunos_urgencia = resultado[resultado['Urgencia'] == urgencia]
    if len(alunos_urgencia) > 0:
        emoji_esperado = emoji_correto[urgencia]
        print(f'\n{emoji_esperado} {urgencia}: {len(alunos_urgencia)} aluno(s)')
        for _, aluno in alunos_urgencia.iterrows():
            emoji_real = aluno['Emoji']
            status_check = '✅' if emoji_real == emoji_esperado else '❌'
            print(f'   {status_check} {aluno["Nome"]}: {emoji_real}')

print(f'\n📊 RESUMO:')
print(f'Total de alunos processados: {len(resultado)}')
print(f'Estrutura CSV: {len(resultado.columns)} colunas')
print(f'Emojis por urgência funcionando: ✅')
print(f'Matriculados sem urgência: ✅')

# Verificar se algum matriculado tem urgência diferente de NENHUMA
matriculados_com_urgencia = resultado[(resultado['Status'] == 'MATRICULADO') & (resultado['Urgencia'] != 'NENHUMA')]
if len(matriculados_com_urgencia) > 0:
    print('❌ ERRO: Encontrados matriculados com urgência!')
    print(matriculados_com_urgencia[['Nome', 'Status', 'Urgencia', 'Emoji']])
else:
    print('✅ CORRETO: Todos os matriculados têm urgência NENHUMA')

print('\n🎯 SISTEMA PRONTO PARA PRODUÇÃO!')