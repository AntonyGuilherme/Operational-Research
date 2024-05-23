import numpy as np
from solver import Solver
from atendimentos import Atendimentos
from ambulancias import Ambulancias
from typing import List, Dict
from tqdm import tqdm

import matplotlib.pyplot as plt

TEMPO_ATUAL = 0
CICLOS_DA_SIMULACAO = 288

# modulo que recebe o resultado do solver + a nova entrada e entrega de volta para o solver
# prepara os dados de um dia de operação
# desconsiderar as ambulâncias em atendimentos
# plotar a solução graficamente

# adicicionar o cálculo de tempo levando em duração a distância - done
# adicionar a duração do atendimento - done

# adicionar o ciclo de atendimento durante o dia
    # adicionar o ciclo - done
    # adicionar a remoção das ambulâncias impedidas - done
    # adicionar o mecanismo de reaproveitamento de atendimentos - done
    
# adicionar o gráfico por ciclo
 # adicionar gráficos de ambulâncias disponíveis
# adicionar o nome as ambulâncias
# adicionar o nome aos pacientes das emergências

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

ambulanciasAvancadas: List[Dict[str, int]] = Ambulancias.generate(6)
ambulanciasBasicas: List[Dict[str, int]] = Ambulancias.generate(21)

simulacao = 0

for _ in tqdm(range(0, CICLOS_DA_SIMULACAO)):
    TEMPO_ATUAL = simulacao * 5
    atendimentosAvancados: List[Dict[str, int]] = Atendimentos.generate(atendimentosAvancadosNaoContemplados)
    atendimentosBasicos: List[Dict[str, int]] = Atendimentos.generate(atendimentosBasicosNaoContemplados)
    
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
            tempo = distancia_euclidiana * (1 + np.random.rand())
            tempos_ambulancias_avancadas[i].append(tempo)

    tempos_ambulancias_basicas = []

    for i in range(quantidade_de_ambulancias_basicas):
        tempos_ambulancias_basicas.append([])
        for j in range(quantidade_de_atendimentos_basicos):
            posicao_ambulancia = np.array([ambulanciasBasicasNaoImpedidas[i].get("x"), ambulanciasBasicasNaoImpedidas[i].get("y")])
            posicao_atendimento = np.array([atendimentosBasicos[j].get("x"), atendimentosBasicos[j].get("y")])
            distancia_euclidiana = np.linalg.norm(posicao_ambulancia - posicao_atendimento)
            tempo = distancia_euclidiana * (1 + np.random.rand())
            tempos_ambulancias_basicas[i].append(tempo)
            
            
    solucao = Solver.solve(prioridade_ocorrencias_avancadas, prioridade_ocorrencias_basicas, tempos_ambulancias_avancadas, tempos_ambulancias_basicas)


    for i in range(quantidade_de_ambulancias_avancadas):
        for j in range(quantidade_de_atendimentos_avancados):
            if solucao["avancados"][(i,j)]:
                ambulanciasAvancadasNaoImpedidas[i]["impedida"] = TEMPO_ATUAL + tempos_ambulancias_avancadas[i][j]
    
    atendimentosAvancadosNaoContemplados = []
    for j in range(quantidade_de_atendimentos_avancados):
        for i in range(quantidade_de_ambulancias_avancadas):
            if solucao["avancados"][(i,j)]:
                atendimentosAvancadosNaoContemplados.append(atendimentosAvancados[j])
                break
    
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
        for i in range(quantidade_de_ambulancias_basicas):
            if solucao["basicos"][(i,j)]:
                atendimentosBasicosNaoContemplados.append(atendimentosBasicos[j])
    
    res = 0
    for ele in ambulanciasBasicas: 
        if 'impedida' not in ele or ele.get('impedida') <= TEMPO_ATUAL: 
            res = res + 1
    
    ambulancias_basicas_disponiveis_por_simulacao.append(res)
    
    
    porcentagem_de_atendimentos_basicos.append(100 * (len(atendimentosBasicosNaoContemplados)/ (len(atendimentosBasicos) or 1)))
    porcentagem_de_atendimentos_avancados.append(100 * (len(atendimentosAvancadosNaoContemplados) / (len(atendimentosAvancados) or 1)))
    
    simulacao += 1
    

fig, ax = plt.subplots()
fig, ax2 = plt.subplots()

fig, ax3 = plt.subplots()
fig, ax4 = plt.subplots()

ax.plot(range(0, simulacao), ambulancias_avancadas_disponiveis_por_simulacao, color="blue")
ax.set_title("Ambulâncias Avançadas Disponíveis")
ax.set_ylabel("Número de Ambulâncias Avançadas")
ax.set_xlabel("Simulações")

ax2.plot(range(0, simulacao), ambulancias_basicas_disponiveis_por_simulacao, color="green")
ax2.set_title("Ambulâncias Básicas Disponíveis")
ax2.set_ylabel("Número de Básicas Avançadas")
ax2.set_xlabel("Simulações")

ax3.plot(range(0, simulacao), porcentagem_de_atendimentos_avancados, color="blue")
ax3.set_title("Porcentagem de Atendimentos Avançados Não Realizados")
ax3.set_ylabel("Porcentagem de Atendimentos Avançados")
ax3.set_xlabel("Simulações")

ax4.plot(range(0, simulacao), porcentagem_de_atendimentos_basicos, color="green")
ax4.set_title("Porcentagem de Atendimentos Básicos Não Realizados")
ax4.set_ylabel("Porcentagem de Atendimentos Básicos")
ax4.set_xlabel("Simulações")

plt.show()
    # print(ambulanciasBasicas)
    # print(ambulanciasAvancadas)   
    