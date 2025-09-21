# 🎓 Manual de Uso - Sistema de Predição de Evasão

## 📋 **GUIA RÁPIDO PARA USUÁRIOS**

### 🚀 **Método 1: Interface Web (Mais Fácil)**

#### **Passo a Passo:**

1. **Abrir o Sistema**
   - Dê duplo clique no arquivo `iniciar_interface_web.bat`
   - Uma página web irá abrir no seu navegador
   
2. **Fazer Upload da Planilha**
   - Clique em "Browse files" 
   - Selecione sua planilha Excel (.xlsx)
   - Aguarde o preview aparecer
   
3. **Processar**
   - Clique no botão "🚀 Processar Predições"
   - Aguarde a barra de progresso completar
   
4. **Download do Resultado**
   - Clique em "📥 Download CSV para Power BI"
   - Salve o arquivo em seu computador

5. **Importar no Power BI**
   - Abra o Power BI
   - Vá em "Obter Dados" → "Arquivo de Texto/CSV"
   - Selecione o arquivo baixado

---

### 📁 **Método 2: Sistema de Pastas (Automático)**

#### **Passo a Passo:**

1. **Preparar Arquivo**
   - Coloque sua planilha Excel na pasta `📁 input`
   - Certifique-se que é um arquivo .xlsx
   
2. **Executar Sistema**
   - Dê duplo clique em `executar_predicao.bat`
   - Aguarde o processamento (aparecerá na tela)
   
3. **Pegar Resultado**
   - O sistema abrirá automaticamente a pasta `📁 output`
   - Pegue o arquivo CSV mais recente
   
4. **Usar no Power BI**
   - Importe o CSV no Power BI normalmente

---

## 📊 **Como Interpretar os Resultados**

### **Colunas Principais:**

| Coluna | O que significa |
|--------|-----------------|
| `Status_Predicao` | **MATRICULADO** (seguro) ou **RISCO_EVASAO** (atenção) |
| `Nivel_Urgencia` | **URGENTE** (ação imediata) → **ALTA** → **MEDIA** → **BAIXA** |
| `Situacao_Predita` | Situação específica prevista (LFI, LAC, MT, etc.) |
| `Probabilidade_Situacao` | Confiança da predição (%) |
| `Fator_Principal` | Principal causa do risco (Financeiro, Acadêmico, etc.) |

### **Prioridades de Ação:**

1. 🚨 **URGENTE**: Ação imediata necessária
2. 🔴 **ALTA**: Ação em 1-2 semanas  
3. 🟡 **MEDIA**: Monitorar de perto
4. 🟢 **BAIXA**: Acompanhamento normal

---

## ⚠️ **Problemas Comuns e Soluções**

### **"Arquivo não encontrado"**
- ✅ Verifique se colocou o Excel na pasta `input`
- ✅ Certifique-se que é arquivo .xlsx (não .xls)

### **"Erro ao processar"**
- ✅ Verifique se sua planilha tem as colunas básicas:
  - Nome, Matrícula, Curso, Sexo
- ✅ Certifique-se que não há caracteres especiais nos nomes das colunas

### **"Sistema não inicia"**
- ✅ Execute como administrador
- ✅ Verifique se o antivírus não está bloqueando

### **"CSV com caracteres estranhos no Power BI"**
- ✅ No Power BI, ao importar, escolha encoding "UTF-8"

---

## 📞 **Suporte**

**Dúvidas ou Problemas?**
- Anote a mensagem de erro exata
- Informe qual arquivo estava processando
- Entre em contato com a TI

---

## 🔄 **Fluxo Recomendado para Produção**

```
📊 Dados dos Alunos (Excel)
           ↓
🤖 Sistema de Predição 
           ↓  
📄 Arquivo CSV
           ↓
📈 Dashboard Power BI
           ↓
👥 Coordenadores/Gestores
```

### **Frequência Sugerida:**
- **Semanal**: Para acompanhamento regular
- **Mensal**: Para relatórios gerenciais  
- **Sob demanda**: Para situações específicas

---

**💡 Dica:** Mantenha sempre backup de suas planilhas originais!

---

## 🚨 Solução de Problemas

Se encontrar algum problema durante o uso:

### 📋 Primeiros Passos:
1. **Consulte o Guia Completo:** `RESOLUCAO_PROBLEMAS.md`
2. **Verifique os logs:** `sistema_predicao_evasao.log`
3. **Anote a mensagem de erro** exata que aparecer
4. **Tente novamente:** Muitos problemas são temporários

### 🔧 Problemas Mais Comuns:

**Excel não reconhecido:**
- Salve o arquivo como `.xlsx` no Excel
- Feche o arquivo no Excel antes do upload
- Evite caracteres especiais no nome

**Interface web não carrega:**
- Aguarde alguns segundos para inicialização
- Recarregue a página (F5)
- Tente outro navegador

**Processamento muito lento:**
- Arquivos grandes (>5000 linhas) podem demorar
- Feche outros programas para liberar memória
- Seja paciente - pode levar alguns minutos

**Dashboard Power BI não aparece:**
- Verifique sua conexão com internet
- Desabilite bloqueadores de popup/anúncio
- Permita iframes no navegador

### 📞 Suporte Técnico:
- 📄 **Guia Completo:** `RESOLUCAO_PROBLEMAS.md`
- 📝 **Logs do Sistema:** `sistema_predicao_evasao.log`
- 💻 **Documentação Técnica:** Consulte o repositório

---

**✅ Sistema pronto para uso em produção!**