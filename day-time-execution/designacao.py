import numpy as np
from solver import Solver
from atendimentos import Atendimentos
from ambulancias import Ambulancias
from typing import List, Dict, Tuple
from tqdm import tqdm
import random
from environment import Environment
import math
from statistics import stdev, mean

import matplotlib.pyplot as plt

TEMPO_ATUAL = 0
QUANTIDADE_DE_DIAS = 7
CICLOS_DA_SIMULACAO = 96 * QUANTIDADE_DE_DIAS # (quantidade de ciclos de 15 minutos em x dias)
TEMPO_ENTRE_SIMULACOES = 15

# definir uma velocidade média para todas as ambulâncias (57km/h) - done
# definir a escala do mapa (20km por 20km) - done
# número de chamados por tempo

# tempo médio de atendimento - done
# variância - done

# 1. Quantas vezes um atendimento básico / urgente deixou de ser atendidom - done
# 2. Qual é a média de tempo que um chamado urgente leva para ser atendido? - done
# 3. Qual o número médio de USB/USA's disponíveis por passo de tempo? - done
# 4. Qual a média da distância que uma unidade está de um chamado atribuído? - done

# Experimentos
# variar a quantidade de ambulâncias e velocidade
# Velocidade    | Ambulâncias Avançadas     | Ambulâncias Básicas | Done

# 40km/h        | 6                         | 21                    | X
# 50km/h        | 6                         | 21                    | 
# 60km/h        | 6                         | 21                    | 

# 50km/h        | 3                         | 14                    | 
# 50km/h        | 6                         | 21                    | 
# 50km/h        | 9                         | 28                    | 

# 40km/h        | 3                         | 14                    | 
# 60km/h        | 9                         | 28                    | 

todosOsAtendimentosAvancadosNaoRealizadosByUID : Dict[str, float] = {}
todosOsAtendimentosBasicosNaoRealizadosByUID : Dict[str, float] = {}

mediaDeTempoDeEsperaDeAtendimentosAvancados : List[float] = []
mediaDeTempoDeEsperaDeAtendimentosBasicos : List[float] = []

ambulancias_avancadas_disponiveis_por_simulacao = []
ambulancias_basicas_disponiveis_por_simulacao = []

numero_de_atendimentos_avancados_nao_comtemplados = []
numero_de_atendimentos_basicos_nao_comtemplados = []

mediaDeDistanciaDosAtendimentosBasicos = []
mediaDeDistanciaDosAtendimentosAvancados = []

def filtrar_ambulancias_nao_impedidas(ambulancias: List[Dict[str, float]]):
    ambulanciasNaoImpedidas = []
    
    for ambulancia in ambulancias:
        if 'impedida' not in ambulancia or ambulancia.get('impedida') <= TEMPO_ATUAL:
            ambulanciasNaoImpedidas.append(ambulancia)
    
    return ambulanciasNaoImpedidas

atendimentosAvancadosNaoContemplados = []
atendimentosBasicosNaoContemplados = []

bases: List[Tuple[float,float]] = []
bases.append([Environment.MAP_SIZE/2, Environment.MAP_SIZE/2 + Environment.MAP_SIZE*(math.sqrt(2)/4)])
bases.append([Environment.MAP_SIZE/2 - Environment.MAP_SIZE*(math.sqrt(2)/4), Environment.MAP_SIZE/2 - Environment.MAP_SIZE*(math.sqrt(2)/4)])
bases.append([Environment.MAP_SIZE/2 + Environment.MAP_SIZE*(math.sqrt(2)/4), Environment.MAP_SIZE/2 - Environment.MAP_SIZE*(math.sqrt(2)/4)])

ambulanciasAvancadas: List[Dict[str, int]] = Ambulancias.generate(Environment.AVANCADAS, bases)
ambulanciasBasicas: List[Dict[str, int]] = Ambulancias.generate(Environment.BASICAS, bases)

simulacao = 0

for _ in tqdm(range(0, CICLOS_DA_SIMULACAO)):
    TEMPO_ATUAL = simulacao * TEMPO_ENTRE_SIMULACOES
    atendimentosAvancados: List[Dict[str, int]] = Atendimentos.generate(atendimentosAvancadosNaoContemplados, todosOsAtendimentosAvancadosNaoRealizadosByUID, max = 8)
    atendimentosBasicos: List[Dict[str, int]] = Atendimentos.generate(atendimentosBasicosNaoContemplados, todosOsAtendimentosBasicosNaoRealizadosByUID, max = 15)
    
    ambulanciasAvancadasNaoImpedidas = filtrar_ambulancias_nao_impedidas(ambulanciasAvancadas)
    ambulanciasBasicasNaoImpedidas = filtrar_ambulancias_nao_impedidas(ambulanciasBasicas)
    
    quantidade_de_ambulancias_avancadas = len(ambulanciasAvancadasNaoImpedidas)
    quantidade_de_atendimentos_avancados = len(atendimentosAvancados)

    quantidade_de_ambulancias_basicas = len(ambulanciasBasicasNaoImpedidas)
    quantidade_de_atendimentos_basicos = len(atendimentosBasicos)

    prioridade_ocorrencias_avancadas = []

    for i in range(quantidade_de_atendimentos_avancados):
        prioridade_ocorrencias_avancadas.append(atendimentosAvancados[i]["peso"])

    prioridade_ocorrencias_basicas = []

    for i in range(quantidade_de_atendimentos_basicos):
        prioridade_ocorrencias_basicas.append(atendimentosBasicos[i]["peso"])


    tempos_ambulancias_avancadas = []

    for i in range(quantidade_de_ambulancias_avancadas):
        tempos_ambulancias_avancadas.append([])
        for j in range(quantidade_de_atendimentos_avancados):
            posicao_ambulancia = np.array([ambulanciasAvancadasNaoImpedidas[i].get("x"), ambulanciasAvancadasNaoImpedidas[i].get("y")])
            posicao_atendimento = np.array([atendimentosAvancados[j].get("x"), atendimentosAvancados[j].get("y")])
            distancia_euclidiana = np.linalg.norm(posicao_ambulancia - posicao_atendimento)
            tempo = (distancia_euclidiana / Environment.AVERAGE_SPEED) + (60 * (random.random()))
            tempos_ambulancias_avancadas[i].append(tempo)

    tempos_ambulancias_basicas = []

    for i in range(quantidade_de_ambulancias_basicas):
        tempos_ambulancias_basicas.append([])
        for j in range(quantidade_de_atendimentos_basicos):
            posicao_ambulancia = np.array([ambulanciasBasicasNaoImpedidas[i].get("x"), ambulanciasBasicasNaoImpedidas[i].get("y")])
            posicao_atendimento = np.array([atendimentosBasicos[j].get("x"), atendimentosBasicos[j].get("y")])
            distancia_euclidiana = np.linalg.norm(posicao_ambulancia - posicao_atendimento)
            tempo = (distancia_euclidiana / Environment.AVERAGE_SPEED) + (30 * (random.random()))
            tempos_ambulancias_basicas[i].append(tempo)
            
            
    solucao = Solver.solve(prioridade_ocorrencias_avancadas, prioridade_ocorrencias_basicas, tempos_ambulancias_avancadas, tempos_ambulancias_basicas)


    for i in range(quantidade_de_ambulancias_avancadas):
        for j in range(quantidade_de_atendimentos_avancados):
            if solucao["avancados"][(i,j)]:
                ambulanciasAvancadasNaoImpedidas[i]["impedida"] = TEMPO_ATUAL + tempos_ambulancias_avancadas[i][j]
    
    atendimentosAvancadosNaoContemplados = []
    distanciasAvancadasParciais = []
    for j in range(quantidade_de_atendimentos_avancados):
        atendido = False
        for i in range(quantidade_de_ambulancias_avancadas):
            if solucao["avancados"][(i,j)]:
                atendido = True
                posicao_ambulancia = np.array([ambulanciasAvancadasNaoImpedidas[i].get("x"), ambulanciasAvancadasNaoImpedidas[i].get("y")])
                posicao_atendimento = np.array([atendimentosAvancados[j].get("x"), atendimentosAvancados[j].get("y")])
                distancia_euclidiana = np.linalg.norm(posicao_ambulancia - posicao_atendimento)
                distanciasAvancadasParciais.append(distancia_euclidiana) 
                break
        
        if not atendido and (atendimentosAvancados[j]["id"] not in todosOsAtendimentosAvancadosNaoRealizadosByUID or
                             todosOsAtendimentosAvancadosNaoRealizadosByUID[atendimentosAvancados[j]["id"]] < 180):
            atendimentosAvancadosNaoContemplados.append(atendimentosAvancados[j])
            
            if atendimentosAvancados[j]["id"] not in todosOsAtendimentosAvancadosNaoRealizadosByUID:
                todosOsAtendimentosAvancadosNaoRealizadosByUID[atendimentosAvancados[j]["id"]] = 0
           
            todosOsAtendimentosAvancadosNaoRealizadosByUID[atendimentosAvancados[j]["id"]] += TEMPO_ENTRE_SIMULACOES
        
        else:
            todosOsAtendimentosAvancadosNaoRealizadosByUID[atendimentosAvancados[j]["id"]] = 0
    
    res = 0
    for ele in ambulanciasAvancadas: 
        if 'impedida' not in ele or ele.get('impedida') <= TEMPO_ATUAL: 
            res = res + 1
    
    ambulancias_avancadas_disponiveis_por_simulacao.append(res)

    for i in range(quantidade_de_ambulancias_basicas):
        for j in range(quantidade_de_atendimentos_basicos):
            if solucao["basicos"][(i,j)]:
                ambulanciasBasicasNaoImpedidas[i]["impedida"] = TEMPO_ATUAL + tempos_ambulancias_basicas[i][j]
    
    atendimentosBasicosNaoContemplados = []
    distanciasBasicasParciais = []
    for j in range(quantidade_de_atendimentos_basicos):
        atendido = False
        for i in range(quantidade_de_ambulancias_basicas):
            if solucao["basicos"][(i,j)]:
                atendido = True
                posicao_ambulancia = np.array([ambulanciasBasicasNaoImpedidas[i].get("x"), ambulanciasBasicasNaoImpedidas[i].get("y")])
                posicao_atendimento = np.array([atendimentosBasicos[j].get("x"), atendimentosBasicos[j].get("y")])
                distancia_euclidiana = np.linalg.norm(posicao_ambulancia - posicao_atendimento)
                distanciasBasicasParciais.append(distancia_euclidiana) 
                break
        
        if not atendido and (atendimentosBasicos[j]["id"] not in  todosOsAtendimentosBasicosNaoRealizadosByUID or
                 todosOsAtendimentosBasicosNaoRealizadosByUID[atendimentosBasicos[j]["id"]] <= 120):
            atendimentosBasicosNaoContemplados.append(atendimentosBasicos[j])
            
            if atendimentosBasicos[j]["id"] not in todosOsAtendimentosBasicosNaoRealizadosByUID:
                todosOsAtendimentosBasicosNaoRealizadosByUID[atendimentosBasicos[j]["id"]] = 0
           
            todosOsAtendimentosBasicosNaoRealizadosByUID[atendimentosBasicos[j]["id"]] += TEMPO_ENTRE_SIMULACOES
        
        else:
            todosOsAtendimentosBasicosNaoRealizadosByUID[atendimentosBasicos[j]["id"]] = 0
            
            
    res = 0
    for ele in ambulanciasBasicas: 
        if 'impedida' not in ele or ele.get('impedida') <= TEMPO_ATUAL: 
            res = res + 1
    
    ambulancias_basicas_disponiveis_por_simulacao.append(res)
    
    numero_de_atendimentos_basicos_nao_comtemplados.append(len(atendimentosBasicosNaoContemplados))
    numero_de_atendimentos_avancados_nao_comtemplados.append(len(atendimentosAvancadosNaoContemplados))
    
    simulacao += 1
    
    media: float = 0
    q = 0
    for uid in todosOsAtendimentosAvancadosNaoRealizadosByUID:
        media += todosOsAtendimentosAvancadosNaoRealizadosByUID[uid]
        if todosOsAtendimentosAvancadosNaoRealizadosByUID[uid] > 0:
            q = q + 1
    
    media = media / (q or 1)        
    mediaDeTempoDeEsperaDeAtendimentosAvancados.append(media)
    
    media = 0
    q = 0
    for uid in todosOsAtendimentosBasicosNaoRealizadosByUID:
        media += todosOsAtendimentosBasicosNaoRealizadosByUID[uid]
        if todosOsAtendimentosBasicosNaoRealizadosByUID[uid] > 0:
            q = q + 1
    
    media = media / (q or 1)   
    mediaDeTempoDeEsperaDeAtendimentosBasicos.append(media)
    
    mediaDeDistanciaDosAtendimentosBasicos.append(mean(distanciasBasicasParciais or [0]))
    mediaDeDistanciaDosAtendimentosAvancados.append(mean(distanciasAvancadasParciais or [0]))
    
fig1, ax = plt.subplots()
fig2, ax2 = plt.subplots()

fig3, ax3 = plt.subplots()
fig4, ax4 = plt.subplots()

fig5, ax5 = plt.subplots()
fig6, ax6 = plt.subplots()

fig7, ax7 = plt.subplots()
fig8, ax8 = plt.subplots()

mediaAvancada = mean(mediaDeTempoDeEsperaDeAtendimentosAvancados)
desvioPadraoAvancado = stdev(mediaDeTempoDeEsperaDeAtendimentosAvancados)
ax.plot(range(0, simulacao), mediaDeTempoDeEsperaDeAtendimentosAvancados, color="blue")
ax.axhline(y=(mediaAvancada + desvioPadraoAvancado), xmin= 0, xmax=simulacao, color="red")
ax.axhline(y=mediaAvancada, xmin= 0, xmax=simulacao, color="orange")
ax.axhline(y=(mediaAvancada - desvioPadraoAvancado), xmin= 0, xmax=simulacao, color="black")
ax.set_title("Tempo de Espera Médio Para Atendimentos Avançados (minutos)")
ax.set_ylabel("Tempo em Minutos")
ax.set_xlabel("Execuções (Ciclos de Cinco Minutos)")
ax.legend(["Tempo de Espera Médio Para Atendimentos Avançados", "Média Geral + Desvio Padrão", "Média Geral", "Média Geral - Desvio Padrão"])

fig1.savefig(f"Espera_Media_Avancadas_{Environment.SPEED}_{Environment.AVANCADAS}")

mediaBasica = mean(mediaDeTempoDeEsperaDeAtendimentosBasicos)
desvioPadroaBasico = stdev(mediaDeTempoDeEsperaDeAtendimentosBasicos)
ax2.plot(range(0, simulacao), mediaDeTempoDeEsperaDeAtendimentosBasicos, color="green")
ax2.axhline(y=(mediaBasica + desvioPadroaBasico), xmin= 0, xmax=simulacao, color="red")
ax2.axhline(y=(mediaBasica), xmin= 0, xmax=simulacao, color="orange")
ax2.axhline(y=(mediaBasica - desvioPadroaBasico), xmin= 0, xmax=simulacao, color="black")
ax2.set_title("Tempo de Espera Médio Para Atendimentos Básicos (minutos)")
ax2.set_ylabel("Tempo em Minutos")
ax2.set_xlabel("Execuções (Ciclos de Cinco Minutos)")
ax2.legend(["Tempo de Espera Médio Para Atendimentos Básicos", "Média Geral + Desvio Padrão", "Média Geral", "Média Geral - Desvio Padrão"])

fig2.savefig(f"Espera_Media_Basicas_{Environment.SPEED}_{Environment.BASICAS}")

mediaBasica = mean(numero_de_atendimentos_basicos_nao_comtemplados)
desvioPadroaBasico = stdev(numero_de_atendimentos_basicos_nao_comtemplados)
ax3.plot(range(0, simulacao), numero_de_atendimentos_basicos_nao_comtemplados, color="green")
ax3.axhline(y=(mediaBasica + desvioPadroaBasico), xmin= 0, xmax=simulacao, color="red")
ax3.axhline(y=(mediaBasica), xmin= 0, xmax=simulacao, color="orange")
ax3.axhline(y=(mediaBasica - desvioPadroaBasico), xmin= 0, xmax=simulacao, color="black")
ax3.set_title("Número de Atendimentos Basicos Não Realizados")
ax3.set_ylabel("Número de Atendimentos Basicos Não Realizados")
ax3.set_xlabel("Execuções (Ciclos de Quinze Minutos)")
ax3.legend(["Número de Atendimentos Basicos Não Realizados", "Média Geral + Desvio Padrão", "Média Geral", "Média Geral - Desvio Padrão"])

fig3.savefig(f"Numero_De_Atendimentos_Basicos_Nao_Realizados_{Environment.SPEED}_{Environment.BASICAS}")

mediaBasica = mean(numero_de_atendimentos_avancados_nao_comtemplados)
desvioPadroaBasico = stdev(numero_de_atendimentos_avancados_nao_comtemplados)
ax4.plot(range(0, simulacao), numero_de_atendimentos_avancados_nao_comtemplados, color="blue")
ax4.axhline(y=(mediaBasica + desvioPadroaBasico), xmin= 0, xmax=simulacao, color="red")
ax4.axhline(y=(mediaBasica), xmin= 0, xmax=simulacao, color="orange")
ax4.axhline(y=(mediaBasica - desvioPadroaBasico), xmin= 0, xmax=simulacao, color="black")
ax4.set_title("Número de Atendimentos Avançados Não Realizados")
ax4.set_ylabel("Número de Atendimentos Avançados Não Realizados")
ax4.set_xlabel("Execuções (Ciclos de Quinze Minutos)")
ax4.legend(["Número de Atendimentos Avançados Não Realizados", "Média Geral + Desvio Padrão", "Média Geral", "Média Geral - Desvio Padrão"])

fig4.savefig(f"Numero_De_Atendimentos_Avancados_Nao_Realizados_{Environment.SPEED}_{Environment.AVANCADAS}")

mediaBasica = mean(mediaDeDistanciaDosAtendimentosBasicos)
desvioPadroaBasico = stdev(mediaDeDistanciaDosAtendimentosBasicos)
ax5.plot(range(0, simulacao), mediaDeDistanciaDosAtendimentosBasicos, color="green")
ax5.axhline(y=(mediaBasica + desvioPadroaBasico), xmin= 0, xmax=simulacao, color="red")
ax5.axhline(y=(mediaBasica), xmin= 0, xmax=simulacao, color="orange")
ax5.axhline(y=(mediaBasica - desvioPadroaBasico), xmin= 0, xmax=simulacao, color="black")
ax5.set_title("Média das Distâncias dos Atendimentos Básicos (metros)")
ax5.set_ylabel("Média das Distâncias dos Atendimentos Básicos (metros)")
ax5.set_xlabel("Execuções (Ciclos de Quinze Minutos)")
ax5.legend(["Média das Distâncias dos Atendimentos Básicos", "Média Geral + Desvio Padrão", "Média Geral", "Média Geral - Desvio Padrão"])

fig5.savefig(f"Media_De_Distancias_Dos_Atendimentos_Basicos_{Environment.SPEED}_{Environment.BASICAS}")

mediaBasica = mean(mediaDeDistanciaDosAtendimentosAvancados)
desvioPadroaBasico = stdev(mediaDeDistanciaDosAtendimentosAvancados)
ax6.plot(range(0, simulacao), mediaDeDistanciaDosAtendimentosAvancados, color="blue")
ax6.axhline(y=(mediaBasica + desvioPadroaBasico), xmin= 0, xmax=simulacao, color="red")
ax6.axhline(y=(mediaBasica), xmin= 0, xmax=simulacao, color="orange")
ax6.axhline(y=(mediaBasica - desvioPadroaBasico), xmin= 0, xmax=simulacao, color="black")
ax6.set_title("Média das Distâncias dos Atendimentos Avançados (metros)")
ax6.set_ylabel("Média das Distâncias dos Atendimentos Avançados (metros)")
ax6.set_xlabel("Execuções (Ciclos de Quinze Minutos)")
ax6.legend(["Média das Distâncias dos Atendimentos Avançados", "Média Geral + Desvio Padrão", "Média Geral", "Média Geral - Desvio Padrão"])

fig6.savefig(f"Media_De_Distancias_Dos_Atendimentos_Avancados_{Environment.SPEED}_{Environment.AVANCADAS}")

mediaBasica = mean(ambulancias_avancadas_disponiveis_por_simulacao)
desvioPadroaBasico = stdev(ambulancias_avancadas_disponiveis_por_simulacao)
ax7.plot(range(0, simulacao), ambulancias_avancadas_disponiveis_por_simulacao, color="blue")
ax7.axhline(y=(mediaBasica + desvioPadroaBasico), xmin= 0, xmax=simulacao, color="red")
ax7.axhline(y=(mediaBasica), xmin= 0, xmax=simulacao, color="orange")
ax7.axhline(y=(mediaBasica - desvioPadroaBasico), xmin= 0, xmax=simulacao, color="black")
ax7.set_title("Número de Ambulâncias Avançadas Disponíveis")
ax7.set_ylabel("Número de Ambulâncias Avançadas Disponíveis")
ax7.set_xlabel("Execuções (Ciclos de Quinze Minutos)")
ax7.legend(["Número de Ambulâncias Avançadas Disponíveis", "Média Geral + Desvio Padrão", "Média Geral", "Média Geral - Desvio Padrão"])

fig7.savefig(f"Numero_De_Ambulancias_Avancadas_{Environment.SPEED}_{Environment.AVANCADAS}")

mediaBasica = mean(ambulancias_basicas_disponiveis_por_simulacao)
desvioPadroaBasico = stdev(ambulancias_basicas_disponiveis_por_simulacao)
ax8.plot(range(0, simulacao), ambulancias_basicas_disponiveis_por_simulacao, color="green")
ax8.axhline(y=(mediaBasica + desvioPadroaBasico), xmin= 0, xmax=simulacao, color="red")
ax8.axhline(y=(mediaBasica), xmin= 0, xmax=simulacao, color="orange")
ax8.axhline(y=(mediaBasica - desvioPadroaBasico), xmin= 0, xmax=simulacao, color="black")
ax8.set_title("Número de Ambulâncias Básicas Disponíveis")
ax8.set_ylabel("Número de Ambulâncias Básicas Disponíveis")
ax8.set_xlabel("Execuções (Ciclos de Quinze Minutos)")
ax8.legend(["Número de Ambulâncias Básicas Disponíveis", "Média Geral + Desvio Padrão", "Média Geral", "Média Geral - Desvio Padrão"])

fig8.savefig(f"Numero_De_Ambulancias_Basicas_{Environment.SPEED}_{Environment.BASICAS}")

plt.show()