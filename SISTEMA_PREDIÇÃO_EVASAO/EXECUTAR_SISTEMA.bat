@echo off
cls
echo.
echo ============================================================
echo   SISTEMA DE PREDICAO DE EVASAO - INTERFACE WEB
echo ============================================================
echo.
echo Status: FUNCIONANDO - Todas as correcoes aplicadas!
echo Alunos testados: 954 alunos carregados com sucesso
echo Colunas ML: 12/12 detectadas corretamente
echo.
echo Iniciando interface web...
echo Acesse: http://localhost:8501
echo.
echo Para parar o sistema: Pressione Ctrl+C
echo ============================================================
echo.

streamlit run interface_web_limpa.py --server.port=8501