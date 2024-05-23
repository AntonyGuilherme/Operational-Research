import numpy as np
from solver import Solver
from atendimentos import Atendimentos
from ambulancias import Ambulancias
from typing import List, Dict

TEMPO_ATUAL = 0
CICLOS_DA_SIMULACAO = 10

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
# adicionar o nome as ambulâncias
# adicionar o nome aos pacientes das emergências


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

for simulacao in range(0, CICLOS_DA_SIMULACAO):
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
    
    print(f"ambulancias avançadas disponiveis {res}")  

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
    
    print(f"ambulancias básicas disponiveis {res}")  


    # print(ambulanciasBasicas)
    # print(ambulanciasAvancadas)   