# =====================================================================
# 1. ESTE BLOCO PRECISA SER A PRIMEIRA COISA DO ARQUIVO (Configura o Caminho)
# =====================================================================
import os
import sys

# Descobre o caminho da raiz do projeto e injeta na busca do Python
diretorio_atual = os.path.dirname(os.path.abspath(__file__))
raiz_projeto = os.path.dirname(diretorio_atual)

if raiz_projeto not in sys.path:
    sys.path.insert(0, raiz_projeto)

# =====================================================================
# 2. AGORA SIM, COLOQUE TODOS OS OUTROS IMPORTS ABAIXO:
# =====================================================================
from src.preprocess import interpolar_horarios_viagem, criar_camada_geografica
from src.simulation import gerar_arquivos_sumo  

import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt

# Desativa o backend gráfico para rodar limpo no terminal do Linux
plt.switch_backend('Agg') 

# ... (resto do seu código de carregamento de dados e análise)

# 1. Carregamento de dados  
trips = pd.read_csv('data/trips.txt')
stop_times = pd.read_csv('data/stop_times.txt')
stops = pd.read_csv('data/stops.txt')
shapes = pd.read_csv('data/shapes.txt')

# Escolher uma linha de teste
trip_id_teste = trips['trip_id'].iloc[0]
shape_id_teste = trips[trips['trip_id'] == trip_id_teste]['shape_id'].iloc[0]

#Processar os Horários com a função especificada
viagem_processada = interpolar_horarios_viagem(stop_times, trip_id_teste)
viagem_com_paradas = pd.merge(viagem_processada, stops, on='stop_id')

# Processar a Geometria com a sua função especificada
gdf_rota = criar_camada_geografica(shapes, shape_id_teste)

# Criar GeoDataFrame das paradas para plotagem
gdf_paradas = gpd.GeoDataFrame(
    viagem_com_paradas, 
    geometry=gpd.points_from_xy(viagem_com_paradas['stop_lon'], viagem_com_paradas['stop_lat']),
    crs="EPSG:4326"
)

# Criação da figura:
fig, ax = plt.subplots(figsize=(10, 8))

#Desenhar as camadas geográficas passando o 'ax'
print("Desenhando camadas no mapa...")
gdf_rota.plot(ax=ax, color='#1a3a5f', linewidth=3, label='Traçado da Rota')
gdf_paradas.plot(ax=ax, color='#e74c3c', markersize=40, zorder=3, label='Pontos Interpolados')

#Configurações do gráfico
ax.set_title(f"Visualização Espacial da Viagem - Shape: {shape_id_teste}", fontsize=14)
ax.set_xlabel("Longitude")
ax.set_ylabel("Latitude")
ax.grid(True, linestyle='--', alpha=0.5)
plt.legend()

# Gravação do arquivo na pasta
print("💾 Gravando o mapa fisicamente em docs/mapa_rota_teste.png...")
plt.savefig('docs/mapa_rota_teste.png', dpi=300, bbox_inches='tight')

print("✅ Arquivo gerado e consolidado com sucesso em docs/mapa_rota_teste.png!")


print("🚀 Iniciando exportação para o SUMO...")

gerar_arquivos_sumo(
    df_viagem_com_paradas=viagem_com_paradas, 
    caminho_rede_sumo='sumo/osm.net.xml',
    pasta_saida='sumo'
)