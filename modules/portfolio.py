import pandas as pd
import numpy as np

def simulate_portfolio(
    price_data,
    initial_capital,
    monthly_contribution,
    weights
):
    # Normalização dos pesos
    weights = np.array(weights)
    weights = weights / np.sum(weights)
    
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
