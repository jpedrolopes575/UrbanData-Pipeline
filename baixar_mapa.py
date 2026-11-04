import requests
import time

# --- 1. COLOQUE AQUI OS VALORES DO SCRIPT limites_rota.py ---
min_lat = -3.738583  # Exemplo (Sul)
max_lat = -3.699899  # Exemplo (Norte)
min_lon = -38.591509 # Exemplo (Oeste)
max_lon = -38.480189 # Exemplo (Leste)
# -------------------------------------------------------------

def baixar_mapa():
    sul = min_lat - 0.005
    norte = max_lat + 0.005
    oeste = min_lon - 0.005
    leste = max_lon + 0.005

    print(f"Área de extração: Sul={sul:.4f}, Norte={norte:.4f}, Oeste={oeste:.4f}, Leste={leste:.4f}")
    
    query = f"""
    [out:xml][timeout:300];
    (
      node({sul},{oeste},{norte},{leste});
      way({sul},{oeste},{norte},{leste});
      relation({sul},{oeste},{norte},{leste});
    );
    out body;
    >;
    out skel qt;
    """

    # Lista de servidores espelho do OSM para fugir do congestionamento
    servidores = [
        "https://lz4.overpass-api.de/api/interpreter",
        "https://z.overpass-api.de/api/interpreter",
        "https://overpass-api.de/api/interpreter"
    ]
    
    cabecalhos = {
        'User-Agent': 'PesquisaIniciacaoTecnologica-Subprojeto2-IFCE/1.0',
        'Accept': '*/*'
    }

    for url in servidores:
        print(f"\nTentando conectar ao servidor: {url} ...")
        try:
            response = requests.post(url, data={'data': query}, headers=cabecalhos, timeout=300)
            
            if response.status_code == 200:
                caminho_arquivo = 'data/fortaleza_estendida.osm'
                with open(caminho_arquivo, 'wb') as f:
                    f.write(response.content)
                print(f"Sucesso Absoluto! O mapa completo foi salvo em: {caminho_arquivo}")
                return # O download deu certo, então encerramos a função aqui
            
            else:
                print(f"Servidor ocupado (Erro HTTP: {response.status_code}).")
                
        except requests.exceptions.Timeout:
            print("O servidor demorou muito para responder (Timeout).")
        except Exception as e:
            print(f"Ocorreu um erro na conexão: {e}")
            
        print("Aguardando 5 segundos antes de tentar o próximo servidor espelho...")
        time.sleep(5)

    print("\nTodos os servidores estão congestionados no momento. Tente rodar o script novamente em alguns minutos.")

if __name__ == "__main__":
    baixar_mapa()