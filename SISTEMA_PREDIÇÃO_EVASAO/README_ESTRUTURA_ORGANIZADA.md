# Sistema de Predição de Evasão Estudantil - Estrutura Organizada

## 📁 Estrutura do Projeto

```
SISTEMA_PREDIÇÃO_EVASAO/
├── 🚀 INICIAR_SISTEMA.bat          # Script principal para iniciar o sistema
├── 🐍 principal.py                 # Arquivo principal do sistema
├── 🌐 interface_web_limpa.py       # Interface web Streamlit (versão limpa)
├── 🌐 interface_web.py             # Interface web Streamlit (versão completa)
├── ⚙️ automacao_powerbi.py          # Automação do Power BI
├── 📚 tutorial_acadweb.py          # Tutorial do AcadWeb
├── 🔧 processar_producao.py        # Processamento de produção
├── 
├── 📂 codigo_fonte/                # Código-fonte principal
│   ├── configuracao/               # Configurações do sistema
│   ├── modelos/                    # Modelos de Machine Learning
│   ├── nucleo/                     # Núcleo do sistema de predição
│   ├── regras_negocio/            # Regras de negócio
│   └── utilitarios/               # Utilitários diversos
├── 
├── 📂 data/                        # Dados do projeto
│   ├── models/                     # Modelos treinados
│   ├── processed/                  # Dados processados
│   └── raw/                       # Dados brutos
├── 
├── 📂 input/                       # Arquivos de entrada
├── 📂 output/                      # Arquivos de saída
├── 📂 scripts/                     # Scripts auxiliares
├── 
├── 📂 docs/                        # Documentação
│   ├── MANUAL_USUARIO.md          # Manual do usuário
│   ├── PERFORMANCE_REPORT.md      # Relatório de performance
│   ├── RESOLUCAO_PROBLEMAS.md     # Guia de resolução de problemas
│   └── outros arquivos .md/.txt
├── 
├── 📂 executores/                  # Scripts de execução (.bat/.ps1)
├── 📂 logs/                        # Arquivos de log
├── 📂 teste_powerbi/              # Testes específicos do Power BI
└── 📂 arquivos_obsoletos/         # Arquivos antigos/obsoletos organizados
    ├── testes_antigos/            # Arquivos teste_*.py
    ├── debug_antigos/             # Arquivos debug_*.py
    └── scripts_antigos/           # Scripts batch/PowerShell antigos
```

## 🚀 Como Usar

### Iniciar o Sistema (Recomendado)
```bash
INICIAR_SISTEMA.bat
```

### Executar Manualmente
```bash
python -m streamlit run interface_web_limpa.py --server.port=8501
```

### Executar Predição via Linha de Comando
```bash
python principal.py arquivo_alunos.xlsx
```

## 📋 Arquivos Principais

| Arquivo | Descrição |
|---------|-----------|
| `INICIAR_SISTEMA.bat` | Script principal para iniciar o sistema |
| `principal.py` | Sistema de linha de comando |
| `interface_web_limpa.py` | Interface web simplificada (recomendada) |
| `interface_web.py` | Interface web completa |
| `automacao_powerbi.py` | Integração com Power BI |

## 🗂️ Organização Implementada

### ✅ Arquivos Movidos para `arquivos_obsoletos/`
- Todos os arquivos `teste_*.py` (13+ arquivos)
- Todos os arquivos `debug_*.py` (4 arquivos)
- Scripts batch duplicados/antigos
- Arquivos de configuração específicos
- Arquivos temporários e de backup

### ✅ Estrutura Limpa
- **Documentação**: Pasta `docs/`
- **Scripts**: Pasta `executores/`
- **Logs**: Pasta `logs/`
- **Código Principal**: Mantido na raiz para fácil acesso

## 🎯 Benefícios da Organização

1. **Clareza**: Fácil identificação dos arquivos principais
2. **Manutenibilidade**: Código-fonte organizado em módulos
3. **Documentação**: Centralizada na pasta `docs/`
4. **Histórico**: Arquivos antigos preservados em `arquivos_obsoletos/`
5. **Execução**: Script único `INICIAR_SISTEMA.bat` para iniciar

## 📞 Suporte

Consulte os arquivos na pasta `docs/` para:
- Manual do usuário
- Guia de resolução de problemas
- Relatórios de performance
- Documentação técnica

---

**Sistema de Predição de Evasão Estudantil v2.0 - Estrutura Organizada**  
*Desenvolvido para Grau Técnico - 2025*