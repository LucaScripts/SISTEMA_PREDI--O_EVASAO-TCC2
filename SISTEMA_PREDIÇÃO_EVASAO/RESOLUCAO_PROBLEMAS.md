# 🚨 Guia de Resolução de Problemas

Este documento contém soluções para problemas comuns que podem ocorrer durante o uso do Sistema de Predição de Evasão.

## 📋 Problemas com Upload de Arquivos Excel

### ❌ "Excel file format cannot be determined"
**Causa:** Formato de arquivo não reconhecido ou arquivo corrompido.

**Soluções:**
1. **Salvar como .xlsx:**
   - Abra o arquivo no Excel
   - Vá em "Arquivo" > "Salvar Como"
   - Escolha formato "Excel Workbook (*.xlsx)"

2. **Verificar integridade:**
   - Tente abrir o arquivo no Excel primeiro
   - Se não abrir, o arquivo pode estar corrompido

3. **Remover caracteres especiais:**
   - Evite caracteres especiais no nome do arquivo
   - Use apenas letras, números e underscores

### ❌ "Permission denied" ou "File is locked"
**Causa:** Arquivo está aberto no Excel ou sem permissão.

**Soluções:**
1. Feche o arquivo no Excel completamente
2. Verifique se você tem permissão para acessar o arquivo
3. Copie o arquivo para uma nova localização

### ❌ "No columns found" ou "Empty file"
**Causa:** Arquivo vazio ou sem dados na primeira planilha.

**Soluções:**
1. Verifique se o arquivo contém dados
2. Certifique-se que os dados estão na primeira aba
3. Verifique se há cabeçalhos nas colunas

## 🌐 Problemas com Interface Web

### ❌ "Port 8501 is already in use"
**Causa:** O Streamlit já está rodando em outra instância.

**Soluções:**
1. Feche outras instâncias do navegador com localhost:8501
2. Use outro porto: `streamlit run interface_web.py --server.port 8502`
3. Reinicie o computador se necessário

### ❌ Interface não carrega ou fica em branco
**Causa:** Problemas de rede ou dependências.

**Soluções:**
1. Aguarde alguns segundos - pode estar inicializando
2. Recarregue a página (F5)
3. Limpe o cache do navegador
4. Tente outro navegador

### ❌ Dashboard Power BI não aparece
**Causa:** Problemas de iframe ou conectividade.

**Soluções:**
1. Verifique sua conexão com a internet
2. Desabilite bloqueadores de anúncio/popup
3. Permita iframe no seu navegador
4. Tente em modo anônimo/incógnito

## 🤖 Problemas de Processamento

### ❌ "Erro ao inicializar sistema"
**Causa:** Modelos ML ou arquivos de configuração não encontrados.

**Soluções:**
1. Verifique se a pasta `data/models/` contém os arquivos:
   - `modelo_xgboost_sem_classes_criticas.pkl`
   - `class_mapping_otimizado.pkl`
   - `training_artifacts.pkl`

2. Execute o treinamento do modelo:
   ```bash
   python scripts/train_model.py
   ```

### ❌ "Colunas obrigatórias não encontradas"
**Causa:** Arquivo Excel não contém as colunas esperadas.

**Soluções:**
1. Verifique se o arquivo contém as colunas básicas:
   - Nome do Aluno
   - Matrícula
   - Curso
   - Sexo
   
2. Use como referência: `data/raw/alunos_ativos_atual.xlsx`

### ❌ Processamento muito lento
**Causa:** Arquivo muito grande ou recursos limitados.

**Soluções:**
1. Processe arquivos menores (< 10.000 linhas por vez)
2. Feche outros programas para liberar memória
3. Aguarde - o processamento pode demorar alguns minutos

## 💻 Problemas de Instalação

### ❌ "Python não encontrado"
**Causa:** Python não instalado ou não no PATH.

**Soluções:**
1. Instale Python 3.8+ do site oficial
2. Marque "Add Python to PATH" na instalação
3. Reinicie o prompt de comando

### ❌ "pip não funciona"
**Causa:** pip não instalado ou ambiente virtual não ativo.

**Soluções:**
1. Ative o ambiente virtual:
   ```bash
   .venv\Scripts\activate
   ```

2. Reinstale pip:
   ```bash
   python -m ensurepip --upgrade
   ```

### ❌ Erro ao instalar dependências
**Causa:** Conflitos de versão ou falta de compiladores.

**Soluções:**
1. Atualize pip:
   ```bash
   python -m pip install --upgrade pip
   ```

2. Instale uma dependência por vez:
   ```bash
   pip install pandas
   pip install streamlit
   ```

3. Use versões específicas:
   ```bash
   pip install -r requirements.txt --no-deps
   ```

## 📞 Suporte Adicional

Se o problema persistir:

1. **Verifique os logs:** `sistema_predicao_evasao.log`
2. **Documente o erro:** Print screen da mensagem de erro
3. **Contexto:** Qual ação estava executando quando o erro ocorreu
4. **Ambiente:** Versão do Windows, Python, navegador

### 📧 Informações para Suporte
Ao solicitar ajuda, inclua:
- Versão do sistema operacional
- Versão do Python (`python --version`)
- Conteúdo do arquivo de erro/log
- Passos para reproduzir o problema

---

## 🔧 Comandos Úteis

### Verificar instalação:
```bash
python --version
pip list
```

### Reinstalar sistema:
```bash
pip uninstall -r requirements.txt -y
pip install -r requirements.txt
```

### Limpar cache Python:
```bash
python -Bc "import pathlib; [p.unlink() for p in pathlib.Path('.').rglob('*.py[co]')]"
python -Bc "import pathlib; [p.rmdir() for p in pathlib.Path('.').rglob('__pycache__')]"
```

### Testar sistema básico:
```bash
python principal.py
```

---

*Este guia é atualizado regularmente. Mantenha uma cópia local para consulta.*