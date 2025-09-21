#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Forçar reload
import sys
if 'automacao_powerbi' in sys.modules:
    del sys.modules['automacao_powerbi']

import pandas as pd
from automacao_powerbi import AutomacaoPowerBI

# Teste rápido dos novos emojis
dados = pd.DataFrame({
    'Nome': ['Teste ALTA', 'Teste BAIXA', 'Teste NENHUMA'],
    'Status': ['RISCO_EVASAO', 'RISCO_EVASAO', 'MATRICULADO'], 
    'Urgencia': ['ALTA', 'BAIXA', 'NENHUMA']
})

auto = AutomacaoPowerBI()
meta = {'teste': 'sim'}
result = auto._padronizar_estrutura_csv(dados, meta)

print('🧪 TESTE RELOAD - NOVOS EMOJIS:')
print('='*40)
for i, row in result.iterrows():
    urgencia = row['Urgencia']
    emoji = row['Emoji']
    print(f'{urgencia}: {emoji}')
    
print('\n✅ Esperado:')
print('ALTA: 🟠')
print('BAIXA: 🔵') 
print('NENHUMA: ⚪')