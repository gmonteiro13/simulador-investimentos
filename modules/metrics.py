import pandas as pd
import numpy as np


def calculate_cagr(series: pd.Series) -> float:
    """Calcula a Taxa de Crescimento Anual Composta (CAGR)."""
    start_value = series.iloc[0]
    end_value = series.iloc[-1]
    num_days = (series.index[-1] - series.index[0]).days
    num_years = num_days / 365.25

    if num_years == 0:
        return 0.0

    cagr = (end_value / start_value) ** (1 / num_years) - 1
    return cagr


def calculate_annualized_volatility(series: pd.Series) -> float:
    """Calcula a volatilidade anualizada dos retornos diários."""
    daily_returns = series.pct_change().dropna()
    # número aprox. de dias de negociação
    volatility = daily_returns.std() * np.sqrt(252)
    return volatility


def calculate_max_drawdown(series: pd.Series) -> float:
    """Calcula o Máximo Drawdown."""
    running_max = series.cummax()
    drawdown = (series - running_max) / running_max
    max_drawdown = drawdown.min()
    return max_drawdown


def calculate_sharpe_ratio(series: pd.Series,
                           risk_free_rate: float = 0.0) -> float:
    """Calcula o Índice de Sharpe simplificado."""
    volatility = calculate_annualized_volatility(series)

    annualized_return = calculate_cagr(series)

    if volatility == 0:
        return np.inf  # caso retorno não tenha risco

    sharpe = (annualized_return - risk_free_rate) / volatility
    return sharpe


def calculate_all_metrics(series: pd.Series,
                          risk_free_cagr: float = 0.0) -> dict:
    """Calcula todas as métricas para uma dada série de valores\
        e retorna um dicionário."""

    # Para o cenário de juros, as métricas de risco são zero
    is_risk_free = series.pct_change().std() == 0

    if is_risk_free:
        volatility = 0.0
        max_drawdown = 0.0
        sharpe = np.inf
    else:
        volatility = calculate_annualized_volatility(series)
        max_drawdown = calculate_max_drawdown(series)
        sharpe = calculate_sharpe_ratio(series, risk_free_cagr)

    metrics = {
        "Valor Final (R$)": series.iloc[-1],
        "CAGR (%)": calculate_cagr(series) * 100,
        "Volatilidade Anual. (%)": volatility * 100,
        "Max. Drawdown (%)": max_drawdown * 100,
        "Índice de Sharpe": sharpe
    }
    return metrics
