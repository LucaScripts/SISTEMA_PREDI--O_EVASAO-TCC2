def dashboard_powerbi_tab():
    """Aba do dashboard Power BI integrado"""
    
    st.markdown("---")
    st.subheader("📊 Dashboard Interativo - Power BI")
    
    # Dashboard embarcado diretamente na interface
    st.success("✅ **Dashboard integrado!** Visualize os dados diretamente aqui:")
    
    # URL do Power BI para embedding
    dashboard_embed_url = "https://app.powerbi.com/view?r=eyJrIjoiZTg2MmYwZTItZjgzZi00ODNmLTk0NTEtMTAzZWRmNDBkZGMwIiwidCI6IjZmZjM3NGY1LWUzZWItNGM2Zi1iN2I1LTUwOTE2NDA5MzdmOCJ9"
    
    # Iframe responsivo do Power BI
    st.markdown(f"""
    <div style="width: 100%; height: 600px; border: 2px solid #0078d4; border-radius: 10px; margin: 20px 0; overflow: hidden;">
        <iframe src="{dashboard_embed_url}" 
                width="100%" 
                height="600" 
                frameborder="0" 
                allowFullScreen="true"
                style="border-radius: 8px;">
        </iframe>
    </div>
    """, unsafe_allow_html=True)
    
    # Controles do dashboard
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("🔄 Atualizar Dashboard"):
            st.success("Dashboard atualizado! Os dados mais recentes serão exibidos.")
            st.rerun()
    
    with col2:
        if st.button("📱 Tela Cheia"):
            st.info("💡 Use F11 para visualização em tela cheia ou clique no ícone de expansão no Power BI acima.")
    
    with col3:
        if st.button("🔗 Abrir em Nova Aba"):
            st.markdown(f'<a href="{dashboard_embed_url}" target="_blank">Clique aqui para abrir em nova aba</a>', unsafe_allow_html=True)
    
    # Informações sobre atualização
    st.info("""
    🕐 **Horários de Atualização Automática:**
    
    O dashboard é atualizado automaticamente nos seguintes horários:
    **08h, 09h, 10h, 11h, 14h, 15h, 16h, 17h**
    
    📊 Após processar novos alunos neste sistema, aguarde até o próximo horário 
    de atualização para ver os dados mais recentes no dashboard acima.
    """)
    
    # Informações sobre uso
    with st.expander("📖 Como usar este dashboard"):
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
            **📈 Funcionalidades Disponíveis:**
            - 🎯 **Filtros interativos** por curso, turma, período
            - 📊 **Gráficos dinâmicos** de distribuição de risco
            - 🔍 **Busca por aluno** específico
            - 📅 **Análise temporal** de tendências
            - 🎨 **Cores intuitivas** (🔴🟠🟡🔵⚪) por urgência
            """)
        
        with col2:
            st.markdown("""
            **🎯 Métricas Principais:**
            - 📊 **Taxa de evasão** prevista por curso
            - 🚨 **Alunos em risco** crítico (urgente/alta)
            - ✅ **Comparações** entre turmas/períodos
            - 💰 **Insights** para ações preventivas
            - 📈 **Evolução** de indicadores no tempo
            """)
    
    # Fluxo automatizado
    st.markdown("### 🚀 **Fluxo Integrado**")
    
    st.success("""
    **Experiência completa em uma só tela:**
    
    1. 👤 **Processe dados** na aba "Processar Predições"
    2. ✅ **Marque** "Atualizar Power BI automaticamente"  
    3. 💾 **Aguarde** o processamento (dados salvos automaticamente)
    4. ⏰ **Volte a esta aba** no próximo horário programado
    5. 🔄 **Clique** "Atualizar Dashboard" para ver novos dados
    6. 📊 **Analise** resultados diretamente aqui!
    
    **Sem necessidade de abrir links externos ou trocar de janela! 🎉**
    """)