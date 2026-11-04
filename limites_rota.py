import pandas as pd

caminho_shapes = 'data/shapes.txt'
shape_alvo = 'shape0016-I'

def descobrir_limites():
    print(f"Lendo os dados de geometria para a rota {shape_alvo}...")
    df_shapes = pd.read_csv(caminho_shapes)
    
    # Filtra apenas a nossa rota
    rota = df_shapes[df_shapes['shape_id'] == shape_alvo]
    
    if rota.empty:
        print("Rota não encontrada.")
        return
        
    min_lat = rota['shape_pt_lat'].min()
    max_lat = rota['shape_pt_lat'].max()
    min_lon = rota['shape_pt_lon'].min()
    max_lon = rota['shape_pt_lon'].max()
    
    print("\n--- Coordenadas para o OpenStreetMap ---")
    print(f"Latitude Mínima (Sul): {min_lat}")
    print(f"Latitude Máxima (Norte): {max_lat}")
    print(f"Longitude Mínima (Oeste): {min_lon}")
    print(f"Longitude Máxima (Leste): {max_lon}")

if __name__ == "__main__":
    descobrir_limites()