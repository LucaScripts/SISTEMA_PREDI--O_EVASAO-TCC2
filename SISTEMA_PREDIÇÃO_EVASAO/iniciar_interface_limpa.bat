@echo off
echo 🚀 Iniciando Sistema de Predição de Evasão - Interface Limpa
echo ============================================================

cd /d "C:\Users\lucas\Downloads\TCC2\SISTEMA_PREDIÇÃO_EVASAO TCC2\SISTEMA_PREDIÇÃO_EVASAO"

echo 📂 Diretório: %CD%
echo 🔧 Ativando ambiente virtual...

call .venv\Scripts\activate.bat

echo 🌐 Iniciando interface web...
echo 💡 Acesse: http://localhost:8509
echo.

.venv\Scripts\python.exe -m streamlit run interface_web_limpa.py --server.port 8509

pause