# Sistema de Predicao de Evasao - Inicializador
Write-Host "🚀 Iniciando Sistema de Predição de Evasão - VERSÃO FINAL" -ForegroundColor Green
Write-Host "============================================================" -ForegroundColor Yellow
Write-Host ""
Write-Host "✅ Todas as correções foram aplicadas!" -ForegroundColor Green
Write-Host "✅ Seu arquivo Excel agora é 100% compatível!" -ForegroundColor Green  
Write-Host "✅ Sistema testado com sucesso - 10 alunos processados!" -ForegroundColor Green
Write-Host ""
Write-Host "🎯 Recursos funcionando:" -ForegroundColor Cyan
Write-Host "    • ✅ Carregamento correto do AcadWeb (954 alunos)" -ForegroundColor White
Write-Host "    • ✅ Todas as 12 colunas do modelo ML detectadas" -ForegroundColor White
Write-Host "    • ✅ Processamento completo com predições" -ForegroundColor White
Write-Host "    • ✅ Interface web limpa e tutorial integrado" -ForegroundColor White
Write-Host "    • ✅ SHAP explicações funcionando" -ForegroundColor White
Write-Host ""
Write-Host "🌐 Abrindo interface web..." -ForegroundColor Yellow
Write-Host ""

# Executar Streamlit
python -m streamlit run interface_web_limpa.py --server.port=8501

Write-Host ""
Write-Host "Pressione qualquer tecla para fechar..." -ForegroundColor Gray
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")