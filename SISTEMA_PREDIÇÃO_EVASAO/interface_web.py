#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Interface web simples usando Streamlit para o sistema de predição
"""
import streamlit as st
import pandas as pd
import sys
import os
from pathlib import Path
import tempfile
import zipfile
from datetime import datetime

# Adicionar o caminho do projeto
sys.path.insert(0, os.getcwd())

from codigo_fonte.nucleo import SistemaPredicaoEvasao
from codigo_fonte.configuracao import configuracoes

def tentar_reparar_arquivo_excel(arquivo_path):
    """
    Tenta reparar arquivo Excel problemático com diferentes estratégias
    
    Args:
        arquivo_path: Caminho para arquivo problemático
        
    Returns:
        str or None: Caminho para arquivo reparado ou None se falhou
    """
    try:
        # Estratégia 1: Tentar diferentes engines um por vez
        engines = [
            {'name': 'openpyxl', 'engine': 'openpyxl'},
            {'name': 'xlrd', 'engine': 'xlrd'},
            {'name': 'auto', 'engine': None}
        ]
        
        for engine_info in engines:
            try:
                if engine_info['engine']:
                    df = pd.read_excel(arquivo_path, engine=engine_info['engine'])
                else:
                    df = pd.read_excel(arquivo_path)
                
                # Se conseguiu ler, recriar arquivo
                arquivo_limpo = arquivo_path.replace('.xlsx', '_limpo.xlsx')
                df.to_excel(arquivo_limpo, index=False, engine='openpyxl')
                
                # Testar se o arquivo limpo funciona
                df_test = pd.read_excel(arquivo_limpo, nrows=1)
                return arquivo_limpo
                
            except Exception:
                continue
        
        # Estratégia 2: Tentar como CSV e reconverter
        try:
            # Às vezes arquivos "Excel" são na verdade CSV
            df_csv = pd.read_csv(arquivo_path, encoding='utf-8', sep=';')
            if len(df_csv.columns) > 1:  # Se conseguiu ler como CSV
                arquivo_convertido = arquivo_path.replace('.xlsx', '_convertido.xlsx')
                df_csv.to_excel(arquivo_convertido, index=False, engine='openpyxl')
                return arquivo_convertido
        except:
            pass
            
        # Estratégia 3: Tentar com diferentes encodings
        encodings = ['utf-8', 'latin1', 'cp1252', 'iso-8859-1']
        for encoding in encodings:
            try:
                df_enc = pd.read_csv(arquivo_path, encoding=encoding)
                if len(df_enc.columns) > 1:
                    arquivo_enc = arquivo_path.replace('.xlsx', f'_enc_{encoding}.xlsx')
                    df_enc.to_excel(arquivo_enc, index=False, engine='openpyxl')
                    return arquivo_enc
            except:
                continue
        
        return None
        
    except Exception:
        return None

def verificar_arquivo_excel(arquivo_path):
    """
    Verifica a integridade e formato do arquivo Excel
    
    Args:
        arquivo_path: Caminho para o arquivo
        
    Returns:
        dict: Informações sobre o arquivo
    """
    info = {
        'valido': False,
        'formato': 'desconhecido',
        'erro': None,
        'sugestoes': []
    }
    
    try:
        # Verificar se o arquivo existe e tem tamanho
        if not os.path.exists(arquivo_path):
            info['erro'] = 'Arquivo não encontrado'
            return info
            
        tamanho = os.path.getsize(arquivo_path)
        if tamanho == 0:
            info['erro'] = 'Arquivo vazio'
            info['sugestoes'].append('Verificar se o arquivo foi salvo corretamente')
            return info
        
        # Ler os primeiros bytes para identificar o formato
        with open(arquivo_path, 'rb') as f:
            header = f.read(8)
        
        # Verificar assinaturas de arquivo
        if header.startswith(b'PK\x03\x04'):
            info['formato'] = 'XLSX (ZIP)'
            info['sugestoes'].append('Arquivo parece ser XLSX válido')
        elif header.startswith(b'\xd0\xcf\x11\xe0'):
            info['formato'] = 'XLS (OLE2)'
            info['sugestoes'].append('Arquivo parece ser XLS válido')
        else:
            info['formato'] = f'Desconhecido (header: {header.hex()})'
            info['sugestoes'].extend([
                'Arquivo pode estar corrompido',
                'Tentar salvar novamente no Excel como .xlsx',
                'Verificar se o arquivo não foi truncado durante o upload'
            ])
        
        info['valido'] = header.startswith(b'PK\x03\x04') or header.startswith(b'\xd0\xcf\x11\xe0')
        
    except Exception as e:
        info['erro'] = f'Erro ao analisar arquivo: {str(e)}'
        info['sugestoes'].append('Verificar permissões de acesso ao arquivo')
    
    return info

def limpar_dataframe_para_streamlit(df):
    """
    Limpa DataFrame para evitar erros de serialização do Streamlit/Arrow
    
    Args:
        df: DataFrame original
        
    Returns:
        pd.DataFrame: DataFrame limpo
    """
    if df is None or df.empty:
        return df
        
    df_limpo = df.copy()
    
    # Remover apenas colunas completamente vazias com nomes "Unnamed:"
    colunas_para_remover = []
    for col in df_limpo.columns:
        if col.startswith('Unnamed:') and df_limpo[col].isnull().all():
            colunas_para_remover.append(col)
    
    if colunas_para_remover:
        df_limpo = df_limpo.drop(columns=colunas_para_remover)
    
    # Converter tipos de dados problemáticos
    for coluna in df_limpo.columns:
        # Se a coluna tem tipos mistos, converter tudo para string
        if df_limpo[coluna].dtype == 'object':
            # Verificar se há tipos mistos na coluna
            valores_nao_nulos = df_limpo[coluna].dropna()
            if len(valores_nao_nulos) > 0:
                tipos_unicos = set(type(x).__name__ for x in valores_nao_nulos)
                if len(tipos_unicos) > 1:
                    df_limpo[coluna] = df_limpo[coluna].astype(str)
    
    return df_limpo

def detectar_engine_excel(nome_arquivo):
    """Detecta o engine apropriado para o arquivo Excel"""
    if hasattr(nome_arquivo, 'name'):
        nome_arquivo = nome_arquivo.name
    
    extensao = str(nome_arquivo).lower().split('.')[-1]
    
    if extensao == 'xlsx':
        return 'openpyxl'
    elif extensao == 'xls':
        return 'xlrd'
    else:
        # Default para arquivos sem extensão clara
        return 'openpyxl'

def corrigir_planilha_institucional(df):
    """
    Aplica correções específicas para planilhas institucionais
    Baseado na configuração otimizada para a planilha do Lucas
    
    Args:
        df: DataFrame carregado
        
    Returns:
        DataFrame corrigido com nomes de colunas adequados
    """
    try:
        # Se as colunas são genéricas (Unnamed, números, etc.), aplicar mapeamento
        colunas_genericas = all(
            isinstance(col, int) or 
            str(col).startswith('Unnamed') or 
            str(col).isdigit() 
            for col in df.columns
        )
        
        if colunas_genericas:
            # Mapeamento padrão para planilhas institucionais
            mapeamento_colunas = {
                0: 'Matrícula',
                1: 'Nome', 
                2: 'Situação',
                3: 'Descrição',
                4: 'Pré-matrícula',
                5: 'Turma',
                6: 'Pend_Acad',
                7: 'Cod_Curso',
                8: 'Curso',
                9: 'Cod_Disc_atual',
                10: 'Disciplina_atual',
                11: 'Curriculo',
                12: 'Modulo',
                13: 'Email',
                14: 'Naturalidade',
                15: 'UF_Nascimento'
            }
            
            # Aplicar mapeamento
            novas_colunas = []
            for i, col in enumerate(df.columns):
                if i in mapeamento_colunas:
                    novas_colunas.append(mapeamento_colunas[i])
                else:
                    novas_colunas.append(f'Coluna_{i+1}')
            
            df.columns = novas_colunas
        
        # Remover colunas completamente vazias
        df = df.dropna(axis=1, how='all')
        
        # Remover linhas que são duplicatas do header (problema comum)
        if len(df) > 0:
            primeira_linha = df.iloc[0]
            # Se primeira linha contém nomes de colunas, remover
            if any(str(val).upper() in ['MATRÍCULA', 'NOME', 'SITUAÇÃO', 'CURSO'] 
                   for val in primeira_linha.values if pd.notna(val)):
                df = df.iloc[1:].reset_index(drop=True)
        
        # Limpeza geral de dados
        for col in df.columns:
            if df[col].dtype == 'object':
                # Remover espaços extras
                df[col] = df[col].astype(str).str.strip()
                # Converter 'nan' string para NaN real
                df[col] = df[col].replace(['nan', 'NaN', 'null', ''], pd.NA)
        
        return df
        
    except Exception as e:
        # Se der erro na correção, retornar original
        return df

def detectar_header_automatico(arquivo, engine=None):
    """
    Detecta automaticamente a linha do header em um arquivo Excel de forma ultra-robusta
    Otimizado para planilhas institucionais com formato: Título > Linha vazia > Headers > Dados
    
    Args:
        arquivo: Arquivo Excel ou caminho
        engine: Engine específico para usar
        
    Returns:
        int: Linha do header detectada
    """
    palavras_chave = [
        # Palavras principais (peso alto)
        'MATRÍCULA', 'MATRICULA', 'NOME', 'CURSO', 'SITUAÇÃO', 'SEXO',
        # Palavras específicas da sua planilha
        'TURMA', 'PEND', 'ACAD', 'DISCIPLINA', 'CURRÍCULO', 'MÓDULO',
        # Palavras comuns em headers
        'ID', 'CODIGO', 'DATA', 'STATUS', 'TIPO', 'DESCRICAO'
    ]
    
    try:
        # Tentar múltiplas estratégias de leitura
        strategies = []
        
        if engine:
            strategies.append({'engine': engine})
        else:
            strategies.extend([
                {'engine': 'openpyxl'},
                {'engine': 'xlrd'},
                {'engine': None}
            ])
        
        for strategy in strategies:
            try:
                # Ler primeiras 10 linhas para análise
                read_kwargs = {'header': None, 'nrows': 10}
                if strategy['engine']:
                    read_kwargs['engine'] = strategy['engine']
                
                df_temp = pd.read_excel(arquivo, **read_kwargs)
                
                # Analisar cada linha procurando por headers
                resultados = []
                
                for i in range(min(8, len(df_temp))):  # Aumentei para 8 linhas
                    linha = df_temp.iloc[i]
                    texto_linha = ' '.join([str(valor) for valor in linha.values if pd.notna(valor)]).upper()
                    
                    # Calcular score da linha
                    score = 0
                    palavras_encontradas = []
                    
                    for palavra in palavras_chave:
                        if palavra in texto_linha:
                            # Peso extra para palavras mais importantes
                            if palavra in ['MATRÍCULA', 'MATRICULA', 'NOME', 'CURSO']:
                                score += 3
                            else:
                                score += 1
                            palavras_encontradas.append(palavra)
                    
                    # Bonus: se tem muitas colunas não-vazias (indica header)
                    valores_nao_nulos = [v for v in linha.values if pd.notna(v) and str(v).strip()]
                    if len(valores_nao_nulos) >= 5:
                        score += len(valores_nao_nulos) * 0.5
                    
                    # Penalty: se parece ser dados (números/códigos no início)
                    primeiro_valor = str(valores_nao_nulos[0]) if valores_nao_nulos else ""
                    if primeiro_valor.replace('.', '').replace('-', '').isdigit():
                        score -= 2  # Provavelmente é linha de dados
                    
                    resultados.append({
                        'linha': i,
                        'score': score,
                        'palavras': palavras_encontradas,
                        'texto': texto_linha[:100],  # Primeira parte do texto
                        'colunas_preenchidas': len(valores_nao_nulos)
                    })
                
                # Encontrar a linha com maior score
                if resultados:
                    melhor = max(resultados, key=lambda x: x['score'])
                    
                    # Se tem score razoável (pelo menos 2 palavras-chave), usar
                    if melhor['score'] >= 2:
                        return melhor['linha']
                    
                    # Caso contrário, procurar linha com muitas colunas preenchidas
                    linha_com_mais_colunas = max(resultados, key=lambda x: x['colunas_preenchidas'])
                    if linha_com_mais_colunas['colunas_preenchidas'] >= 5:
                        return linha_com_mais_colunas['linha']
                
                # Fallback: procurar padrão "Base de dados" + linha vazia + headers
                for i in range(min(5, len(df_temp) - 2)):
                    linha_atual = ' '.join([str(v) for v in df_temp.iloc[i].values if pd.notna(v)]).upper()
                    
                    # Se encontrou linha com "BASE DE DADOS" ou similar
                    if any(termo in linha_atual for termo in ['BASE', 'DADOS', 'PLANILHA', 'RELATÓRIO']):
                        # Verificar se a linha i+2 tem headers
                        if i + 2 < len(df_temp):
                            possivel_header = df_temp.iloc[i + 2]
                            texto_header = ' '.join([str(v) for v in possivel_header.values if pd.notna(v)]).upper()
                            palavras_header = sum(1 for palavra in palavras_chave if palavra in texto_header)
                            
                            if palavras_header >= 2:
                                return i + 2
                
                # Se chegou aqui, usar linha 0 como fallback
                return 0
                
            except Exception:
                continue
        
        # Se todas as estratégias falharam, usar 0
        return 0
        
    except Exception:
        # Fallback final
        return 0

def ler_excel_seguro(arquivo, **kwargs):
    """Lê arquivo Excel com tratamento ultra-robusto para diferentes formatos"""
    import tempfile
    import os
    
    # Lista de estratégias para tentar - OTIMIZADA PARA PLANILHAS INSTITUCIONAIS
    estrategias = [
        # CONFIGURAÇÃO ESPECÍFICA PARA PLANILHA DO LUCAS
        {'engine': 'openpyxl', 'skiprows': 2, 'header': 0, 'nome': 'Configuração Institucional'},
        {'engine': 'openpyxl', 'header': 2, 'nome': 'Header Linha 2'},
        {'engine': 'openpyxl', 'read_only': False, 'nome': 'OpenPyXL Padrão'},
        {'engine': 'openpyxl', 'read_only': True, 'nome': 'OpenPyXL Read-Only'},
        {'engine': 'xlrd', 'nome': 'Engine XLRD'},
        {'engine': None, 'nome': 'Pandas Auto'},  # Deixar pandas decidir
    ]
    
    erros = []
    arquivo_temp = None
    
    try:
        # Se o arquivo não for um arquivo temporário, criar um
        if hasattr(arquivo, 'read'):
            # É um arquivo uploadado, salvar temporariamente
            with tempfile.NamedTemporaryFile(delete=False, suffix='.xlsx') as tmp:
                arquivo.seek(0)  # Volta ao início
                tmp.write(arquivo.read())
                arquivo_temp = tmp.name
            arquivo_para_ler = arquivo_temp
        else:
            arquivo_para_ler = arquivo
            
        for i, estrategia in enumerate(estrategias):
            try:
                nome_estrategia = estrategia.get('nome', f'Estratégia {i+1}')
                engine = estrategia.get('engine')
                kwargs_local = kwargs.copy()
                
                # Aplicar configurações específicas da estratégia
                for key, value in estrategia.items():
                    if key not in ['engine', 'nome']:
                        kwargs_local[key] = value
                
                # Remover argumentos que possam causar conflito
                if engine == 'xlrd':
                    kwargs_local.pop('data_only', None)
                    kwargs_local.pop('keep_vba', None)
                    kwargs_local.pop('read_only', None)
                
                # Detectar header se necessário (apenas se não foi especificado na estratégia)
                if 'header' not in kwargs_local and 'skiprows' not in kwargs_local:
                    try:
                        header_linha = detectar_header_automatico(arquivo_para_ler, engine=engine)
                        kwargs_local['header'] = header_linha
                    except:
                        kwargs_local['header'] = 0  # Fallback
                
                # Tentar ler
                if engine is None:
                    df = pd.read_excel(arquivo_para_ler, **kwargs_local)
                else:
                    df = pd.read_excel(arquivo_para_ler, engine=engine, **kwargs_local)
                
                # Aplicar correções pós-leitura para planilhas institucionais
                df = corrigir_planilha_institucional(df)
                
                # Se chegou até aqui, deu certo
                if len(df) > 0:
                    return df
                    
            except Exception as e:
                erro_msg = str(e)
                erros.append(f"{nome_estrategia}: {erro_msg}")
                
                # Log específico para debugging
                if i == 0:  # Primeira estratégia (nossa configuração otimizada)
                    st.info(f"⚠️ Configuração otimizada falhou: {erro_msg[:100]}...")
                
                continue
        
        # Se chegou aqui, todas as estratégias falharam
        raise Exception(f"Todas as estratégias falharam. Detalhes: {' | '.join(erros)}")
        
    finally:
        # Limpar arquivo temporário se criado
        if arquivo_temp and os.path.exists(arquivo_temp):
            try:
                os.unlink(arquivo_temp)
            except:
                pass

def main():
    # Configurar a página
    st.set_page_config(
        page_title="Sistema de Predição de Evasão",
        page_icon="🎓",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Título principal
    st.title("🎓 Sistema de Predição de Evasão Estudantil")
    
    # Criar abas
    tab1, tab2, tab3 = st.tabs(["🤖 Processar Predições", "📊 Dashboard Power BI", "📋 Sobre o Sistema"])
    
    with tab1:
        processar_predicoes_tab()
    
    with tab2:
        dashboard_powerbi_tab()
    
    with tab3:
        sobre_sistema_tab()

def processar_predicoes_tab():
    """Aba principal para processar predições"""
    st.markdown("---")
    
    # Sidebar com informações
    with st.sidebar:
        st.header("� Tutorial AcadWeb")
        
        # Botão para tutorial detalhado
        if st.button("🎯 Como Gerar Excel no AcadWeb", use_container_width=True, type="secondary"):
            st.markdown("""
            ### �📋 **Passo a Passo Rápido:**
            
            1. 🔐 **Acesse AcadWeb** → Seção "Alunos"
            2. ✅ **Marque "Apenas Ativos"** → Clique "Selecionar"  
            3. 🖱️ **Botão direito** em qualquer matrícula
            4. 📊 **"Relatório Excel"** → **"Base de dados"**
            5. 💾 **Baixe arquivo** (31 colunas, ~955 alunos)
            6. 📤 **Upload aqui** na seção de processamento
            
            ⚡ **Processamento automático em < 30s!**
            """)
            
        st.info("💡 **Tutorial Detalhado:** Execute `streamlit run tutorial_acadweb.py --server.port 8508`")
        
        st.markdown("---")
        
        st.header("📋 Como usar:")
        st.markdown("""
        1. **Upload** da planilha Excel com dados dos alunos
        2. **Clique** em "Processar Predições" 
        3. **Aguarde** o processamento
        4. **Download** do arquivo CSV resultante
        5. **Importe** no Power BI
        """)
        
        st.success("🎯 **Otimizado para AcadWeb**")
        st.markdown("- ✅ Detecção automática de header")
        st.markdown("- ✅ 955+ alunos suportados") 
        st.markdown("- ✅ 31 colunas reconhecidas")
        st.markdown("- ✅ Processamento < 30s")
        
        st.markdown("---")
        st.subheader("📊 Colunas necessárias:")
        st.text("""
        • Nome
        • Matrícula  
        • Pend. Financ.
        • Faltas Consecutivas
        • Pend. Acad.
        • Curso
        • Sexo
        • Turma Atual
        """)
    
    # Área principal
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("📁 1. Upload da Planilha de Alunos")
        uploaded_file = st.file_uploader(
            "Selecione o arquivo Excel (.xlsx ou .xls)",
            type=['xlsx', 'xls'],
            help="Faça upload da planilha com os dados dos alunos ativos"
        )
        
        if uploaded_file is not None:
            # Mostrar preview dos dados
            try:
                # Usar função robusta de leitura
                df_preview = ler_excel_seguro(uploaded_file, nrows=5)
                
                st.success(f"✅ Arquivo carregado: {uploaded_file.name}")
                st.subheader("👀 Preview dos dados (primeiras 5 linhas):")
                
                # Limpar DataFrame antes de mostrar
                df_preview_limpo = limpar_dataframe_para_streamlit(df_preview)
                st.dataframe(df_preview_limpo)
                
                # Verificar colunas essenciais
                colunas_necessarias = ['Nome', 'Matrícula']
                colunas_encontradas = [col for col in colunas_necessarias if col in df_preview.columns]
                
                if len(colunas_encontradas) >= 1:
                    st.success(f"✅ Colunas básicas encontradas: {', '.join(colunas_encontradas)}")
                else:
                    st.warning("⚠️ Verifique se as colunas necessárias estão presentes")
                    
                # Mostrar todas as colunas disponíveis
                with st.expander("🔍 Ver todas as colunas disponíveis"):
                    st.write(f"**Colunas encontradas ({len(df_preview.columns)}):**")
                    for i, col in enumerate(df_preview.columns, 1):
                        st.write(f"{i}. {col}")
                
            except Exception as e:
                st.error(f"❌ Erro ao ler arquivo: {str(e)}")
                st.info("💡 Dicas para resolver:")
                st.markdown("""
                - **Formato**: Certifique-se que o arquivo é .xlsx ou .xls
                - **Integridade**: Verifique se o arquivo não está corrompido
                - **Compatibilidade**: Tente salvar novamente no Excel como .xlsx
                - **Caracteres**: Evite caracteres especiais no nome do arquivo
                - **Permissões**: Certifique-se que o arquivo não está aberto no Excel
                """)
                uploaded_file = None
    
    with col2:
        st.subheader("⚙️ Status do Sistema")
        
        # Verificar se sistema está pronto
        if st.button("🔍 Verificar Sistema"):
            with st.spinner("Verificando sistema..."):
                try:
                    sistema = SistemaPredicaoEvasao()
                    sistema.inicializar()
                    st.success("✅ Sistema pronto!")
                    st.info("🤖 Modelo carregado")
                    st.info("📏 Regras configuradas")
                except Exception as e:
                    st.error(f"❌ Erro no sistema: {str(e)}")
    
    # Botão de processamento
    st.markdown("---")
    if uploaded_file is not None:
        col1, col2, col3 = st.columns([1, 2, 1])
        
        with col2:
            if st.button("🚀 Processar Predições", type="primary", use_container_width=True):
                processar_predicoes(uploaded_file)
    else:
        st.info("👆 Faça upload de uma planilha para continuar")

def dashboard_powerbi_tab():
    """Aba com dashboard do Power BI integrado"""
    st.header("📊 Dashboard Power BI - Análise de Evasão")
    st.markdown("---")
    
    # URL do seu Power BI
    powerbi_url = "https://app.powerbi.com/view?r=eyJrIjoiZTg2MmYwZTItZjgzZi00ODNmLTk0NTEtMTAzZWRmNDBkZGMwIiwidCI6IjZmZjM3NGY1LWUzZWItNGM2Zi1iN2I1LTUwOTE2NDA5MzdmOCJ9"
    
    # Informações sobre o dashboard
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("""
        ### 📈 Visualização Interativa
        Este dashboard apresenta análises em tempo real dos dados de predição de evasão:
        
        - 📊 **Distribuição de Alunos por Status**
        - 🎯 **Casos Prioritários por Urgência**  
        - 📈 **Tendências por Curso e Período**
        - 🔍 **Fatores de Risco Principais**
        - 📋 **Lista de Alunos em Risco**
        """)
    
    with col2:
        st.info("""
        💡 **Dica:**
        
        Após processar uma nova planilha na aba "Processar Predições", 
        atualize este dashboard para ver os novos dados.
        
        🔄 Use o botão de atualizar do Power BI para carregar dados mais recentes.
        """)
    
    # Incorporar o Power BI via iframe
    st.markdown("### 📊 Dashboard Interativo:")
    
    # Criar iframe com o Power BI
    iframe_html = f"""
    <iframe 
        title="Dashboard Predição Evasão" 
        width="100%" 
        height="800" 
        src="{powerbi_url}&chromeless=1"
        frameborder="0" 
        allowFullScreen="true">
    </iframe>
    """
    
    # Exibir o iframe
    st.components.v1.html(iframe_html, height=800)
    
    # Botões de ação
    st.markdown("---")
    col1, col2, col3 = st.columns([1, 1, 1])
    
    with col1:
        if st.button("🔄 Atualizar Dashboard", use_container_width=True):
            st.rerun()
    
    with col2:
        if st.button("🔗 Abrir em Nova Aba", use_container_width=True):
            st.markdown(f'<a href="{powerbi_url}" target="_blank">Abrir Power BI</a>', unsafe_allow_html=True)
    
    with col3:
        st.download_button(
            label="📥 Baixar Link",
            data=powerbi_url,
            file_name="dashboard_powerbi.txt",
            mime="text/plain",
            use_container_width=True
        )

def sobre_sistema_tab():
    """Aba com informações sobre o sistema"""
    st.header("📋 Sobre o Sistema de Predição de Evasão")
    st.markdown("---")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("""
        ### 🎯 **Objetivo**
        Sistema híbrido inteligente que combina **Machine Learning** com **Regras de Negócio** 
        para identificar alunos em risco de evasão escolar.
        
        ### ✨ **Principais Características**
        - 🤖 **Modelo XGBoost** treinado com dados históricos
        - 📏 **Regras de Negócio** específicas do Grau Técnico  
        - 🔍 **Explicabilidade SHAP** para interpretação das predições
        - 📊 **Relatórios Detalhados** em formato CSV
        - ⚡ **Sistema de Urgência** para priorização de ações
        
        ### 📊 **Como Interpretar os Resultados**
        
        **Status de Predição:**
        - 🟢 **MATRICULADO**: Aluno com baixo risco de evasão
        - 🔴 **RISCO_EVASAO**: Aluno que precisa de atenção
        
        **Níveis de Urgência:**
        - 🚨 **URGENTE**: Ação imediata (até 3 dias)
        - 🔴 **ALTA**: Ação prioritária (1-2 semanas)
        - 🟡 **MEDIA**: Monitoramento próximo (1 mês)
        - 🟢 **BAIXA**: Acompanhamento normal
        """)
    
    with col2:
        st.markdown("""
        ### 🔧 **Especificações Técnicas**
        
        **Modelo de ML:**
        - Algoritmo: XGBoost
        - Features: 12 variáveis
        - Classes: 13 situações
        - Acurácia: ~73%
        
        **Regras de Negócio:**
        - LFI: Limpeza Financeira
        - LAC: Limpeza Acadêmica  
        - LFR: Limpeza Frequência
        - NC: Nunca Compareceu
        - MT: Matriculado
        - NF: Não Formado
        
        **Dados de Entrada:**
        - Pendências Financeiras
        - Faltas Consecutivas
        - Pendências Acadêmicas
        - Informações do Curso
        - Dados Demográficos
        """)
        
        st.markdown("---")
        st.info("""
        📞 **Suporte Técnico**
        
        Para dúvidas ou problemas:
        - Anote mensagens de erro
        - Informe qual arquivo estava processando
        - Entre em contato com TI
        """)
    
    # Estatísticas do sistema (se disponível)
    st.markdown("---")
    st.subheader("📈 Estatísticas do Sistema")
    
    try:
        # Tentar carregar estatísticas do último processamento
        import os
        if os.path.exists("output/analise_completa.csv"):
            df_stats = pd.read_csv("output/analise_completa.csv")
            
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                total_alunos = len(df_stats)
                st.metric("👥 Último Processamento", f"{total_alunos} alunos")
            
            with col2:
                matriculados = len(df_stats[df_stats['Status_Predicao'] == 'MATRICULADO'])
                perc_matriculados = (matriculados / total_alunos) * 100 if total_alunos > 0 else 0
                st.metric("✅ Matriculados", f"{matriculados}", f"{perc_matriculados:.1f}%")
            
            with col3:
                em_risco = len(df_stats[df_stats['Status_Predicao'] == 'RISCO_EVASAO'])
                perc_risco = (em_risco / total_alunos) * 100 if total_alunos > 0 else 0
                st.metric("⚠️ Em Risco", f"{em_risco}", f"{perc_risco:.1f}%")
            
            with col4:
                urgentes = len(df_stats[df_stats['Nivel_Urgencia'] == 'URGENTE'])
                st.metric("🚨 Casos Urgentes", f"{urgentes}")
                
    except Exception:
        st.info("📊 Execute um processamento para ver estatísticas")

    # Sidebar com informações
    with st.sidebar:
        st.header("📋 Como usar:")
        st.markdown("""
        **Aba Processar:**
        1. Upload da planilha Excel
        2. Clique em "Processar Predições" 
        3. Aguarde o processamento
        4. Download do arquivo CSV
        5. Use no Power BI
        
        **Aba Dashboard:**
        - Visualize resultados em tempo real
        - Dashboard interativo do Power BI
        - Gráficos e análises detalhadas
        
        **Aba Sobre:**
        - Informações do sistema
        - Como interpretar resultados
        - Especificações técnicas
        """)
        
        st.markdown("---")
        st.subheader("📊 Colunas necessárias:")
        st.text("""
        Obrigatórias:
        • Nome
        • Matrícula  
        
        Recomendadas:
        • Pend. Financ.
        • Faltas Consecutivas
        • Pend. Acad.
        • Curso
        • Sexo
        • Turma Atual
        """)

def processar_predicoes(uploaded_file):
    """Processa as predições e disponibiliza download"""
    
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    try:
        # Passo 1: Salvar arquivo temporário
        status_text.text("📁 Salvando arquivo...")
        progress_bar.progress(10)
        
        # Determinar extensão apropriada
        extensao_arquivo = uploaded_file.name.lower().split('.')[-1]
        sufixo = f'.{extensao_arquivo}' if extensao_arquivo in ['xlsx', 'xls'] else '.xlsx'
        
        with tempfile.NamedTemporaryFile(delete=False, suffix=sufixo) as tmp_file:
            tmp_file.write(uploaded_file.read())
            arquivo_temp = tmp_file.name
        
        # Verificar se conseguimos ler o arquivo salvo
        try:
            # Primeiro, verificar a integridade do arquivo
            info_arquivo = verificar_arquivo_excel(arquivo_temp)
            
            if not info_arquivo['valido']:
                os.unlink(arquivo_temp)
                st.error(f"❌ Arquivo inválido: {info_arquivo.get('erro', 'Formato não reconhecido')}")
                st.warning(f"🔍 Formato detectado: {info_arquivo['formato']}")
                
                if info_arquivo['sugestoes']:
                    st.info("💡 Sugestões:")
                    for sugestao in info_arquivo['sugestoes']:
                        st.markdown(f"- {sugestao}")
                
                st.markdown("""
                ### 🛠️ Soluções Adicionais:
                - **Recriar o arquivo**: Copie os dados para uma nova planilha Excel
                - **Verificar origem**: Arquivo pode ter sido baixado incorretamente
                - **Formato correto**: Use Excel (.xlsx) ou LibreOffice (.ods > Salvar como .xlsx)
                - **Tamanho do arquivo**: Verifique se não está truncado
                """)
                return
            
            # Se o arquivo é válido, tentar ler
            test_df = ler_excel_seguro(arquivo_temp, nrows=1)
            st.success(f"✅ Arquivo validado: {len(test_df.columns)} colunas encontradas")
            st.info(f"📄 Formato: {info_arquivo['formato']}")
                
        except Exception as e:
            os.unlink(arquivo_temp)
            
            # Análise mais detalhada do erro
            erro_str = str(e)
            st.error(f"❌ Erro ao validar arquivo: {erro_str}")
            
            # Criar seção expansível com diagnóstico detalhado
            with st.expander("🔍 Diagnóstico Avançado", expanded=False):
                st.markdown("### Informações técnicas do erro:")
                st.code(erro_str, language="text")
                
                # Tentar diagnóstico básico do arquivo
                try:
                    # Recriar arquivo temporário para análise
                    with tempfile.NamedTemporaryFile(delete=False, suffix='.xlsx') as tmp_diag:
                        uploaded_file.seek(0)
                        tmp_diag.write(uploaded_file.read())
                        arquivo_diag = tmp_diag.name
                    
                    # Análise básica
                    tamanho = os.path.getsize(arquivo_diag)
                    st.write(f"📏 **Tamanho do arquivo**: {tamanho:,} bytes")
                    
                    with open(arquivo_diag, 'rb') as f:
                        header = f.read(16)
                    st.write(f"🔢 **Header (primeiros 16 bytes)**: `{header.hex()}`")
                    
                    if header.startswith(b'PK\x03\x04'):
                        st.write("✅ **Formato detectado**: XLSX (ZIP válido)")
                    elif header.startswith(b'\xd0\xcf\x11\xe0'):
                        st.write("✅ **Formato detectado**: XLS (OLE2 válido)")  
                    else:
                        st.write("❌ **Formato detectado**: Não reconhecido")
                        st.warning("⚠️ O arquivo pode estar corrompido ou ter formato incompatível")
                    
                    os.unlink(arquivo_diag)
                    
                except Exception as diag_error:
                    st.write(f"❌ Erro no diagnóstico: {diag_error}")
            
            # Sugestões baseadas no tipo de erro
            if "Invalid argument" in erro_str:
                st.warning("🚨 **Problema detectado**: Arquivo pode estar corrompido ou ter caracteres inválidos no caminho")
                st.info("💡 **Soluções específicas:**")
                st.markdown("""
                1. **📁 Verificar o arquivo original**:
                   - Abra o arquivo diretamente no Excel
                   - Verifique se abre sem problemas
                   - Se não abrir, o arquivo está corrompido
                
                2. **🔄 Recriar o arquivo**:
                   - Selecione todos os dados no Excel (Ctrl+A)
                   - Copie (Ctrl+C) 
                   - Cole em uma nova planilha (Ctrl+V)
                   - Salve como novo arquivo .xlsx
                
                3. **📂 Verificar local do arquivo**:
                   - Evite pastas com nomes muito longos
                   - Use apenas letras e números no nome do arquivo
                   - Mova para uma pasta simples (ex: Desktop)
                """)
                
            elif "BOF record" in erro_str or "corrupt file" in erro_str:
                st.warning("🚨 **Problema detectado**: Arquivo corrompido ou formato incompatível")
                st.info("💡 **Soluções específicas:**")
                st.markdown("""
                1. **🔧 Reparar no Excel**:
                   - Abra o Excel
                   - Vá em File > Open
                   - Selecione o arquivo
                   - Se der erro, escolha "Sim" para reparar
                   - Salve como novo arquivo
                
                2. **💾 Recriar completamente**:
                   - O arquivo original pode estar irreparavelmente danificado
                   - Solicite uma nova cópia da fonte original
                   - Ou digite os dados manualmente em nova planilha
                
                3. **🔄 Converter formato**:
                   - Tente abrir no LibreOffice Calc
                   - Salve como Excel (.xlsx)
                   - Use este novo arquivo
                """)
                
            elif "Unsupported format" in erro_str:
                st.warning("🚨 **Problema detectado**: Formato de arquivo não suportado")
                st.info("💡 **Soluções específicas:**")
                st.markdown("""
                1. **📝 Verificar extensão**:
                   - Certifique-se que o arquivo tem extensão .xlsx ou .xls
                   - Se tiver extensão diferente, renomeie
                
                2. **💾 Salvar no formato correto**:
                   - Abra no Excel
                   - File > Save As
                   - Escolha "Excel Workbook (*.xlsx)"
                   - Salve com novo nome
                
                3. **🔍 Verificar tipo real**:
                   - O arquivo pode não ser realmente um Excel
                   - Verifique se não é um CSV renomeado
                   - Abra no Notepad para verificar conteúdo
                """)
            else:
                st.info("💡 **Soluções gerais:**")
                st.markdown("""
                - **✅ Usar Excel original**: Abra e salve novamente no Microsoft Excel
                - **🔄 Tentar formato .xlsx**: Sempre prefira .xlsx ao invés de .xls  
                - **📋 Verificar dados**: Certifique-se que há dados na primeira aba
                - **🚫 Remover proteções**: Desproteja a planilha se estiver protegida
                - **💾 Nova cópia**: Use uma versão mais recente do arquivo original
                """)
                
            return
        
        # Passo 2: Inicializar sistema
        status_text.text("🔧 Inicializando sistema...")
        progress_bar.progress(30)
        
        sistema = SistemaPredicaoEvasao()
        sistema.inicializar()
        
        # Passo 3: Processar predições
        status_text.text("🤖 Processando predições...")
        progress_bar.progress(60)
        
        predicoes, estatisticas = sistema.predizer_alunos(Path(arquivo_temp))
        
        # Passo 4: Gerar CSV
        status_text.text("📊 Gerando relatório...")
        progress_bar.progress(80)
        
        # Criar DataFrame com resultados
        dados_csv = []
        for predicao in predicoes:
            dados_csv.append({
                'Nome': predicao.nome,
                'Matricula': predicao.matricula,
                'Curso': predicao.curso,
                'Sexo': predicao.sexo,
                'Status_Predicao': predicao.status_predicao,
                'Situacao_Predita': predicao.situacao_predita,
                'Probabilidade_Situacao': predicao.probabilidade_situacao,
                'Nivel_Urgencia': predicao.nivel_urgencia,
                'Fator_Principal': predicao.fator_principal,
                'Valor_Importancia': predicao.valor_importancia,
                'Fonte_Predicao': predicao.fonte_predicao
            })
        
        df_resultado = pd.DataFrame(dados_csv)
        
        # Passo 5: Finalizar
        progress_bar.progress(100)
        status_text.text("✅ Processamento concluído!")
        
        # Mostrar estatísticas
        st.success("🎉 Predições processadas com sucesso!")
        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("👥 Total de Alunos", len(predicoes))
        with col2:
            matriculados = len([p for p in predicoes if p.status_predicao == 'MATRICULADO'])
            st.metric("✅ Matriculados", matriculados)
        with col3:
            em_risco = len([p for p in predicoes if p.status_predicao == 'RISCO_EVASAO'])
            st.metric("⚠️ Em Risco", em_risco)
        with col4:
            urgentes = len([p for p in predicoes if p.nivel_urgencia == 'URGENTE'])
            st.metric("🚨 Urgentes", urgentes)
        
        # Preview do resultado
        st.subheader("📋 Preview do Resultado:")
        df_resultado_limpo = limpar_dataframe_para_streamlit(df_resultado)
        st.dataframe(df_resultado_limpo.head(10))
        
        # Botão de download
        csv_data = df_resultado.to_csv(index=False)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        nome_arquivo = f"predicao_evasao_{timestamp}.csv"
        
        st.download_button(
            label="📥 Download CSV para Power BI",
            data=csv_data,
            file_name=nome_arquivo,
            mime="text/csv",
            type="primary",
            use_container_width=True
        )
        
        # Limpar arquivo temporário
        os.unlink(arquivo_temp)
        
    except Exception as e:
        st.error(f"❌ Erro durante processamento: {str(e)}")
        status_text.text("❌ Erro no processamento")

if __name__ == "__main__":
    main()