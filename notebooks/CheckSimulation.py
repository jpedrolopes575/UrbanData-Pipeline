# notebooks/CheckSimulation.py
import os
import sys
import xml.etree.ElementTree as ET
import matplotlib.pyplot as plt
import pandas as pd

# Configura o caminho para encontrar a pasta 'src'
diretorio_atual = os.path.dirname(os.path.abspath(__file__))
raiz_projeto = os.path.dirname(diretorio_atual)
if raiz_projeto not in sys.path:
    sys.path.insert(0, raiz_projeto)

def analisar_resultado_onibus(caminho_xml='sumo/resultado_real.xml'):
    print("📊 Lendo resultados reais da simulação...")
    
    if not os.path.exists(caminho_xml):
        print(f"❌ Erro: O arquivo {caminho_xml} não foi encontrado!")
        return

    tree = ET.parse(caminho_xml)
    root = tree.getroot()
    
    dados_onibus = []
    for tripinfo in root.findall('tripinfo'):
        # Filtra apenas o veículo do ônibus que você configurou
        if 'viagem_101' in tripinfo.get('id') or tripinfo.get('vClass') == 'bus':
            dados_onibus.append({
                'id': tripinfo.get('id'),
                'duracao_minutos': float(tripinfo.get('duration')) / 60,
                'tempo_atraso_sinal_minutos': float(tripinfo.get('waitingTime')) / 60,
                'distancia_km': float(tripinfo.get('routeLength')) / 1000,
                'velocidade_media_kmh': float(tripinfo.get('speed')) * 3.6
            })
            
    if not dados_onibus:
        print("⚠️ Nenhum dado de ônibus foi encontrado no arquivo XML. O ônibus chegou ao fim da rota?")
        return
        
    df_resumo = pd.DataFrame(dados_onibus)
    
    # Exibe os dados formatados no terminal
    print("\n========= DESEMPENHO DO ÔNIBUS CORRIGIDO =========")
    print(f"🚌 ID do Veículo: {df_resumo['id'].iloc[0]}")
    print(f"⏱️ Tempo Total de Viagem: {df_resumo['duracao_minutos'].iloc[0]:.2f} minutos")
    print(f"🛑 Preso em Congestionamentos: {df_resumo['tempo_atraso_sinal_minutos'].iloc[0]:.2f} minutos")
    print(f"🛣️ Distância Percorrida: {df_resumo['distancia_km'].iloc[0]:.2f} km")
    print(f"⚡ Velocidade Média: {df_resumo['velocidade_media_kmh'].iloc[0]:.2f} km/h")
    print("==================================================\n")
    
    # Gera um gráfico de barras simples comparando Tempo em Movimento vs Parado
    plt.figure(figsize=(6, 4))
    tempo_movimento = df_resumo['duracao_minutos'].iloc[0] - df_resumo['tempo_atraso_sinal_minutos'].iloc[0]
    tempo_parado = df_resumo['tempo_atraso_sinal_minutos'].iloc[0]
    
    plt.bar(['Em Movimento', 'Preso no Trânsito'], [tempo_movimento, tempo_parado], color=['#2ecc71', '#e74c3c'])
    plt.ylabel('Tempo (Minutos)')
    plt.title('Divisão do Tempo de Viagem do Ônibus')
    
    os.makedirs('docs', exist_ok=True)
    plt.savefig('docs/grafico_desempenho_onibus.png', bbox_inches='tight')
    print("💾 Gráfico de desempenho salvo com sucesso em docs/grafico_desempenho_onibus.png!")

if __name__ == '__main__':
    analisar_resultado_onibus()