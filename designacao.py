import gurobipy as gp
from gurobipy import GRB
import numpy as np

# comparação das prioridades por fibannaci e por geração aleatórios
# os itens com maior peso são menos ou mais atendidos?
# como a complexidade do problema altera o tempo de execução do algoritmo?

quantidade_de_ambulancias_avancadas = 100
quantidade_de_atendimentos_avancados = 100

quantidade_de_ambulancias_basicas = 1000
quantidade_de_atendimentos_basicos = 1000

prioridade_ocorrencias_avancadas = []

for i in range(quantidade_de_atendimentos_avancados):
    prioridade_ocorrencias_avancadas.append(np.random.randint(5, 10))

prioridade_ocorrencias_basicas = []

for i in range(quantidade_de_atendimentos_basicos):
    prioridade_ocorrencias_basicas.append(np.random.randint(1, 5))


tempos_ambulancias_avancadas = []

for i in range(quantidade_de_ambulancias_avancadas):
    tempos_ambulancias_avancadas.append([])
    for j in range(quantidade_de_atendimentos_avancados):
        tempos_ambulancias_avancadas[i].append(np.random.randint(12, 100))

tempos_ambulancias_basicas = []

for i in range(quantidade_de_ambulancias_basicas):
    tempos_ambulancias_basicas.append([])
    for j in range(quantidade_de_atendimentos_basicos):
        tempos_ambulancias_basicas[i].append(np.random.randint(12, 100))
    

model = gp.Model()

# adicionando as variáveis de decisão
x = model.addVars(quantidade_de_ambulancias_avancadas, quantidade_de_atendimentos_avancados, vtype=GRB.BINARY)
y = model.addVars(quantidade_de_ambulancias_basicas, quantidade_de_atendimentos_basicos, vtype=GRB.BINARY)

#função objetivo
model.setObjective(
            gp.quicksum(
                prioridade_ocorrencias_avancadas[j] * x[i, j] 
                    for i in range(quantidade_de_ambulancias_avancadas) 
                    for j in range(quantidade_de_atendimentos_avancados)
            ) 
            + 
            gp.quicksum(
                prioridade_ocorrencias_basicas[l] * y[k, l] 
                    for k in range(quantidade_de_ambulancias_basicas) 
                    for l in range(quantidade_de_atendimentos_basicos)
            ), 
            sense = GRB.MAXIMIZE)

c1 = model.addConstrs( gp.quicksum(x[i, j] for i in range(quantidade_de_ambulancias_avancadas)) <= 1 for j in range(quantidade_de_atendimentos_avancados) )

c2 = model.addConstrs( gp.quicksum(x[i, j] for j in range(quantidade_de_atendimentos_avancados)) <= 1 for i in range(quantidade_de_ambulancias_avancadas) )

c3 = model.addConstrs( gp.quicksum(y[k, l] for k in range(quantidade_de_ambulancias_basicas)) <= 1 for l in range(quantidade_de_atendimentos_basicos) )

c4 = model.addConstrs( gp.quicksum(y[k, l] for l in range(quantidade_de_atendimentos_basicos)) <= 1 for k in range(quantidade_de_ambulancias_basicas) )

for i in range(quantidade_de_ambulancias_avancadas):
    for j in range(quantidade_de_atendimentos_avancados):
        model.addConstr((x[i,j] * tempos_ambulancias_avancadas[i][j]) <= 30)

for k in range(quantidade_de_ambulancias_basicas):
    for l in range(quantidade_de_atendimentos_basicos):
        model.addConstr((y[k, l] * tempos_ambulancias_basicas[k][l]) <= 120)

model.setParam(GRB.Param.OutputFlag, 0)

model.optimize()

print(model.objVal)

print("Avancada")
for eq in range(quantidade_de_ambulancias_avancadas):
    for pj in range(quantidade_de_atendimentos_avancados):
        if x[eq, pj].X >= 1:
            print(f"{eq} => {pj}")

print("Basica")            
for eq in range(quantidade_de_ambulancias_basicas):
    for pj in range(quantidade_de_atendimentos_basicos):
        if y[eq, pj].X >= 1:
            print(f"{eq} => {pj}")