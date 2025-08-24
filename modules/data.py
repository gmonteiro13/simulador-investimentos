import pandas as pd
import yfinance as yf

def fetch_data(tickers, start_date, end_date):

    data = yf.download(
        tickers, start=start_date, end=end_date, progress=False
    )
    
    if len(tickers) == 1:
        price_data = data[['Close']]
        price_data.columns = tickers # renomear a coluna para o nome do ticker
    else:
        price_data = data[['Close']]
        
    price_data = price_data.ffill().bfill() # trata dados ausentes
    return price_data

if __name__ == "__main__":
    # testes com mais de 1 ticker
    tickers = ["PETR4.SA", "VALE3.SA", "ITUB4.SA"]
    start_date = "2020-01-01"
    end_date = "2020-12-31"
    data_multi_tickers = fetch_data(tickers, start_date, end_date)
    print(data_multi_tickers.head())

    # teste com apenas 1 ticker
    tickers = ["PETR4.SA"]
    data_single_ticker = fetch_data(tickers, start_date, end_date)
    print(data_single_ticker.head())