import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
from typing import Dict


def generate_comparison_plot(
    interest_series: pd.Series,
    portfolio_series: pd.Series
):
    """
    Gera e salva um gráfico comparando a evolução das duas simulações.
    """
    print("Gerando gráfico de comparação...")
    plt.style.use('seaborn-v0_8-darkgrid')
    fig, ax = plt.subplots(figsize=(12, 7))

    ax.plot(interest_series.index,
            interest_series,
            label=interest_series.name,
            color='royalblue',
            linewidth=2)
    ax.plot(portfolio_series.index,
            portfolio_series,
            label=portfolio_series.name,
            color='darkorange',
            linewidth=2)

    # Formatando o eixo Y para parecer com moeda
    formatter = mticker.FuncFormatter(lambda x,
                                      _: f'R$ {x:,.0f}'
                                      .replace(',', '.'))
    ax.yaxis.set_major_formatter(formatter)

    ax.set_title('Juros Compostos vs. Carteira de Ações', fontsize=16)
    ax.set_xlabel('Data', fontsize=12)
    ax.set_ylabel('Patrimônio (R$)', fontsize=12)
    ax.legend(fontsize=12)

    plt.tight_layout()
    plt.savefig('comparativo_evolucao.png')
    print("Gráfico 'comparativo_evolucao.png' salvo.")
    plt.close(fig)  # Fecha a figura para liberar memória


def generate_drawdown_plot(portfolio_series: pd.Series):
    """
    Gera e salva um gráfico mostrando o drawdown da carteira ao longo do tempo.
    """
    print("Gerando gráfico de drawdown...")
    running_max = portfolio_series.cummax()
    drawdown = (portfolio_series - running_max) / running_max

    plt.style.use('seaborn-v0_8-darkgrid')
    fig, ax = plt.subplots(figsize=(12, 7))

    ax.plot(drawdown.index, drawdown, color='red', linewidth=1)
    ax.fill_between(drawdown.index, drawdown, 0, color='red', alpha=0.3)

    # Formatando o eixo Y para porcentagem
    formatter = mticker.FuncFormatter(lambda x, _: f'{x:.1%}')
    ax.yaxis.set_major_formatter(formatter)

    ax.set_title('Drawdown da Carteira de Ações', fontsize=16)
    ax.set_xlabel('Data', fontsize=12)
    ax.set_ylabel('Queda do Pico (%)', fontsize=12)

    plt.tight_layout()
    plt.savefig('drawdown_carteira.png')
    print("Gráfico 'drawdown_carteira.png' salvo.")
    plt.close(fig)


def generate_report_table(
    interest_metrics: Dict,
    portfolio_metrics: Dict
):
    """
    Cria e imprime uma tabela comparativa das métricas no console.
    """
    print("\n" + "="*50)
    print("RELATÓRIO DE MÉTRICAS COMPARATIVAS")
    print("="*50)

    # Adicionando nomes aos dicionários para usar como índice
    interest_metrics['Cenário'] = 'Juros Compostos'
    portfolio_metrics['Cenário'] = 'Carteira de Ações'

    df = pd.DataFrame([interest_metrics, portfolio_metrics])
    df = df.set_index('Cenário')

    # Formatando os valores para melhor visualização
    df['Valor Final (R$)'] = df['Valor Final (R$)'].map('R$ {:,.2f}'.format)
    df['CAGR (%)'] = df['CAGR (%)'].map('{:.2f}%'.format)
    df['Volatilidade Anual. (%)'] = df['Volatilidade Anual. (%)']\
        .map('{:.2f}%'.format)
    df['Max. Drawdown (%)'] = df['Max. Drawdown (%)'].map('{:.2f}%'.format)
    df['Índice de Sharpe'] = df['Índice de Sharpe'].map('{:.2f}'.format)

    print(df.to_string())
    print("="*50 + "\n")
