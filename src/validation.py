import numpy as np
import pandas as pd


def calcular_metricas_validacao(df_simulado, df_real, coluna_valor):
  df_comparacao = pd.merge(
      df_simulado, df_real, on='id_segmento', suffixes=('_sim', '_real')
  )

  y_sim = df_comparacao[f'{coluna_valor}_sim']
  y_real = df_comparacao[f'{coluna_valor}_real']

  # Cálculo do RMSE
  rmse = np.sqrt(np.mean((y_sim - y_real) ** 2))

  # Cálculo do MAPE (%) evitando divisão por zero
  mape = np.mean(np.abs((y_real - y_sim) / y_real)) * 100

  return {'RMSE': rmse, 'MAPE (%)': mape, 'dados_comparados': df_comparacao}


def gerar_relatorio_validacao(resultados):
  """Exibe um resumo formatado dos resultados estatísticos da calibração."""
  print('=== RELATÓRIO DE VALIDAÇÃO ESTATÍSTICA (SUMO vs REAL) ===')
  print(f"-> RMSE (Erro Quadrático Médio): {resultados['RMSE']:.2f}")
  print(f"-> MAPE (Erro Percentual Absoluto): {resultados['MAPE (%)']:.2f}%")
  print('===========================================================')