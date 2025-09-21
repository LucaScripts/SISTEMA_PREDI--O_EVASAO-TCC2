# Sistema de Predição de Evasão Estudantil

## 🎯 **Visão Geral**

Este projeto implementa um sistema híbrido para predição de evasão estudantil, combinando a precisão de um modelo de Machine Learning (XGBoost) com a transparência e conformidade de regras de negócio específicas da instituição.

O sistema analisa dados de alunos ativos para identificar aqueles com maior risco de evasão, permitindo ações proativas de retenção.

## ✨ **Principais Funcionalidades**

- **Sistema Híbrido:** Combina Machine Learning com regras de negócio para predições mais precisas e explicáveis.
- **Modelo XGBoost:** Utiliza um modelo Gradient Boosting para identificar padrões complexos nos dados históricos.
- **Regras de Negócio Configuráveis:** Implementa regras específicas do Grau Técnico para classificação de alunos (LFI, LFR, NC, LAC, NF, MT).
- **Análise SHAP:** Fornece explicabilidade para as predições do modelo de ML, identificando os principais fatores de risco.
- **Estrutura Modular:** Código organizado, limpo e fácil de manter, seguindo as melhores práticas de desenvolvimento.
- **Logging e Configuração:** Sistema de logging estruturado e configurações centralizadas para fácil ajuste.
- **Relatórios Detalhados:** Gera relatórios completos em formato CSV com todas as informações da predição.

## 📊 **Resultados**

Em testes com 954 alunos, o sistema híbrido demonstrou resultados realistas e alinhados com as expectativas da instituição:

- **89.1% Matriculados** (850 alunos)
- **10.9% em Risco de Evasão** (104 alunos)
- **96.9% das decisões** baseadas em regras de negócio, garantindo transparência.

## 🚀 **Como Usar**

### **1. Pré-requisitos**

- Python 3.8+
- Pip (gerenciador de pacotes)

### **2. Instalação**

Clone o repositório e instale as dependências:

```bash
git clone https://github.com/seu-usuario/student-dropout-prediction.git
cd student-dropout-prediction
pip install -r requirements.txt
```

### **3. Estrutura de Dados**

Coloque os arquivos de dados na pasta `data/raw/`:

- `alunos_ativos_atual.xlsx`: Planilha com dados dos alunos ativos.
- `Planilhabasedados.xlsx`: Base de dados para treinamento do modelo.
- `disciplinas.xlsx`: Grade curricular das disciplinas.
- `cursos.xlsx`: Informações dos cursos.

### **4. Executando a Predição**

Para fazer predições para os alunos ativos, execute o script principal:

```bash
python main.py
```

O resultado será salvo em `output/analise_completa.csv`.

### **5. Treinando o Modelo**

Para retreinar o modelo com novos dados, execute o script de treinamento:

```bash
python scripts/train_model.py
```

Os novos arquivos de modelo serão salvos em `data/models/`.

## 🏗️ **Estrutura do Projeto**

```
student-dropout-prediction/
├── data/                    # Dados brutos, processados e modelos
│   ├── raw/
│   ├── processed/
│   └── models/
├── docs/                    # Documentação do projeto
├── notebooks/               # Jupyter notebooks para análise exploratória
├── scripts/                 # Scripts para treinamento, predição, etc.
├── src/                     # Código fonte do projeto
│   ├── business_rules/      # Módulo de regras de negócio
│   ├── config/            # Configurações do sistema
│   ├── core/              # Lógica principal do preditor
│   ├── models/            # Modelo de machine learning
│   └── utils/             # Utilitários (logger, data loader)
├── tests/                   # Testes unitários e de integração
├── main.py                  # Ponto de entrada principal
├── requirements.txt         # Dependências do projeto
└── README.md                # Documentação principal
```

## 🔧 **Configurações**

As principais configurações do sistema podem ser ajustadas no arquivo `src/config/settings.py`:

- **Parâmetros do modelo:** `ModelConfig`
- **Regras de negócio:** `BusinessRulesConfig`
- **Caminhos de dados:** `DataConfig`
- **Configurações de logging:** `LoggingConfig`

## 🤝 **Contribuições**

Contribuições são bem-vindas! Sinta-se à vontade para abrir uma issue ou enviar um pull request.

## 📄 **Licença**

Este projeto está licenciado sob a licença MIT. Veja o arquivo `LICENSE` para mais detalhes.


