@echo off
echo 🚀 Iniciando Sistema de Predição de Evasão
echo =========================================

echo 📋 Ativando ambiente virtual...
call ".venv\Scripts\activate.bat"

echo 🔍 Verificando dependências...
python -c "import streamlit, pandas, numpy, xgboost, shap; print('✅ Todas as dependências OK!')"

echo 🌐 Iniciando interface web...
echo 💡 Acesse: http://localhost:8501
echo 
streamlit run interface_web.py

pause