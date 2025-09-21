# 🎓 Sistema de Predição de Evasão Estudantil

## 📋 **Visão Geral**

Sistema híbrido inteligente que combina **Machine Learning** com **Regras de Negócio** para identificar alunos em risco de evasão escolar. Desenvolvido especificamente para instituições de ensino técnico, oferece predições precisas e explicáveis.

### ✨ **Principais Características**
- 🤖 **Modelo XGBoost** treinado com dados históricos
- 📏 **Regras de Negócio** específicas do Grau Técnico
- 🔍 **Explicabilidade SHAP** para interpretação das predições
- 📊 **Relatórios Detalhados** em formato CSV
- ⚡ **Sistema de Urgência** para priorização de ações
- 🏗️ **Arquitetura Modular** e escalável

---

## 🚀 **GUIA DE INSTALAÇÃO E TESTE**

### 📦 **Pré-requisitos**

**Software Necessário:**
- ✅ **Python 3.8+** ([Download aqui](https://www.python.org/downloads/))
- ✅ **Git** (opcional, para clonar o repositório)
- ✅ **Editor de código** (VS Code recomendado)

**Verificar instalação:**
```bash
python --version
# Deve mostrar: Python 3.8+ 
```

### �️ **Passo 1: Obter o Código**

**Opção A - Clonar com Git:**
```bash
git clone https://github.com/LucaScripts/SISTEMA_PREDI--O_EVASAO-TCC2.git
cd SISTEMA_PREDI--O_EVASAO-TCC2/SISTEMA_PREDIÇÃO_EVASAO
```

**Opção B - Download ZIP:**
1. Baixe o ZIP do repositório
2. Extraia para uma pasta
3. Navegue até `SISTEMA_PREDIÇÃO_EVASAO`

### ⚙️ **Passo 2: Configurar Ambiente**

**1. Criar ambiente virtual:**
```bash
python -m venv .venv
```

**2. Ativar ambiente virtual:**

**Windows (PowerShell):**
```powershell
.venv\Scripts\Activate.ps1
```

**Windows (CMD):**
```cmd
.venv\Scripts\activate.bat
```

**Linux/Mac:**
```bash
source .venv/bin/activate
```

**3. Instalar dependências:**
```bash
pip install -r requirements.txt
```

**📋 O arquivo `requirements.txt` inclui:**
- `pandas>=1.5.0` - Manipulação de dados
- `scikit-learn>=1.1.0` - Algoritmos de ML
- `xgboost>=1.6.0` - Modelo principal
- `shap>=0.41.0` - Explicabilidade
- `matplotlib>=3.5.0` - Visualizações
- `openpyxl>=3.0.0` - Leitura de Excel
- `joblib>=1.1.0` - Persistência de modelos
- E outras dependências essenciais...

### 🧪 **Passo 3: EXECUTAR TESTES**

#### **🎯 Teste Rápido (30 segundos)**

Execute o script de teste automático:
```bash
python test_sistema.py
```

**Resultado esperado:**
```
🧪 INICIANDO TESTES COMPLETOS DO SISTEMA
==================================================
🧪 Testando importações...
✅ Todas as importações funcionaram!

📁 Verificando arquivos...
✅ data/raw/alunos_ativos_atual.xlsx
✅ data/models/modelo_xgboost_sem_classes_criticas.pkl
✅ data/models/class_mapping_otimizado.pkl
✅ data/models/training_artifacts.pkl

🚀 Testando inicialização do sistema...
✅ Sistema inicializado com sucesso!

🎯 Testando predições...
✅ Predições realizadas com sucesso!
   Total de alunos: 954
   Matriculados: 837 (87.7%)
   Em risco: 117 (12.3%)
   Distribuição por urgência:
     ALTA: 88 alunos
     URGENTE: 18 alunos
     MEDIA: 6 alunos
     BAIXA: 5 alunos

🎉 TODOS OS TESTES CONCLUÍDOS COM SUCESSO!
```

#### **🔧 Teste Manual Completo**

**1. Verificar importações:**
```bash
python -c "
import sys, os
sys.path.insert(0, os.getcwd())
from codigo_fonte.configuracao import configuracoes
from codigo_fonte.nucleo import SistemaPredicaoEvasao
print('✅ Importações OK')
print(f'Modelos em: {configuracoes.dados.diretorio_modelos}')
"
```

**2. Executar sistema principal:**
```bash
python principal.py
```

**3. Executar com modo verboso:**
```bash
python principal.py --verboso
```

**4. Verificar arquivo de saída:**
```bash
python -c "
import pandas as pd
df = pd.read_csv('output/analise_completa.csv')
print(f'📊 Resultados: {len(df)} alunos processados')
print(f'Arquivo gerado: output/analise_completa.csv')
"
```

### 📊 **Resultados Esperados**

**Performance do Sistema:**
- ✅ **~954 alunos** analisados
- ✅ **~837 matriculados** (87.7%)
- ✅ **~117 em risco** (12.3%)
- ✅ **~18 casos urgentes** identificados
- ✅ **930 regras** de negócio aplicadas

**Arquivos Gerados:**
- 📄 `output/analise_completa.csv` - Predições detalhadas
- 📊 `output/confusion_matrix.png` - Matrix de confusão
- 📈 `output/feature_importance.png` - Importância das variáveis
- 📝 `output/model_training_report.txt` - Relatório de treinamento

---

## 📁 **Estrutura do Projeto**

```
SISTEMA_PREDIÇÃO_EVASAO/
├── 📁 codigo_fonte/              # Código fonte principal
│   ├── 📁 configuracao/          # Configurações do sistema
│   ├── 📁 modelos/              # Modelos de Machine Learning
│   ├── 📁 nucleo/               # Lógica principal do preditor
│   ├── 📁 regras_negocio/       # Regras de negócio específicas
│   └── 📁 utilitarios/          # Utilitários (logs, dados)
├── 📁 data/                     # Dados e modelos
│   ├── 📁 raw/                  # Dados brutos (Excel)
│   ├── 📁 models/               # Modelos treinados (.pkl)
│   └── 📁 processed/            # Dados processados
├── 📁 output/                   # Resultados das análises
├── 📁 scripts/                  # Scripts de treinamento
├── 🐍 principal.py              # Script principal
├── 🧪 test_sistema.py           # Testes automatizados
├── ⚡ quick_test.bat            # Teste rápido (Windows)
└── 📋 requirements.txt          # Dependências Python
```

---

## 🎯 **Como Usar o Sistema**

### **1. Predição Básica**
```bash
# Usar arquivo padrão
python principal.py

# Com arquivo específico
python principal.py data/raw/meus_alunos.xlsx

# Modo detalhado
python principal.py --verboso
```

### **2. Interpretar Resultados**

O arquivo `output/analise_completa.csv` contém:

| Coluna | Descrição |
|--------|-----------|
| `Nome` | Nome do aluno |
| `Status_Predicao` | MATRICULADO ou RISCO_EVASAO |
| `Nivel_Urgencia` | URGENTE, ALTA, MEDIA, BAIXA |
| `Situacao_Predita` | Situação específica predita |
| `Probabilidade_Situacao` | Confiança da predição (%) |
| `Fonte_Predicao` | ML ou Regra aplicada |
| `Fator_Principal` | Principal variável de risco |

### **3. Casos Prioritários**

Focar nos alunos com:
- ⚠️ `Nivel_Urgencia` = "URGENTE" (ação imediata)
- 🔴 `Nivel_Urgencia` = "ALTA" (ação em 1-2 semanas)

---

## 🐛 **Resolução de Problemas**

### **❌ Erro: "ModuleNotFoundError"**
```bash
# Verificar se ambiente virtual está ativo
# Reinstalar dependências do requirements.txt
pip install -r requirements.txt

# Ou instalar com upgrade
pip install -r requirements.txt --upgrade
```

### **❌ Erro: "File not found"**
```bash
# Verificar se arquivos estão nas pastas corretas
python -c "
from pathlib import Path
print('Arquivos encontrados:')
for f in Path('data/raw').glob('*.xlsx'):
    print(f'  {f}')
"
```

### **❌ Erro: "Permission denied"**
```bash
# Verificar permissões da pasta
# Executar como administrador se necessário
```

### **⚠️ Warnings de versão**
```bash
# Re-treinar modelos com versões atuais
python -c "
# Script de re-treinamento rápido já incluído no sistema
print('Execute: python test_sistema.py para verificar')
"
```

---

## � **Suporte e Informações**

### **📊 Dados de Entrada Necessários**

O sistema espera uma planilha Excel com as colunas:
- `Nome` - Nome do aluno
- `Matrícula` - Código único do aluno  
- `Pend. Financ.` - Pendências financeiras
- `Faltas Consecutivas` - Número de faltas seguidas
- `Pend. Acad.` - Pendências acadêmicas
- `Curso` - Nome do curso
- `Sexo` - Gênero do aluno
- `Turma Atual` - Turma atual
- E outras variáveis disponíveis...

### **🔧 Configurações Avançadas**

Edite `codigo_fonte/configuracao/configuracoes.py` para ajustar:
- Parâmetros do modelo XGBoost
- Thresholds das regras de negócio
- Caminhos dos arquivos
- Configurações de logging

### **📈 Performance do Sistema**

- ⚡ **Tempo de processão:** ~2-3 segundos para 1000 alunos
- 🎯 **Acurácia:** ~73% no conjunto de teste
- 📊 **Precisão:** Otimizada para minimizar falsos negativos
- 🔄 **Compatibilidade:** Python 3.8+ em Windows/Linux/Mac

---

## 🤝 **Contribuição e Desenvolvimento**

Este é um sistema educacional desenvolvido como TCC. Para sugestões ou melhorias:

1. Fork o repositório
2. Crie uma branch para sua feature
3. Faça commit das mudanças
4. Abra um Pull Request

---

## 📄 **Licença**

Sistema desenvolvido para fins educacionais - TCC 2025.

---

**🎯 Pronto para usar! Execute `python test_sistema.py` para começar!**


