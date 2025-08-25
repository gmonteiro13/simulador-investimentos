import pandas as pd


def simulate_compound_interest(
    capital_inicial: float,
    aporte_mensal: float,
    taxa_juros_mensal: float,
    dates: pd.DatetimeIndex
) -> pd.Series:
    """
    Simula a evolução de um capital com juros compostos e aportes mensais.

    Args:
        capital_inicial (float):\
            O valor inicial do investimento.
        aporte_mensal (float):\
            O valor aportado no início de cada mês.
        taxa_juros_mensal (float):\
            A taxa de juros mensal em porcentagem (ex: 0.8 para 0.8%).
        dates (pd.DatetimeIndex):\
            O índice de datas para a simulação.

    Returns:
        pd.Series: Uma série com o valor do patrimônio \
            para cada dia na simulação.
    """
    taxa_mensal_decimal = taxa_juros_mensal / 100.0
    results = pd.Series(0.0, index=dates)
    results.iloc[0] = capital_inicial

    for i in range(1, len(dates)):
        data_anterior = dates[i-1]
        data_atual = dates[i]

        valor_base = results.iloc[i-1]

        if data_atual.month != data_anterior.month:
            valor_base += aporte_mensal

        dias_no_mes = data_anterior.days_in_month
        taxa_diaria = (1 + taxa_mensal_decimal)**(1/dias_no_mes) - 1
        valor_atual = valor_base * (1 + taxa_diaria)

        results.iloc[i] = valor_atual

    results.name = "Juros Compostos"
    return results
