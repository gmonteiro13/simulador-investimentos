# Simulador de Investimentos em Python

[![Python CI Pipeline](https://github.com/gmonteiro13/simulador-investimentos/actions/workflows/ci_pipeline.yml/badge.svg)](https://github.com/gmonteiro13/simulador-investimentos/actions)

Simulador em Python que compara a evolução de capital em juros compostos vs. uma carteira de ações com aportes mensais. Análise com dados do Yahoo Finance, incluindo métricas como CAGR, volatilidade e drawdown.

## 📊 Visão Geral

Este projeto é uma ferramenta de linha de comando (CLI) para análise e simulação de estratégias de investimento. Ele compara dois cenários principais: um investimento de baixo risco com rendimento fixo (juros compostos) e um investimento de maior risco em uma carteira de ações diversificada.

A ferramenta busca dados históricos reais do mercado através da biblioteca `yfinance` e gera relatórios comparativos, incluindo gráficos e uma tabela de métricas financeiras.

## ✨ Principais Funcionalidades

- **Simulação de Juros Compostos:** Calcula o crescimento de um capital com aportes mensais a uma taxa fixa.
- **Simulação de Carteira de Ações:** Simula o desempenho de uma carteira com ativos e pesos definidos pelo usuário.
- **Dados Históricos:** Busca preços de fechamento ajustados de qualquer ativo listado no Yahoo Finance.
- **Cálculo de Métricas:** Analisa as simulações e calcula métricas essenciais como Valor Final, CAGR, Volatilidade Anualizada, Máximo Drawdown e Índice de Sharpe.
- **Relatórios Visuais:** Gera gráficos comparativos e de drawdown, salvando-os como arquivos de imagem.
- **Testes Automatizados:** A lógica principal do projeto é validada por testes unitários usando `pytest`.
- **Integração Contínua:** Utiliza GitHub Actions para rodar os testes automaticamente a cada push, garantindo a qualidade do código.

## 🛠️ Tecnologias Utilizadas

- **Python 3.9+**
- **Pandas:** Para manipulação e análise de dados.
- **NumPy:** Para cálculos numéricos eficientes.
- **yfinance:** Para a obtenção de dados do mercado financeiro.
- **Matplotlib:** Para a geração dos gráficos.
- **Pytest:** Para a automação dos testes.
- **GitHub Actions:** Para o pipeline de CI (Integração Contínua).

## 📂 Estrutura do Projeto

```
├── .github/workflows/ci_pipeline.yml
├── main.py
├── modules/
│   ├── data.py
│   ├── interest.py
│   ├── portfolio.py
│   ├── metrics.py
│   └── report.py
├── tests/
│   └── test_core.py
├── requirements.txt
└── README.md
```

## 🚀 Instalação e Configuração

Siga os passos abaixo para executar o projeto localmente.

**1. Clone o repositório:**
```bash
git clone [https://github.com/gmonteiro13/simulador-investimentos.git](https://github.com/gmonteiro13/simulador-investimentos.git)
cd simulador-investimentos
```

**2. Crie e ative um ambiente virtual:**
```bash
# Criar o ambiente
python -m venv venv

# Ativar no macOS/Linux
source venv/bin/activate

# Ativar no Windows
.\venv\Scripts\activate
```

**3. Instale as dependências:**
```bash
pip install -r requirements.txt
```

## ⚙️ Como Usar

O script principal (`main.py`) é executado via terminal e aceita diversos parâmetros para personalizar a simulação.

**Exemplo de comando:**
```bash
python main.py \
  --tickers "PETR4.SA,VALE3.SA,ITUB4.SA" \
  --start 2020-01-01 \
  --end 2024-12-31 \
  --weights "0.4,0.3,0.3" \
  --aporte_mensal 1000 \
  --capital_inicial 50000 \
  --taxa_juros_mensal 0.8
```

### Parâmetros

- `--tickers`: Lista de ativos (separados por vírgula) conforme o Yahoo Finance.
- `--start`: Data de início da simulação (`YYYY-MM-DD`).
- `--end`: Data de fim da simulação (`YYYY-MM-DD`).
- `--weights`: Pesos de cada ativo na carteira (separados por vírgula).
- `--aporte_mensal`: Valor do aporte mensal em R$.
- `--capital_inicial`: Valor do capital inicial em R$.
- `--taxa_juros_mensal`: Taxa de juros mensal para o cenário de renda fixa (em %).

## 📊 Saídas Esperadas

Após a execução, o programa irá:
1.  Imprimir uma tabela comparativa de métricas no console.
2.  Salvar dois gráficos na pasta do projeto:
    - `comparativo_evolucao.png`: Gráfico comparando a evolução dos dois cenários.
    - `drawdown_carteira.png`: Gráfico mostrando o drawdown da carteira de ações.

## ✅ Testes

Para garantir a qualidade e o correto funcionamento da lógica de cálculos, execute a suíte de testes automatizados:

```bash
pytest
```

## 👨‍💻 Autor

- **Gabriel Monteiro** - [gmonteiro13](https://github.com/gmonteiro13)