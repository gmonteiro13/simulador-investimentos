import pandas as pd
import yfinance as yf
from typing import List


def fetch_data(tickers: List[str],
               start_date: str,
               end_date: str) -> pd.DataFrame:
    """
    Busca os dados de preços de fechamento
    JÁ AJUSTADOS para uma lista de tickers.

    Esta função usa o parâmetro auto_adjust=True para que a coluna 'Close'
    já contenha os preços ajustados para dividendos e desdobramentos.

    Args:
        tickers (List[str]): Uma lista de tickers de ações.\
        Ex: ["PETR4.SA", "VALE3.SA"].
        start_date (str): A data de início no formato 'YYYY-MM-DD'.
        end_date (str): A data de fim no formato 'YYYY-MM-DD'.

    Returns:
        pd.DataFrame: Um DataFrame com as datas como índice e os preços de
                      fechamento ajustados de cada ticker nas colunas.
    """
    print(f"Buscando dados para {tickers} de {start_date} até {end_date}...")

    data = yf.download(
        tickers,
        start=start_date,
        end=end_date,
        auto_adjust=True,
        progress=False
    )

    if data.empty:
        print("""Nenhum dado encontrado
              para os tickers e o período especificado.""")
        return pd.DataFrame()

    if len(tickers) == 1:
        price_data = data[['Close']]
        price_data.columns = tickers
    else:
        price_data = data['Close']
    price_data = price_data.ffill().bfill()

    print("Busca de dados concluída.")
    return price_data
