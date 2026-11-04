# /home/usuario/UrbanData/src/simulation.py
import xml.etree.ElementTree as ET
from xml.dom import minidom
import sumolib
import os
from validation import calcular_metricas_validacao, gerar_relatorio_validacao

def gerar_arquivos_sumo(df_viagem_com_paradas, caminho_rede_sumo, pasta_saida='sumo'):
    print("🔄 Conectando dados do GTFS com a rede do SUMO...")
    
    caminho_absoluto = os.path.abspath(caminho_rede_sumo)
    caminho_absoluto_rede = f"file://{caminho_absoluto}"
    
    
    rede = sumolib.net.readNet(caminho_absoluto_rede)
    
    xml_adicional = ET.Element('additional')
    xml_rotas = ET.Element('routes')
    
    ET.SubElement(xml_rotas, 'vType', {'id': 'onibus_fortaleza', 'vClass': 'passenger', 'length': '12.0', 'color': '1,0,0'})
    
    lista_ids_paradas = []
    ruas_do_percurso = []
    
    for idx, row in df_viagem_com_paradas.iterrows():
        lat = row['stop_lat']
        lon = row['stop_lon']
        stop_id = str(row['stop_id'])
        
        x, y = rede.convertLonLat2XY(lon, lat)
        ruas_proximas = rede.getNeighboringEdges(x, y, 50)
        
        if ruas_proximas:
            rua_proxima, distancia = ruas_proximas[0]
            edge_id = rua_proxima.getID()
            lane_id = f"{edge_id}_0"
            
            ruas_do_percurso.append(edge_id)
            id_tag_parada = f"parada_{stop_id}"
            lista_ids_paradas.append((id_tag_parada, row['arrival_time_clean']))
            ET.SubElement(xml_adicional, 'busStop', {
                'id': id_tag_parada,
                'lane': lane_id,
                'startPos': '0.0',
                'endPos': '-1.0', 
                'friendlyPos': 'true', 
                'lines': '101',
                'name': str(row['stop_name'])
            })
            
    h, m, s = map(int, df_viagem_com_paradas['arrival_time_clean'].iloc[0].split(':'))
    segundos_partida = str(h * 3600 + m * 60 + s)
    
    trip = ET.SubElement(xml_rotas, 'trip', {
        'id': 'viagem_101_automatica',
        'type': 'onibus_fortaleza',
        'depart': segundos_partida,
        'from': ruas_do_percurso[0],
        'to': ruas_do_percurso[-1],
        'departLane': 'best',      
        'departPos': 'free',       
        'arrivalLane': 'current',  
        'arrivalPos': 'max'     
    })
    for id_parada, horario in lista_ids_paradas:
        ET.SubElement(trip, 'stop', {'busStop': id_parada, 'duration': '20', 'friendlyPos': 'true'})
        
    _salvar_xml_bonito(xml_adicional, f"{pasta_saida}/paradas.add.xml")
    _salvar_xml_bonito(xml_rotas, f"{pasta_saida}/onibus.rou.xml")

def _salvar_xml_bonito(elemento_xml, caminho_saida):
    xml_str = minidom.parseString(ET.tostring(elemento_xml)).toprettyxml(indent="    ")
    with open(caminho_saida, "w", encoding="utf-8") as f:
        f.write(xml_str)
    print(f"✅ Arquivo gerado com sucesso: {caminho_saida}")

    # --- Adicione isto no FINAL do seu arquivo src/simulation.py ---

import pandas as pd


def executar_pipeline_simulacao(caminho_csv_viagem, caminho_rede):
  # 1. Carrega os dados do GTFS filtrados para a viagem
  df_viagem = pd.read_csv(caminho_csv_viagem)

  # 2. Gera os arquivos XML do SUMO usando a sua função existente
  gerar_arquivos_sumo(df_viagem, caminho_rede, pasta_saida='simulacao')
  print('🚀 Arquivos do SUMO gerados com sucesso!')

  # 3. Bloco de Validação Estatística (Integração com validation.py)
  try:
    print('📊 A carregar dados para validação estatística...')

    # Substitua pelos caminhos reais dos seus arquivos de saída e Ground Truth
    # (Ex: saída convertida do SUMO e dados reais de campo)
    df_saida_sumo = pd.read_csv('sumo/edgeData.csv')
    df_ground_truth = pd.read_csv('data/ground_truth.csv')

    # Calcula RMSE e MAPE comparando a coluna de tempo de viagem
    resultados = calcular_metricas_validacao(
        df_saida_sumo, df_ground_truth, coluna_valor='tempo_viagem'
    )

    # Exibe o relatório formatado no terminal
    gerar_relatorio_validacao(resultados)

  except FileNotFoundError as e:
    print(
        f'⚠️ Aviso: Arquivo de saída para validação não encontrado ({e}).'
        ' Rode a simulação no SUMO primeiro para gerar os relatórios.'
    )


import subprocess
import pandas as pd

if __name__ == '__main__':
  print('🚀 Iniciando processamento do SUMO...')

  # 1. Carrega os dados brutos do GTFS da pasta data/ e faz o merge
  df_stop_times = pd.read_csv('data/stop_times.txt')
  df_stops = pd.read_csv('data/stops.txt')
  df_viagem_completo = pd.merge(df_stop_times, df_stops, on='stop_id')

  if (
      'arrival_time_clean' not in df_viagem_completo.columns
      and 'arrival_time' in df_viagem_completo.columns
  ):
    df_viagem_completo['arrival_time_clean'] = df_viagem_completo[
        'arrival_time'
    ]

  # 2. Gera os ficheiros de paragem e rota diretamente na pasta sumo/
  caminho_rede = 'sumo/osm.net.xml'
  # Mude 'simulacao' para 'sumo' para salvar direto na pasta correta
  gerar_arquivos_sumo(df_viagem_completo, caminho_rede, pasta_saida='sumo')

  # 3. Executa a simulação do SUMO via linha de comando usando o .sumocfg
  print('🚗 A executar a simulação no SUMO...')
  try:
    comando_sumo = ['sumo', '-c', 'sumo/osm.sumocfg']
    subprocess.run(comando_sumo, check=True)
    print('✅ Simulação concluída com sucesso pelo SUMO!')
  except subprocess.CalledProcessError as e:
    print(f'❌ Erro ao executar a simulação no SUMO: {e}')
    exit(1)

  # 4. Executa a Validação Estatística (RMSE e MAPE)
  try:
    print('📊 A calcular métricas de validação estatística...')

    # Lê os dados resultantes e o Ground Truth de campo
    df_saida_sumo = pd.read_csv('sumo/resultado_simulacao.csv')
    df_ground_truth = pd.read_csv('data/ground_truth.csv')

    resultados = calcular_metricas_validacao(
        df_saida_sumo, df_ground_truth, coluna_valor='tempo_viagem'
    )

    gerar_relatorio_validacao(resultados)

  except FileNotFoundError as e:
    print(f'⚠️ Aviso: Ficheiro para validação não encontrado ({e}).')