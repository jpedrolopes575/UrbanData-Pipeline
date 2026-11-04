import os
import sys
import pandas as pd

if 'SUMO_HOME' in os.environ:
    sys.path.append(os.path.join(os.environ['SUMO_HOME'], 'tools'))
else:
    sys.exit("Por favor, declare a variável de ambiente 'SUMO_HOME'")

import sumolib

caminho_rede = 'data/rede_fortaleza_estendida.net.xml'
caminho_shapes = 'data/shapes.txt'

SHAPE_ALVO = 'shape0016-I'

def extrair_edges_da_rota():
    print("Carregando a malha viária do SUMO...")
    net = sumolib.net.readNet(caminho_rede)

    print("Carregando os dados de geometria do GTFS...")
    colunas_importantes = ['shape_id', 'shape_pt_lat', 'shape_pt_lon', 'shape_pt_sequence']
    df_shapes = pd.read_csv(caminho_shapes, usecols=colunas_importantes)

    rota = df_shapes[df_shapes['shape_id'] == SHAPE_ALVO].sort_values(by='shape_pt_sequence')

    if rota.empty:
        sys.exit(f"Erro: Nenhum dado encontrado para o shape_id '{SHAPE_ALVO}'. Verifique o ID.")

    print(f"Mapeando {len(rota)} pontos geográficos para a rede viária...")
    
    lista_edges = []

    for index, ponto in rota.iterrows():
        lon = ponto['shape_pt_lon']
        lat = ponto['shape_pt_lat']
        
        x, y = net.convertLonLat2XY(lon, lat)
        
        edges_vizinhas = net.getNeighboringEdges(x, y, r=15)
        
        if edges_vizinhas:
            edge_mais_proxima = min(edges_vizinhas, key=lambda e: e[1])[0]
            id_edge = edge_mais_proxima.getID()
            
            if not lista_edges or lista_edges[-1] != id_edge:
                lista_edges.append(id_edge)

    print("\nExtração concluída! Sequência de Edge IDs gerada:")
    print(" ".join(lista_edges))
    
    with open('data/rota_edges.txt', 'w') as f:
        f.write(" ".join(lista_edges))
    print("\nArquivo 'data/rota_edges.txt' salvo com sucesso.")

if __name__ == "__main__":
    extrair_edges_da_rota()