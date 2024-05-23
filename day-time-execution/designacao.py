import numpy as np
from solver import Solver
from atendimentos import Atendimentos
from ambulancias import Ambulancias
from typing import List, Dict
import datetime

TIME = 0

# modulo que recebe o resultado do solver + a nova entrada e entrega de volta para o solver
# prepara os dados de um dia de operação
# desconsiderar as ambulâncias em atendimentos
# plotar a solução graficamente

# adicicionar o cálculo de tempo levando em duração a distância - done
# adicionar a duração do atendimento - done

# adicionar o ciclo de atendimento durante o dia
# adicionar o gráfico por ciclo
# adicionar o nome as ambulâncias
# adicionar o nome aos pacientes das emergências

atendimentosAvancados: List[Dict[str, int]] = Atendimentos.generate()
atendimentosBasicos: List[Dict[str, int]] = Atendimentos.generate()

ambulanciasAvancadas: List[Dict[str, int]] = Ambulancias.generate(6)
ambulanciasBasicas: List[Dict[str, int]] = Ambulancias.generate(21)


quantidade_de_ambulancias_avancadas = len(ambulanciasAvancadas)
quantidade_de_atendimentos_avancados = len(atendimentosAvancados)

quantidade_de_ambulancias_basicas = len(ambulanciasBasicas)
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
        posicao_ambulancia = np.array([ambulanciasAvancadas[i].get("x"), ambulanciasAvancadas[i].get("y")])
        posicao_atendimento = np.array([atendimentosAvancados[j].get("x"), atendimentosAvancados[j].get("y")])
        distancia_euclidiana = np.linalg.norm(posicao_ambulancia - posicao_atendimento)
        tempo = distancia_euclidiana * (1 + np.random.rand())
        tempos_ambulancias_avancadas[i].append(tempo)

tempos_ambulancias_basicas = []

for i in range(quantidade_de_ambulancias_basicas):
    tempos_ambulancias_basicas.append([])
    for j in range(quantidade_de_atendimentos_basicos):
        posicao_ambulancia = np.array([ambulanciasBasicas[i].get("x"), ambulanciasBasicas[i].get("y")])
        posicao_atendimento = np.array([atendimentosBasicos[j].get("x"), atendimentosBasicos[j].get("y")])
        distancia_euclidiana = np.linalg.norm(posicao_ambulancia - posicao_atendimento)
        tempo = distancia_euclidiana * (1 + np.random.rand())
        tempos_ambulancias_basicas[i].append(tempo)
        
        
solucao = Solver.solve(prioridade_ocorrencias_avancadas, prioridade_ocorrencias_basicas, tempos_ambulancias_avancadas, tempos_ambulancias_basicas)


for i in range(quantidade_de_ambulancias_avancadas):
    for j in range(quantidade_de_atendimentos_avancados):
        if solucao["avancados"][(i,j)]:
            ambulanciasAvancadas[i]["impedida"] = TIME + tempos_ambulancias_avancadas[i][j]

for i in range(quantidade_de_ambulancias_basicas):
    for j in range(quantidade_de_atendimentos_basicos):
        if solucao["basicos"][(i,j)]:
            ambulanciasBasicas[i]["impedida"] = TIME + tempos_ambulancias_basicas[i][j]


print(ambulanciasBasicas)
print(ambulanciasAvancadas)   