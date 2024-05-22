import gurobipy as gp
from gurobipy import GRB
from typing import List, Dict, Tuple

class Solver:
    @staticmethod
    def solve(prioridade_ocorrencias_avancadas: List[int], 
              prioridade_ocorrencias_basicas: List[int],
              tempos_ambulancias_avancadas: List[List[int]],
              tempos_ambulancias_basicas: List[List[int]]
              ):
        
        quantidade_de_ambulancias_avancadas = len(tempos_ambulancias_avancadas)
        quantidade_de_ambulancias_basicas = len(tempos_ambulancias_basicas)
        
        quantidade_de_atendimentos_avancados = len(tempos_ambulancias_avancadas[0])
        quantidade_de_atendimentos_basicos = len(tempos_ambulancias_basicas[0])
        
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

        model.addConstrs( gp.quicksum(x[i, j] for i in range(quantidade_de_ambulancias_avancadas)) <= 1 for j in range(quantidade_de_atendimentos_avancados) )

        model.addConstrs( gp.quicksum(x[i, j] for j in range(quantidade_de_atendimentos_avancados)) <= 1 for i in range(quantidade_de_ambulancias_avancadas) )

        model.addConstrs( gp.quicksum(y[k, l] for k in range(quantidade_de_ambulancias_basicas)) <= 1 for l in range(quantidade_de_atendimentos_basicos) )

        model.addConstrs( gp.quicksum(y[k, l] for l in range(quantidade_de_atendimentos_basicos)) <= 1 for k in range(quantidade_de_ambulancias_basicas) )

        for i in range(quantidade_de_ambulancias_avancadas):
            for j in range(quantidade_de_atendimentos_avancados):
                 model.addConstr((x[i,j] * tempos_ambulancias_avancadas[i][j]) <= 30)

        for k in range(quantidade_de_ambulancias_basicas):
            for l in range(quantidade_de_atendimentos_basicos):
                model.addConstr((y[k, l] * tempos_ambulancias_basicas[k][l]) <= 120)
                
        model.setParam(GRB.Param.OutputFlag, 0)
        model.optimize()
        
        solution: Dict[str, Dict[Tuple[int, int], bool]] = { 'avancados': {}, 'basicos': {}  }

        for i in range(quantidade_de_ambulancias_avancadas):
            for j in range(quantidade_de_atendimentos_avancados):
                solution['avancados'][(i,j)] = x[i, j].X >= 1
                 
        for i in range(quantidade_de_ambulancias_basicas):
            for j in range(quantidade_de_atendimentos_basicos):
                solution['basicos'][(i,j)] = y[i, j].X >= 1          
        
        return solution