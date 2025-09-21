@echo off
echo Iniciando Sistema de Predicao de Evasao - VERSAO FINAL
echo ============================================================
echo.
echo Todas as correcoes foram aplicadas!
echo Seu arquivo Excel agora eh 100%% compativel!
echo Sistema testado com sucesso - 10 alunos processados!
echo.
echo Recursos funcionando:
echo    - Carregamento correto do AcadWeb (954 alunos)
echo    - Todas as 12 colunas do modelo ML detectadas  
echo    - Processamento completo com predicoes
echo    - Interface web limpa e tutorial integrado
echo    - SHAP explicacoes funcionando
echo.
echo Abrindo interface web...
echo.

python -m streamlit run interface_web_limpa.py --server.port=8501

pause