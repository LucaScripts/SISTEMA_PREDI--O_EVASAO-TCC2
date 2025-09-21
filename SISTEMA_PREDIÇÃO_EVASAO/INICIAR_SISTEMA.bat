@echo off
cls
echo.
echo ============================================================
echo   SISTEMA DE PREDICAO DE EVASAO - GRAU TECNICO
echo ============================================================
echo.
echo 🚀 Iniciando Sistema Organizado...
echo 📊 Interface Web Streamlit
echo 🎯 Versao Final - Estrutura Limpa
echo.
echo 💡 Acesse: http://localhost:8501
echo.
echo Para parar o sistema: Pressione Ctrl+C
echo ============================================================
echo.

python -m streamlit run interface_web_limpa.py --server.port=8501

pause