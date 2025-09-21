#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pandas as pd
from automacao_powerbi import AutomacaoPowerBI

# Criar dados de teste com todos os níveis de urgência
dados_teste = pd.DataFrame({
    'Nome': ['URGENTE - Maria', 'ALTA - Pedro', 'MÉDIA - Ana', 'BAIXA - João', 'NENHUMA - Carlos'],
    'Matrícula': ['54321', '98765', '11111', '22222', '12345'],
    'Curso': ['Informática', 'Informática', 'Informática', 'Informática', 'Informática'],
    'Status': ['RISCO_EVASAO', 'RISCO_EVASAO', 'RISCO_EVASAO', 'RISCO_EVASAO', 'MATRICULADO'],
    'Urgencia': ['URGENTE', 'ALTA', 'MEDIA', 'BAIXA', 'NENHUMA'],
    'Probabilidade_Evasao_Total': ['95.8%', '87.3%', '74.1%', '62.5%', '5.2%'],
    'Situacao_Predita': ['Limpeza Academica', 'Transferido', 'Limpeza Academica', 'Matriculado', 'Matriculado']
})

print('🎨 NOVO ESQUEMA DE CORES - TESTE VISUAL')
print('='*60)

# Processar com a função atualizada
automacao = AutomacaoPowerBI()
metadados = {'data_processamento': '2024-12-21', 'arquivo_original': 'teste_cores'}
resultado = automacao._padronizar_estrutura_csv(dados_teste, metadados)

# Definir cores esperadas e suas descrições
cores_sistema = {
    'URGENTE': {'emoji': '🔴', 'cor': '#FF0000', 'desc': 'Vermelho forte - perigo/atenção imediata'},
    'ALTA': {'emoji': '🟠', 'cor': '#FF8000', 'desc': 'Laranja - chama atenção, menos que vermelho'},
    'MEDIA': {'emoji': '🟡', 'cor': '#FFD700', 'desc': 'Amarelo - intermediário, alerta moderado'},
    'BAIXA': {'emoji': '🔵', 'cor': '#1E90FF', 'desc': 'Azul - tranquilidade, prioridade menor'},
    'NENHUMA': {'emoji': '⚪', 'cor': '#A9A9A9', 'desc': 'Cinza claro - neutro, sem prioridade'}
}

print('📊 RESULTADO DO MAPEAMENTO:')
print('-' * 60)

for urgencia in ['URGENTE', 'ALTA', 'MEDIA', 'BAIXA', 'NENHUMA']:
    alunos_urgencia = resultado[resultado['Urgencia'] == urgencia]
    if len(alunos_urgencia) > 0:
        config = cores_sistema[urgencia]
        print(f'\n{config["emoji"]} {urgencia}:')
        print(f'   📐 Cor: {config["cor"]}')
        print(f'   📝 Descrição: {config["desc"]}')
        
        for _, aluno in alunos_urgencia.iterrows():
            emoji_real = aluno['Emoji']
            status_check = '✅' if emoji_real == config["emoji"] else '❌'
            print(f'   {status_check} {aluno["Nome"]}: {emoji_real}')

print(f'\n🎯 VALIDAÇÃO DO SISTEMA:')
print('='*60)

# Verificar se todos os emojis estão corretos
todos_corretos = True
for _, row in resultado.iterrows():
    urgencia = row['Urgencia']
    emoji_esperado = cores_sistema[urgencia]['emoji']
    emoji_real = row['Emoji']
    
    if emoji_real != emoji_esperado:
        print(f'❌ ERRO: {row["Nome"]} - Esperado: {emoji_esperado}, Real: {emoji_real}')
        todos_corretos = False

if todos_corretos:
    print('✅ TODOS OS EMOJIS ESTÃO CORRETOS!')
    print('✅ Sistema de cores psicológicas implementado com sucesso!')
else:
    print('❌ Encontrados erros no mapeamento de emojis')

print(f'\n📈 ESTATÍSTICAS:')
print(f'• Total processados: {len(resultado)} alunos')
print(f'• Colunas geradas: {len(resultado.columns)}')
print(f'• Urgências mapeadas: {len(cores_sistema)} níveis')

print(f'\n🎨 BENEFÍCIOS DO NOVO ESQUEMA:')
print('• 🔴 Vermelho: Impacto visual máximo para casos críticos')
print('• 🟠 Laranja: Destaque moderado para alta prioridade')  
print('• 🟡 Amarelo: Equilíbrio visual para casos médios')
print('• 🔵 Azul: Tranquilidade para baixa prioridade')
print('• ⚪ Cinza: Neutralidade para casos sem risco')

print('\n🚀 SISTEMA ATUALIZADO E PRONTO!')