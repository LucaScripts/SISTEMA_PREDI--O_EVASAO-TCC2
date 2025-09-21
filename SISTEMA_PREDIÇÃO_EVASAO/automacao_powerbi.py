#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Automação Power BI - Sistema de Predição de Evasão
Automatiza atualização do Power BI após processamento
"""

import os
import shutil
import requests
import json
from datetime import datetime
from pathlib import Path
import pandas as pd

class AutomacaoPowerBI:
    """Classe para automatizar atualização do Power BI"""
    
    def __init__(self, pasta_csv_powerbi="C:/PowerBI_Data/"):
        """
        Inicializa automação
        
        Args:
            pasta_csv_powerbi: Pasta onde Power BI busca os CSVs
        """
        self.pasta_csv_powerbi = Path(pasta_csv_powerbi)
        self.pasta_csv_powerbi.mkdir(exist_ok=True)
        
        # Nome padrão do arquivo CSV que o Power BI monitora
        self.nome_arquivo_bi = "predicoes_evasao.csv"
        
        # Log de atualizações
        self.log_atualizacoes = self.pasta_csv_powerbi / "log_atualizacoes.txt"
    
    def salvar_csv_para_powerbi(self, df_resultado, metadados=None):
        """
        Salva CSV na pasta que o Power BI monitora
        Usa estrutura baseada no arquivo de referência analise_completa_alunos.csv
        
        Args:
            df_resultado: DataFrame com resultados das predições
            metadados: Informações sobre o processamento
        """
        try:
            # Padronizar estrutura baseada no arquivo de referência
            df_padronizado = self._padronizar_estrutura_csv(df_resultado, metadados)
            
            # Salvar na pasta do Power BI
            caminho_completo = self.pasta_csv_powerbi / self.nome_arquivo_bi
            df_padronizado.to_csv(caminho_completo, index=False, encoding='utf-8-sig')
            
            # Registrar atualização
            self._registrar_atualizacao(metadados, len(df_padronizado))
            
            print(f"✅ CSV salvo para Power BI: {caminho_completo}")
            print(f"📊 Total de alunos: {len(df_padronizado)}")
            print(f"📁 Colunas: {len(df_padronizado.columns)}")
            
            return True
            
        except Exception as e:
            print(f"❌ Erro ao salvar CSV para Power BI: {e}")
            return False
    
    def _padronizar_estrutura_csv(self, df_original, metadados):
        """
        Padroniza estrutura do CSV baseado no arquivo analise_completa_alunos.csv
        
        Estrutura esperada (23 colunas):
        Nome, Matricula, Curso, Sexo, Turma, Status, Situacao_Predita, 
        Probabilidade_Situacao, Probabilidade_Evasao_Total, Urgencia, Emoji,
        Fator_Principal, Valor_Importancia, Confianca, Top_1_Situacao, Top_1_Prob,
        Top_2_Situacao, Top_2_Prob, Top_3_Situacao, Top_3_Prob, Data_Processamento,
        Total_Processados, Arquivo_Origem
        """
        
        # Criar DataFrame com estrutura padronizada
        df_padrao = pd.DataFrame()
        
        # Mapeamento de colunas do sistema atual para estrutura padrão
        mapeamento_colunas = {
            'Nome': ['Nome', 'nome'],
            'Matricula': ['Matrícula', 'Matricula', 'matricula'], 
            'Curso': ['Curso', 'curso'],
            'Sexo': ['Sexo', 'sexo'],
            'Turma': ['Turma Atual', 'Turma', 'turma'],
            'Status': ['Status Predição', 'Status', 'status_predicao'],
            'Situacao_Predita': ['Situação Predita', 'Situacao_Predita', 'situacao_predita'],
            'Probabilidade_Situacao': ['Probabilidade Situação', 'Probabilidade_Situacao', 'probabilidade_situacao'],
            'Probabilidade_Evasao_Total': ['Probabilidade Evasão', 'Probabilidade_Evasao_Total', 'probabilidade_evasao_total'],
            'Urgencia': ['Nível Urgência', 'Urgencia', 'nivel_urgencia'],
            'Fator_Principal': ['Fator Principal', 'Fator_Principal', 'fator_principal'],
            'Valor_Importancia': ['Valor Importância', 'Valor_Importancia', 'valor_importancia'],
            'Confianca': ['Confiança', 'Confianca', 'confianca_predicao']
        }
        
        # Aplicar mapeamento
        for col_padrao, possibilidades in mapeamento_colunas.items():
            valor_encontrado = None
            for possivel in possibilidades:
                if possivel in df_original.columns:
                    valor_encontrado = df_original[possivel]
                    break
            
            if valor_encontrado is not None:
                df_padrao[col_padrao] = valor_encontrado
            else:
                # Valores padrão se coluna não for encontrada
                if col_padrao == 'Sexo':
                    df_padrao[col_padrao] = 'M'
                elif col_padrao == 'Turma':
                    df_padrao[col_padrao] = 'N/A'
                elif col_padrao == 'Status':
                    df_padrao[col_padrao] = 'MATRICULADO'
                elif col_padrao == 'Situacao_Predita':
                    df_padrao[col_padrao] = 'Matriculado'
                elif col_padrao == 'Probabilidade_Situacao':
                    df_padrao[col_padrao] = '50.0%'
                elif col_padrao == 'Probabilidade_Evasao_Total':
                    df_padrao[col_padrao] = '30.0%'
                elif col_padrao == 'Urgencia':
                    df_padrao[col_padrao] = 'NENHUMA'  # Padrão para matriculados
                elif col_padrao == 'Fator_Principal':
                    df_padrao[col_padrao] = 'Não identificado'
                elif col_padrao == 'Valor_Importancia':
                    df_padrao[col_padrao] = 0.0
                elif col_padrao == 'Confianca':
                    df_padrao[col_padrao] = 'Média'
                else:
                    df_padrao[col_padrao] = 'N/A'
        
        # Adicionar emoji baseado no nível de urgência (cores psicológicas)
        df_padrao['Emoji'] = df_padrao['Urgencia'].map({
            'URGENTE': '🔴',      # Vermelho forte (#FF0000) - perigo/atenção imediata
            'ALTA': '🟠',         # Laranja (#FF8000) - chama atenção, menos que vermelho
            'MEDIA': '🟡',        # Amarelo (#FFD700) - intermediário, alerta moderado
            'BAIXA': '🔵',        # Azul (#1E90FF) - tranquilidade, prioridade menor
            'NENHUMA': '⚪'       # Cinza claro (#A9A9A9) - neutro, sem prioridade
        }).fillna('⚪')
        
        # Adicionar colunas Top_N (simuladas se não existirem)
        if 'Top_1_Situacao' not in df_original.columns:
            df_padrao['Top_1_Situacao'] = df_padrao['Situacao_Predita']
            df_padrao['Top_1_Prob'] = df_padrao['Probabilidade_Situacao']
            df_padrao['Top_2_Situacao'] = 'Matriculado'
            df_padrao['Top_2_Prob'] = '30.0%'
            df_padrao['Top_3_Situacao'] = 'Limpeza Academica'
            df_padrao['Top_3_Prob'] = '15.0%'
        
        # Adicionar metadados como colunas extras (opcionais)
        if metadados:
            df_padrao['Data_Processamento'] = metadados.get('data_processamento', datetime.now())
            df_padrao['Total_Processados'] = len(df_padrao)
            df_padrao['Arquivo_Origem'] = metadados.get('arquivo_original', 'Sistema Web')
        
        return df_padrao
    
    def _registrar_atualizacao(self, metadados, total_processados=None):
        """Registra log de atualização"""
        try:
            timestamp = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
            total_alunos = total_processados or (metadados.get('total_alunos', 'N/A') if metadados else 'N/A')
            arquivo_origem = metadados.get('arquivo_original', 'Sistema Web') if metadados else 'Sistema Web'
            
            log_entry = f"{timestamp} - CSV atualizado - {total_alunos} alunos - Origem: {arquivo_origem}\n"
            
            with open(self.log_atualizacoes, 'a', encoding='utf-8') as f:
                f.write(log_entry)
                
        except Exception as e:
            print(f"⚠️ Erro no log: {e}")
    
    def _tentar_refresh_powerbi_service(self):
        """
        Tenta atualizar dataset no Power BI Service via API
        (Requer configuração de credenciais)
        """
        # Esta funcionalidade requer:
        # 1. App registrado no Azure AD
        # 2. Configuração de credenciais
        # 3. ID do dataset no Power BI Service
        print("⚠️ Refresh automático do Power BI Service não configurado")
        print("💡 Configure manualmente o refresh automático no Power BI Service")
        
    def configurar_pasta_dashboard(self, nova_pasta):
        """
        Configura nova pasta para salvar CSVs (ex: pasta do Dashboard)
        
        Args:
            nova_pasta: Caminho para nova pasta
        """
        self.pasta_csv_powerbi = Path(nova_pasta)
        self.pasta_csv_powerbi.mkdir(exist_ok=True)
        self.log_atualizacoes = self.pasta_csv_powerbi / "log_atualizacoes.txt"
        print(f"✅ Pasta configurada: {self.pasta_csv_powerbi}")
    
    def configurar_powerbi_desktop(self):
        """
        Retorna instruções para configuração do Power BI Desktop
        """
        instrucoes = f"""
🔧 CONFIGURAÇÃO POWER BI DESKTOP
================================

📁 PASTA CSV: {self.pasta_csv_powerbi}
📊 ARQUIVO: {self.nome_arquivo_bi}

PASSOS:
1. Abra seu arquivo .pbix
2. Transformar Dados → Nova Fonte
3. Texto/CSV → Selecione: {self.nome_arquivo_bi}
4. Configure refresh automático:
   • Horários: 08h, 09h, 10h, 11h, 14h, 15h, 16h, 17h
   • Detectar alterações automaticamente
5. Salve e publique no Power BI Service

🔗 RESULTADO:
Seu dashboard será atualizado automaticamente nos horários definidos!
        """
        return instrucoes.strip()


# Função de conveniência para uso direto
def atualizar_powerbi(df_resultado, pasta_destino=None, metadados=None):
    """
    Função de conveniência para atualizar Power BI
    
    Args:
        df_resultado: DataFrame com resultados
        pasta_destino: Pasta onde salvar CSV (opcional)
        metadados: Metadados do processamento
    
    Returns:
        bool: True se sucesso, False se erro
    """
    if pasta_destino:
        automacao = AutomacaoPowerBI(pasta_destino)
    else:
        automacao = AutomacaoPowerBI()
    
    return automacao.salvar_csv_para_powerbi(df_resultado, metadados)


if __name__ == "__main__":
    # Teste básico
    print("🧪 Testando AutomacaoPowerBI...")
    
    # Dados de teste
    dados_teste = pd.DataFrame({
        'Nome': ['Teste Urgente', 'Teste Alta', 'Teste Média', 'Teste Baixa', 'Teste Matriculado'],
        'Matrícula': ['001', '002', '003', '004', '005'],
        'Curso': ['Info'] * 5,
        'Status': ['RISCO_EVASAO', 'RISCO_EVASAO', 'RISCO_EVASAO', 'RISCO_EVASAO', 'MATRICULADO'],
        'Urgencia': ['URGENTE', 'ALTA', 'MEDIA', 'BAIXA', 'NENHUMA'],
        'Probabilidade_Evasao_Total': ['95%', '85%', '70%', '60%', '5%']
    })
    
    # Teste
    automacao = AutomacaoPowerBI("./teste_powerbi/")
    metadados_teste = {
        'data_processamento': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'arquivo_original': 'teste_cores_psicologicas.csv'
    }
    
    sucesso = automacao.salvar_csv_para_powerbi(dados_teste, metadados_teste)
    
    if sucesso:
        print("✅ Teste concluído com sucesso!")
        print("🎨 Cores psicológicas implementadas:")
        print("   🔴 URGENTE - Vermelho forte")
        print("   🟠 ALTA - Laranja")  
        print("   🟡 MÉDIA - Amarelo")
        print("   🔵 BAIXA - Azul")
        print("   ⚪ NENHUMA - Cinza claro")
    else:
        print("❌ Teste falhou!")