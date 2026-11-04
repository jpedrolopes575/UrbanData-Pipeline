import pandas as pd

caminho_shapes = 'data/shapes.txt'

def encontrar_rotas_no_mapa():
    print("Lendo os dados de geometria do GTFS...")
    df_shapes = pd.read_csv(caminho_shapes)

    # Coordenadas limites da sua rede no Carlito Pamplona (baseado no seu arquivo .osm)
    min_lat, max_lat = -3.715, -3.712
    min_lon, max_lon = -38.556, -38.550

    print("Procurando linhas de ônibus que passam pela região...")
    
    # Filtra apenas os pontos de GPS que caem dentro dessa "caixa" de coordenadas
    pontos_na_area = df_shapes[
        (df_shapes['shape_pt_lat'] >= min_lat) & 
        (df_shapes['shape_pt_lat'] <= max_lat) & 
        (df_shapes['shape_pt_lon'] >= min_lon) & 
        (df_shapes['shape_pt_lon'] <= max_lon)
    ]

    # Extrai os IDs únicos das rotas que têm pontos nessa área
    shapes_validos = pontos_na_area['shape_id'].unique()

    if len(shapes_validos) > 0:
        print(f"\nSucesso! Encontramos {len(shapes_validos)} trajetos nessa área.")
        print("Aqui estão alguns IDs que você pode usar:")
        for sid in shapes_validos[:5]:  # Exibe os 5 primeiros para você escolher
            print(f" -> {sid}")
    else:
        print("\nNenhuma rota de ônibus encontrada exatamente dentro dessas coordenadas.")

if __name__ == "__main__":
    encontrar_rotas_no_mapa()