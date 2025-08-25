import pandas as pd
import numpy as np
from typing import List


def _normalize_weights(weights: List[float]) -> np.ndarray:
    """Normaliza uma lista de pesos para que a soma seja 1."""
    weights = np.array(weights)
    return weights / np.sum(weights)


def simulate_portfolio(
    price_data: pd.DataFrame,
    initial_capital: float,
    monthly_contribution: float,
    weights: List[float]
) -> pd.Series:
    """
    Simula a evolução de uma carteira de ações com aportes mensais.

    Args:
        price_data (pd.DataFrame): DataFrame com os\
            preços históricos dos ativos.
        capital_inicial (float): O valor inicial do investimento.
        aporte_mensal (float): O valor aportado no início de cada mês.
        weights (List[float]): Lista com os pesos de cada ativo na carteira.

    Returns:
        pd.Series: Uma série com o valor do portfólio\
            para cada dia na simulação.
    """

    weights = _normalize_weights(weights)

    daily_returns = price_data.pct_change()

    dates = daily_returns.index
    portfolio_values = pd.Series(0.0, index=dates)
    portfolio_values.iloc[0] = initial_capital

    for i in range(1, len(dates)):
        previous_date = dates[i - 1]
        current_date = dates[i]

        previous_value = portfolio_values.iloc[i - 1]

        returns_on_current_day = daily_returns.iloc[i]
        retorno_carteira_dia = np.dot(returns_on_current_day, weights)

        current_value = previous_value * (1 + retorno_carteira_dia)

        if current_date.month != previous_date.month:
            current_value += monthly_contribution

        portfolio_values.iloc[i] = current_value

    portfolio_values.name = "Carteira de Ações"
    return portfolio_values
