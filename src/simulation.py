# /home/usuario/UrbanData/src/simulation.py
import xml.etree.ElementTree as ET
from xml.dom import minidom
import sumolib
import os

def gerar_arquivos_sumo(df_viagem_com_paradas, caminho_rede_sumo, pasta_saida='simulacao'):
    """
    Pega os dados de paradas interpolados e tratados no Python e gera 
    automaticamente os arquivos paradas.add.xml e onibus.rou.xml para o SUMO.
    """
    print("🔄 Conectando dados do GTFS com a rede do SUMO...")
    
    # CORREÇÃO DEFINITIVA: Pega o caminho absoluto e adiciona o protocolo 'file://'
    # Isso impede que o leitor de XML do Python tente buscar uma URL de internet
    caminho_absoluto = os.path.abspath(caminho_rede_sumo)
    caminho_absoluto_rede = f"file://{caminho_absoluto}"
    
    # Agora o sumolib lerá o arquivo perfeitamente no Linux
    rede = sumolib.net.readNet(caminho_absoluto_rede)
    
    xml_adicional = ET.Element('additional')
   
    # ... (o resto do código do arquivo continua exatamente igual)
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
            
            # SOLUÇÃO ROBUSTA: friendlyPos="true" força o SUMO a ignorar erros de tamanho de rua
            ET.SubElement(xml_adicional, 'busStop', {
                'id': id_tag_parada,
                'lane': lane_id,
                'startPos': '0.0',
                'endPos': '-1.0', # No SUMO, -1 significa ir até o final exato da rua, não importa o tamanho dela
                'friendlyPos': 'true', # CORREÇÃO CRUCIAL: Corrige e tolera geometrias problemáticas
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
        'departPos': 'free',       # ALTERADO DE 'allowed' PARA 'free'
        'arrivalLane': 'current',  
        'arrivalPos': 'max'     # Garante a conclusão até o final da via
    })
    
    # ... (código anterior do arquivo)
    for id_parada, horario in lista_ids_paradas:
        # CORREÇÃO: Adicionado friendlyPos para evitar alertas de parada curta
        ET.SubElement(trip, 'stop', {'busStop': id_parada, 'duration': '20', 'friendlyPos': 'true'})
        
    _salvar_xml_bonito(xml_adicional, f"{pasta_saida}/paradas.add.xml")
    _salvar_xml_bonito(xml_rotas, f"{pasta_saida}/onibus.rou.xml")

def _salvar_xml_bonito(elemento_xml, caminho_saida):
    xml_str = minidom.parseString(ET.tostring(elemento_xml)).toprettyxml(indent="    ")
    with open(caminho_saida, "w", encoding="utf-8") as f:
        f.write(xml_str)
    print(f"✅ Arquivo gerado com sucesso: {caminho_saida}")