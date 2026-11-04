import pandas as pd
import zipfile

# Caminho para o seu arquivo GTFS compactado
gtfs_zip_path = 'data/fortaleza.zip'

print("Lendo dados do GTFS Estático diretamente do arquivo ZIP...")

try:
    # Abrindo o ZIP e lendo os arquivos necessários em memória
    with zipfile.ZipFile(gtfs_zip_path, 'r') as z:
        # Lendo as paradas (coordenadas)
        with z.open('stops.txt') as f:
            stops = pd.read_csv(f, usecols=['stop_id', 'stop_lat', 'stop_lon'])
            
        # Lendo os horários programados
        with z.open('stop_times.txt') as f:
            stop_times = pd.read_csv(f, usecols=['trip_id', 'arrival_time', 'stop_id', 'stop_sequence'])

    # Alinhando as informações (Horário + Posição da Parada)
    gtfs_estatico = pd.merge(stop_times, stops, on='stop_id', how='left')
    
    print(f"Sucesso! GTFS Estático carregado: {len(gtfs_estatico)} registros.")
    print("-" * 40)
    print(gtfs_estatico.head())

except FileNotFoundError:
    print(f"⚠️ Erro: Não encontrei o arquivo em {gtfs_zip_path}. Verifique o nome da pasta.")
except Exception as e:
    print(f"⚠️ Erro ao ler o GTFS: {e}")