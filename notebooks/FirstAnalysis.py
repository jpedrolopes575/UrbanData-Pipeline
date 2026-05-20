import pandas as pd

# 1. Carregar as tabelas principais
routes = pd.read_csv('data/routes.txt')
trips = pd.read_csv('data/trips.txt')
stop_times = pd.read_csv('data/stop_times.txt')
stops = pd.read_csv('data/stops.txt')

# 2. Fazer um cruzamento (Merge) para entender o fluxo
# Vamos descobrir todas as paradas de uma viagem específica
exemplo_viagem = stop_times[stop_times['trip_id'] == trips['trip_id'].iloc[0]]
exemplo_com_paradas = pd.merge(exemplo_viagem, stops, on='stop_id')

# Exibir a sequência de pontos e horários esperados para aquela viagem
print(exemplo_com_paradas[['stop_sequence', 'arrival_time', 'stop_name']])