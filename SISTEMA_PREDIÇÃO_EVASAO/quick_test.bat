@echo off
echo ====================================
echo   TESTE RAPIDO DO SISTEMA DE PREDICAO
echo ====================================

echo.
echo 1. Ativando ambiente virtual...
call .venv\Scripts\activate.bat

echo.
echo 2. Testando importacoes basicas...
python -c "import sys, os; sys.path.insert(0, os.getcwd()); from codigo_fonte.configuracao import configuracoes; print('✅ Importações OK')"
if %errorlevel% neq 0 (
    echo ❌ Erro nas importacoes
    pause
    exit /b 1
)

echo.
echo 3. Executando sistema principal...
python principal.py

echo.
echo 4. Verificando arquivo de saida...
if exist "output\analise_completa.csv" (
    echo ✅ Arquivo CSV gerado com sucesso
    for %%A in (output\analise_completa.csv) do echo    Tamanho: %%~zA bytes
) else (
    echo ❌ Arquivo CSV nao foi gerado
)

echo.
echo ====================================
echo   TESTE CONCLUIDO
echo ====================================
pause