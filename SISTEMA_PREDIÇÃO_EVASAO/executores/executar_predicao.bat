@echo off
echo =====================================
echo   SISTEMA DE PREDICAO DE EVASAO
echo =====================================
echo.

:: Verificar se há arquivos Excel na pasta input
if not exist "input\*.xlsx" (
    echo ❌ ERRO: Nenhum arquivo Excel encontrado na pasta 'input'
    echo.
    echo 📋 INSTRUCOES:
    echo 1. Coloque seu arquivo Excel na pasta 'input'
    echo 2. Execute este script novamente
    echo.
    pause
    exit /b 1
)

echo 📁 Arquivo encontrado na pasta input:
for %%f in (input\*.xlsx) do echo    %%~nxf

echo.
echo 🚀 Iniciando processamento...
echo ⏳ Aguarde, isso pode levar alguns segundos...
echo.

:: Executar o sistema Python
".venv\Scripts\python.exe" processar_producao.py

if %errorlevel% equ 0 (
    echo.
    echo ✅ PROCESSAMENTO CONCLUIDO!
    echo 📊 Arquivo CSV gerado na pasta 'output'
    echo 🔗 Importe este arquivo no Power BI
    echo.
    echo 📁 Abrindo pasta de resultados...
    start "" "output"
) else (
    echo.
    echo ❌ ERRO durante o processamento
    echo 📞 Entre em contato com suporte técnico
)

echo.
pause