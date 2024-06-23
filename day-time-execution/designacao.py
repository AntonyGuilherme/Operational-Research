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
QUNATIDADE_DE_DIAS = 30
CICLOS_DA_SIMULACAO = 288 * QUNATIDADE_DE_DIAS # (quantidade de ciclos de 5 minutos em x dias)
TEMPO_ENTRE_SIMULACOES = 5

# definir uma velocidade média para todas as ambulâncias (57km/h) - done
# definir a escala do mapa (20km por 20km) - done

# tempo médio de atendimento - done
# variância - done

# Experimentos
# variar a quantidade de ambulâncias e velocidade
# Velocidade    | Ambulâncias Avançadas     | Ambulâncias Avançadas
# 50km/h        | 6                         | 21

todosOsAtendimentosAvancadosNaoRealizadosByUID : Dict[str, float] = {}
todosOsAtendimentosBasicosNaoRealizadosByUID : Dict[str, float] = {}

mediaDeTempoDeEsperaDeAtendimentosAvancados : List[float] = []
mediaDeTempoDeEsperaDeAtendimentosBasicos : List[float] = []

ambulancias_avancadas_disponiveis_por_simulacao = []
ambulancias_basicas_disponiveis_por_simulacao = []

porcentagem_de_atendimentos_avancados = []
porcentagem_de_atendimentos_basicos = []

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

ambulanciasAvancadas: List[Dict[str, int]] = Ambulancias.generate(6, bases)
ambulanciasBasicas: List[Dict[str, int]] = Ambulancias.generate(21, bases)

simulacao = 0

for _ in tqdm(range(0, CICLOS_DA_SIMULACAO)):
    TEMPO_ATUAL = simulacao * TEMPO_ENTRE_SIMULACOES
    atendimentosAvancados: List[Dict[str, int]] = Atendimentos.generate(atendimentosAvancadosNaoContemplados, todosOsAtendimentosAvancadosNaoRealizadosByUID, max = 2)
    atendimentosBasicos: List[Dict[str, int]] = Atendimentos.generate(atendimentosBasicosNaoContemplados, todosOsAtendimentosBasicosNaoRealizadosByUID, max = 6)
    
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
    for j in range(quantidade_de_atendimentos_avancados):
        atendido = False
        for i in range(quantidade_de_ambulancias_avancadas):
            if solucao["avancados"][(i,j)]:
                atendido = True
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
    for j in range(quantidade_de_atendimentos_basicos):
        atendido = False
        for i in range(quantidade_de_ambulancias_basicas):
            if solucao["basicos"][(i,j)]:
                atendido = True
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
    
    porcentagem_de_atendimentos_basicos.append(100 * (len(atendimentosBasicosNaoContemplados)/ (len(atendimentosBasicos) or 1)))
    porcentagem_de_atendimentos_avancados.append(100 * (len(atendimentosAvancadosNaoContemplados) / (len(atendimentosAvancados) or 1)))
    
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
    
fig, ax = plt.subplots()
fig, ax2 = plt.subplots()

fig, ax3 = plt.subplots()
fig, ax4 = plt.subplots()

fig, ax5 = plt.subplots()
fig, ax6 = plt.subplots()

mediaAvancada = mean(mediaDeTempoDeEsperaDeAtendimentosAvancados)
desvioPadraoAvancado = stdev(mediaDeTempoDeEsperaDeAtendimentosAvancados)
ax.plot(range(0, simulacao), mediaDeTempoDeEsperaDeAtendimentosAvancados, color="blue")
ax.axhline(y=(mediaAvancada + desvioPadraoAvancado), xmin= 0, xmax=simulacao, color="red")
ax.axhline(y=mediaAvancada, xmin= 0, xmax=simulacao, color="orange")
ax.axhline(y=(mediaAvancada - desvioPadraoAvancado), xmin= 0, xmax=simulacao, color="black")
ax.set_title("Tempo de Espera Médio Para Atendimentos Avançados (minutos)")
ax.set_ylabel("Tempo em Minutos")
ax.set_xlabel("Execuções (Ciclos de Cinco Minutos)")
ax.legend(["Média ao Longo das Execuções", "Média Geral + Desvio Padrão", "Média Geral", "Média Geral - Desvio Padrão"])

mediaBasica = mean(mediaDeTempoDeEsperaDeAtendimentosBasicos)
desvioPadroaBasico = stdev(mediaDeTempoDeEsperaDeAtendimentosBasicos)
ax2.plot(range(0, simulacao), mediaDeTempoDeEsperaDeAtendimentosBasicos, color="green")
ax2.axhline(y=(mediaBasica + desvioPadroaBasico), xmin= 0, xmax=simulacao, color="red")
ax2.axhline(y=(mediaBasica), xmin= 0, xmax=simulacao, color="orange")
ax2.axhline(y=(mediaBasica - desvioPadroaBasico), xmin= 0, xmax=simulacao, color="black")
ax2.set_title("Tempo de Espera Médio Para Atendimentos Básicos (minutos)")
ax2.set_ylabel("Tempo em Minutos")
ax2.set_xlabel("Execuções (Ciclos de Cinco Minutos)")
ax2.legend(["Média ao Longo das Execuções", "Média Geral + Desvio Padrão", "Média Geral", "Média Geral - Desvio Padrão"])

ax3.plot(range(0, simulacao), ambulancias_avancadas_disponiveis_por_simulacao, color="blue")
ax3.set_title("Ambulâncias Avançadas Disponíveis")
ax3.set_ylabel("Número de Ambulâncias Avançadas")
ax3.set_xlabel("Execuções (Ciclos de Cinco Minutos)")

ax4.plot(range(0, simulacao), ambulancias_basicas_disponiveis_por_simulacao, color="green")
ax4.set_title("Ambulâncias Básicas Disponíveis")
ax4.set_ylabel("Número de Básicas Avançadas")
ax4.set_xlabel("Execuções (Ciclos de Cinco Minutos)")

ax5.plot(range(0, simulacao), porcentagem_de_atendimentos_avancados, color="blue")
ax5.set_title("Porcentagem de Atendimentos Avançados Não Realizados")
ax5.set_ylabel("Porcentagem de Atendimentos Avançados")
ax5.set_xlabel("Execuções (Ciclos de Cinco Minutos)")

ax6.plot(range(0, simulacao), porcentagem_de_atendimentos_basicos, color="green")
ax6.set_title("Porcentagem de Atendimentos Básicos Não Realizados")
ax6.set_ylabel("Porcentagem de Atendimentos Básicos")
ax6.set_xlabel("Execuções (Ciclos de Cinco Minutos)")

plt.show()