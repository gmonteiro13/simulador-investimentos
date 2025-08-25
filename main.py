import argparse
import sys

sys.path.append('modules')

from data import fetch_data
from interest import simulate_compound_interest
from portfolio import simulate_portfolio
from metrics import calculate_all_metrics
from report import generate_comparison_plot, generate_drawdown_plot, generate_report_table

def main():
    """
    Função principal que orquestra a execução do script.
    """
    # --- 1. Configuração do Painel de Controle (Argument Parser) ---
    parser = argparse.ArgumentParser(description="Simulação de Juros Compostos vs. Carteira de Ações.")
    
    parser.add_argument('--tickers', type=str, required=True, help='Lista de tickers separados por vírgula. Ex: "PETR4.SA,VALE3.SA"')
    parser.add_argument('--start', type=str, required=True, help='Data de início no formato YYYY-MM-DD.')
    parser.add_argument('--end', type=str, required=True, help='Data de fim no formato YYYY-MM-DD.')
    parser.add_argument('--weights', type=str, required=True, help='Pesos da carteira separados por vírgula. Ex: "0.4,0.3,0.3"')
    parser.add_argument('--aporte_mensal', type=float, required=True, help='Aporte mensal em R$.')
    parser.add_argument('--capital_inicial', type=float, required=True, help='Capital inicial em R$.')
    parser.add_argument('--taxa_juros_mensal', type=float, required=True, help='Taxa de juros mensal (%). Ex: 0.8')
    
    args = parser.parse_args()

    # --- 2. Processando os Inputs ---
    tickers = [ticker.strip() for ticker in args.tickers.split(',')]
    weights = [float(weight.strip()) for weight in args.weights.split(',')]
    
    print("Iniciando a simulação com os seguintes parâmetros:")
    print(f" - Tickers: {tickers}")
    print(f" - Período: {args.start} a {args.end}")
    print(f" - Pesos: {weights}")
    print(f" - Capital Inicial: R$ {args.capital_inicial:,.2f}")
    print(f" - Aporte Mensal: R$ {args.aporte_mensal:,.2f}")
    print(f" - Taxa de Juros Mensal: {args.taxa_juros_mensal}%")
    print("-" * 50)

    # --- 3. A Orquestração ---
    # Passo 1: Buscar os dados
    price_data = fetch_data(tickers, args.start, args.end)
    
    if price_data.empty:
        print("Não foi possível obter os dados. Encerrando o script.")
        return

    # Passo 2: Simular os dois cenários
    interest_series = simulate_compound_interest(
        args.capital_inicial, args.aporte_mensal, args.taxa_juros_mensal, price_data.index
    )
    portfolio_series = simulate_portfolio(
        price_data, args.capital_inicial, args.aporte_mensal, weights
    )
    
    # Passo 3: Calcular as métricas para cada cenário
    interest_cagr = calculate_all_metrics(interest_series)['CAGR (%)'] / 100
    interest_metrics = calculate_all_metrics(interest_series)
    portfolio_metrics = calculate_all_metrics(portfolio_series, risk_free_cagr=interest_cagr)
    
    # Passo 4: Gerar os relatórios (tabela e gráficos)
    generate_report_table(interest_metrics, portfolio_metrics)
    generate_comparison_plot(interest_series, portfolio_series)
    generate_drawdown_plot(portfolio_series)
    
    print("Simulação e geração de relatórios concluídas com sucesso!")

if __name__ == "__main__":
    main()