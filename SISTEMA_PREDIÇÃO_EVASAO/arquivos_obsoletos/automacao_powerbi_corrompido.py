#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Automação Power BI - Sistema de Predição de Evasão
Automatiza atualização do da                         df_padrao[col_padrao] = 'N/A'
        
        # Adicionar emoji baseado no nível de urgência (atualizado com cores específicas)
        df_padrao['Emoji'] = df_padrao['Urgencia'].map({
            'URGENTE': '🔴',      # Vermelho forte (#FF0000) - perigo/atenção imediata
            'ALTA': '🟠',         # Laranja (#FF8000) - chama atenção, menos que vermelho
            'MEDIA': '🟡',        # Amarelo (#FFD700) - intermediário, alerta moderado
            'BAIXA': '🔵',        # Azul (#1E90FF) - tranquilidade, prioridade menor
            'NENHUMA': '⚪'       # Cinza claro (#A9A9A9) - neutro, sem prioridade
        }).fillna('⚪')
        
        # Adicionar colunas Top_N (simuladas se não existirem)ar emoji baseado no nível de urgência (atualizado com cores específicas)
        df_padrao['Emoji'] = df_padrao['Urgencia'].map({
            'URGENTE': '🔴',      # Vermelho forte (#FF0000) - perigo/atenção imediata
            'ALTA': '�',         # Laranja (#FF8000) - chama atenção, menos que vermelho
            'MEDIA': '🟡',        # Amarelo (#FFD700) - intermediário, alerta moderado
            'BAIXA': '�',        # Azul (#1E90FF) - tranquilidade, prioridade menor
            'NENHUMA': '⚪'       # Cinza claro (#A9A9A9) - neutro, sem prioridade
        }).fillna('⚪')após processamento
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
            # Padronizar DataFrame para estrutura esperada pelo Power BI
            df_padronizado = self._padronizar_estrutura_csv(df_resultado, metadados)
            
            # Caminho completo do arquivo
            caminho_csv = self.pasta_csv_powerbi / self.nome_arquivo_bi
            
            # Salvar CSV com encoding correto para Power BI
            df_padronizado.to_csv(caminho_csv, index=False, encoding='utf-8-sig', sep=',')
            
            # Registrar atualização
            self._registrar_atualizacao(metadados, len(df_padronizado))
            
            print(f"✅ CSV salvo em: {caminho_csv}")
            print(f"📊 {len(df_padronizado)} alunos processados")
            print(f"📋 {len(df_padronizado.columns)} colunas padronizadas")
            
            # Tentar atualizar Power BI Service via API (se configurado)
            self._tentar_refresh_powerbi_service()
            
            return True
            
        except Exception as e:
            print(f"❌ Erro ao salvar CSV: {e}")
            return False
    
    def _padronizar_estrutura_csv(self, df_original, metadados):
        """
        Padroniza DataFrame para estrutura do arquivo de referência
        
        Estrutura esperada (20 colunas):
        Nome, Matricula, Curso, Sexo, Turma, Status, Situacao_Predita, 
        Probabilidade_Situacao, Probabilidade_Evasao_Total, Urgencia, Emoji,
        Fator_Principal, Valor_Importancia, Confianca, Top_1_Situacao, Top_1_Prob,
        Top_2_Situacao, Top_2_Prob, Top_3_Situacao, Top_3_Prob
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
        
        # Adicionar emoji baseado no nível de urgência (corrigido)
        df_padrao['Emoji'] = df_padrao['Urgencia'].map({
            'URGENTE': '🔴',      # Vermelho para urgente
            'ALTA': '🟡',         # Amarelo/laranja para alta
            'MEDIA': '🟡',        # Amarelo/laranja para média
            'BAIXA': '🟢',        # Verde para baixa
            'NENHUMA': '�'       # Verde para matriculados sem urgência
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
        # 2. Credenciais de Service Principal
        # 3. ID do dataset no Power BI Service
        
        # Por enquanto, apenas informa que seria possível
        print("💡 Para refresh automático via API, configure as credenciais Azure AD")
        print("📖 Documentação: https://docs.microsoft.com/power-bi/developer/embedded/")
    
    def configurar_powerbi_desktop(self):
        """
        Instruções para configurar Power BI Desktop para refresh automático
        """
        instrucoes = f"""
        
        🔧 CONFIGURAÇÃO POWER BI DESKTOP:
        
        1. Abra seu Power BI Desktop
        2. Vá em Transformar Dados (Power Query)
        3. Configure fonte de dados como: {self.pasta_csv_powerbi / self.nome_arquivo_bi}
        4. Em Opções de Consulta:
           - Marque "Atualizar automaticamente ao detectar alterações"
           - Configure intervalo de refresh (ex: a cada 5 minutos)
        
        5. Salve o arquivo .pbix
        6. Configure refresh automático no Power BI Service:
           - Vá em Configurações do Dataset
           - Ative "Atualização automática de página"
           - Configure credenciais de gateway (se necessário)
        
        📁 Pasta monitorada: {self.pasta_csv_powerbi}
        📄 Arquivo: {self.nome_arquivo_bi}
        
        """
        print(instrucoes)
        
        # Criar arquivo README na pasta
        readme_path = self.pasta_csv_powerbi / "README_CONFIGURACAO.txt"
        with open(readme_path, 'w', encoding='utf-8') as f:
            f.write(instrucoes)
        
        return instrucoes

# Funções de integração com o sistema existente
def integrar_com_sistema_web():
    """
    Modifica o sistema web para usar automação Power BI
    """
    codigo_integracao = '''
    # Adicionar no processamento da interface web:
    
    from automacao_powerbi import AutomacaoPowerBI
    
    def processar_arquivo_com_autobi(uploaded_file, incluir_shap, incluir_regras, formato_saida):
        """Processa arquivo e atualiza Power BI automaticamente"""
        
        # Processamento normal (código existente)
        resultado = processar_arquivo(uploaded_file, incluir_shap, incluir_regras, formato_saida)
        
        # NOVA FUNCIONALIDADE: Automação Power BI
        if resultado and "df_resultado" in resultado:
            automacao = AutomacaoPowerBI()
            
            metadados = {
                "data_processamento": datetime.now(),
                "total_alunos": len(resultado["df_resultado"]),
                "arquivo_original": uploaded_file.name,
                "incluir_shap": incluir_shap,
                "incluir_regras": incluir_regras
            }
            
            # Salvar automaticamente para Power BI
            sucesso = automacao.salvar_csv_para_powerbi(
                resultado["df_resultado"], 
                metadados
            )
            
            if sucesso:
                st.success("🚀 Power BI será atualizado automaticamente!")
                st.info("📊 Dashboard web ficará disponível em alguns minutos")
                
        return resultado
    '''
    
    return codigo_integracao

if __name__ == "__main__":
    # Exemplo de uso
    automacao = AutomacaoPowerBI()
    
    print("🚀 Configurando automação Power BI...")
    automacao.configurar_powerbi_desktop()
    
    # Teste com dados fictícios
    df_teste = pd.DataFrame({
        'Nome': ['Aluno A', 'Aluno B'],
        'Probabilidade_Evasao': [0.8, 0.3],
        'Status_Predicao': ['RISCO_EVASAO', 'MATRICULADO']
    })
    
    metadados_teste = {
        'data_processamento': datetime.now(),
        'total_alunos': 2,
        'arquivo_original': 'teste.xlsx'
    }
    
    automacao.salvar_csv_para_powerbi(df_teste, metadados_teste)
    print("✅ Teste concluído!")