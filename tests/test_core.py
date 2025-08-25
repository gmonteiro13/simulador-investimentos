import sys
import pytest
import numpy as np
import pandas as pd
from metrics import calculate_cagr, calculate_max_drawdown
from interest import simulate_compound_interest
from portfolio import _normalize_weights


sys.path.append('modules')


# --- Teste 1: CAGR (Taxa de Crescimento Anual Composta) ---
def test_calculate_cagr():
    """
    Testa se o cálculo do CAGR está correto para um cenário simples.
    """
    # Usando um período que totaliza
    # exatamente 2 anos (730.5 dias / 365.25 = 2.0)
    datas = pd.to_datetime(['2021-01-01', '2022-12-31'])
    serie_teste = pd.Series([100.0, 121.0], index=datas)

    resultado_cagr = calculate_cagr(serie_teste)

    # Verificamos se o resultado, arredondado para 2 casas decimais, é 0.10
    assert round(resultado_cagr, 2) == 0.10


# --- Teste 2: Máximo Drawdown ---
def test_calculate_max_drawdown():
    """
    Testa se o cálculo do Máximo Drawdown está correto.
    Em uma série com pico de 120 e fundo de 90, o drawdown deve ser -25%.
    """
    datas = pd.to_datetime(
        ['2020-01-01', '2020-01-02', '2020-01-03', '2020-01-04']
    )
    serie_teste = pd.Series([100.0, 120.0, 90.0, 110.0], index=datas)

    resultado_drawdown = calculate_max_drawdown(serie_teste)

    valor_esperado = (90 - 120) / 120
    assert resultado_drawdown == pytest.approx(valor_esperado)


# --- Teste 3: Simulação de Juros Compostos ---
def test_simulate_compound_interest_logic():
    """
    Testa a lógica da simulação de juros\
    para um período curto e valores simples.
    """
    # Cenário: R$1000 iniciais, R$100 de aporte
    # 10% de juros ao mês, por 2 meses.
    capital_inicial = 1000
    aporte_mensal = 100
    taxa_juros_mensal = 10
    indice_datas = pd.bdate_range(start='2021-01-01', end='2021-02-28')

    # Mês 1
    # valor = 1000 * (1 + 0.1) ** (21/30) = 1070.0
    # Mês 2
    # valor = 1070 * (1 + 0.1) ** (20/30) + 100 = 1246.75

    valor_esperado_final = 1246.75

    resultado_simulacao = simulate_compound_interest(
        capital_inicial, aporte_mensal, taxa_juros_mensal, indice_datas
    )

    # Usamos uma tolerância (abs=2) por causa da
    # conversão de taxa mensal para diária
    assert resultado_simulacao.iloc[-1] == pytest.approx(
        valor_esperado_final,
        abs=2
    )


# --- Testes de Casos de Canto (Edge Cases) ---
def test_ffill_logic_for_nan_values():
    """Testa se a lógica de forward fill funciona como esperado."""
    datas = pd.to_datetime(['2023-01-02', '2023-01-03', '2023-01-04'])
    # O dia 3 não tem dados (NaN)
    serie_com_nan = pd.Series([10.0, np.nan, 12.0], index=datas)
    serie_preenchida = serie_com_nan.ffill()
    # O valor do dia 3 deve ser preenchido com o valor do dia 2 (R$10)
    assert serie_preenchida.loc['2023-01-03'] == 10.0


def test_weight_normalization():
    """Testa se os pesos que não somam 1 são normalizados corretamente."""
    pesos_nao_normalizados = [0.5, 0.5, 0.5]
    pesos_normalizados = _normalize_weights(pesos_nao_normalizados)

    # A soma dos pesos normalizados deve ser aproximadamente 1
    assert np.sum(pesos_normalizados) == pytest.approx(1.0)
    # Cada peso deve ser 1/3 do total
    assert pesos_normalizados[0] == pytest.approx(1/3)


def test_contribution_on_next_business_day():
    """
    Testa se o aporte é feito no próximo dia útil\
    se o mês virar no fim de semana.
    Fevereiro de 2021 terminou em um domingo.
    O aporte de Março deve ocorrer na segunda, dia 1º.
    """
    indice_datas = pd.bdate_range(start='2021-02-26', end='2021-03-01')
    # Sexta (26/02) e Segunda (01/03) são os dias úteis relevantes.

    simulacao = simulate_compound_interest(capital_inicial=1000,
                                           aporte_mensal=100,
                                           taxa_juros_mensal=0,
                                           dates=indice_datas)

    valor_na_sexta = simulacao.loc['2021-02-26']
    valor_na_segunda = simulacao.loc['2021-03-01']

    # O valor na segunda deve ser o valor da sexta
    # + o aporte (juros de 0% para simplificar)
    assert valor_na_segunda == valor_na_sexta + 100
