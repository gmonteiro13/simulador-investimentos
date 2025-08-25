import pandas as pd

def simulate_compound_interest(initial_capital,
                               monthly_contribution,
                               monthly_interest_rate,
                               price_data):
    
    # bdate retorna o número de dias úteis para um período de tempo
    start_date = price_data.min()
    end_date = price_data.max()

    # Gera uma série de datas úteis dentro do intervalo
    dates = pd.bdate_range(start=start_date, end=end_date)

    # Converte a taxa de juros mensal para decimal
    decimal_rate = monthly_interest_rate / 100.0
    
    # Cria a série inicial preenchida com zeros
    capital_series = pd.Series(0, index=dates)
    capital_series.iloc[0] = initial_capital

    # Simula o crescimento do investimento ao longo do tempo
    for i in range(1, len(dates)):
        data_anterior = dates[i-1]
        data_atual = dates[i]
        
        valor_anterior = capital_series.iloc[i-1]
        
        # Calcular os juros diários. Usamos a aproximação de (1+taxa)^(1/dias no mês).
        dias_no_mes = data_anterior.days_in_month
        taxa_diaria = (1 + decimal_rate)**(1/dias_no_mes) - 1

        # Calcula o valor atual com juros
        valor_atual = valor_anterior * (1 + taxa_diaria)
        
        # Verificar se é o início de um novo mês para adicionar o aporte
        # (consideramos o primeiro dia útil do mês na nossa série de datas)
        if data_atual.month != data_anterior.month:
            valor_atual += monthly_contribution

        capital_series.iloc[i] = valor_atual

    capital_series.name = "Juros Compostos"
    return capital_series

if __name__ == "__main__":
    # Exemplo de uso da função
    print("Iniciando simulação de juros compostos...")
    evolucao_patrimonio = simulate_compound_interest(
        initial_capital=10000,
        monthly_contribution=500,
        monthly_interest_rate=0.8,
        start_date="2020-01-01",
        end_date="2021-12-31"
    )

    print("\n--- Evolução do Patrimônio (5 primeiros dias) ---")
    print(evolucao_patrimonio.head())
    
    print("\n--- Evolução do Patrimônio (5 últimos dias) ---")
    print(evolucao_patrimonio.tail())
    
    # Um gráfico simples para visualizar o resultado
    try:
        import matplotlib.pyplot as plt
        print("\nGerando gráfico de visualização...")
        evolucao_patrimonio.plot(
            title="Evolução do Patrimônio - Juros Compostos",
            figsize=(10, 6)
        )
        plt.xlabel("Data")
        plt.ylabel("Patrimônio (R$)")
        plt.grid(True)
        
        # Salva a figura em um arquivo PNG na pasta principal do projeto
        plt.savefig("grafico_juros_compostos.png")
        print("Gráfico salvo como 'grafico_juros_compostos.png'")

    except ImportError:
        print("\nMatplotlib não instalado. Pule o gráfico de teste.")