# src/preprocess.py
import pandas as pd
import geopandas as gpd
from shapely.geometry import Point, LineString

def interpolar_horarios_viagem(df_stop_times, trip_id):
    """
    Filtra os dados de stop_times para uma viagem específica e preenche 
    os horários vazios (NaN) utilizando interpolação linear.
    
    Atividade Associada: A2 (Limpeza e Filtragem)
    """
    # 1. Filtrar pela viagem escolhida e criar uma cópia isolada
    df_viagem = df_stop_times[df_stop_times['trip_id'] == trip_id].copy()
    
    if df_viagem.empty:
        raise ValueError(f"A viagem com trip_id '{trip_id}' não foi encontrada nos dados.")
        
    # 2. Garantir a ordenação correta pela sequência de paradas
    df_viagem = df_viagem.sort_values('stop_sequence')
    
    # 3. Converter strings de horários (HH:MM:SS) para Timedelta para permitir cálculos matemáticos
    df_viagem['arrival_time_delta'] = pd.to_timedelta(df_viagem['arrival_time'])
    
    # 4. Aplicar a interpolação linear para preencher os valores nulos (NaN)
    df_viagem['arrival_time_delta'] = df_viagem['arrival_time_delta'].interpolate(method='linear')
    
    # 5. Converter de volta os Timedeltas para strings formatadas legíveis (HH:MM:SS)
    df_viagem['arrival_time_clean'] = df_viagem['arrival_time_delta'].dt.components.apply(
        lambda x: f"{int(x.hours):02d}:{int(x.minutes):02d}:{int(x.seconds):02d}", axis=1
    )
    
    return df_viagem

def criar_camada_geografica(df_shapes, shape_id):
    """
    Filtra os pontos de latitude e longitude de um shape_id específico e os
    converte em uma linha geográfica estruturada (LineString) no formato GeoDataFrame.
    
    Atividade Associada: A3 (Padronização e Camadas)
    """
    # 1. Filtrar os pontos geométricos do shape escolhido
    pontos_shape = df_shapes[df_shapes['shape_id'] == shape_id].copy()
    
    if pontos_shape.empty:
        raise ValueError(f"O traçado com shape_id '{shape_id}' não foi encontrado nos dados.")
        
    # 2. Ordenar estritamente pela sequência de pontos que desenham a rua
    pontos_shape = pontos_shape.sort_values('shape_pt_sequence')
    
    # 3. Juntar as coordenadas de longitude e latitude em objetos Point do Shapely
    coordenadas = [Point(xy) for xy in zip(pontos_shape['shape_pt_lon'], pontos_shape['shape_pt_lat'])]
    
    # 4. Unir todos os pontos sequenciais em uma única linha contínua (LineString)
    linha_geometria = LineString(coordenadas)
    
    # 5. Construir o GeoDataFrame definindo o sistema de coordenadas geográficas (WGS84 - EPSG:4326)
    gdf_rota = gpd.GeoDataFrame(geometry=[linha_geometria], crs="EPSG:4326")
    
    return gdf_rota