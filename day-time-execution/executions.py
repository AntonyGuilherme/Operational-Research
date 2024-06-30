from environment import Environment
from designacao_mensal import execute
import json

# 1. Quantas vezes um atendimento básico / urgente deixou de ser atendido - done
# 2. Qual é a média de tempo que um chamado urgente leva para ser atendido? - done
# 3. Qual o número médio de USB/USA's disponíveis por passo de tempo? - done
# 4. Qual a média da distância que uma unidade está de um chamado atribuído? - done

# Experimentos
# variar a quantidade de ambulâncias e velocidade
# Velocidade    | Ambulâncias Avançadas     | Ambulâncias Básicas | Done

# 30km/h        | 6                         | 21                    | X
# 50km/h        | 6                         | 21                    | 
# 70km/h        | 6                         | 21                    | 

# 50km/h        | 3                         | 14                    | 
# 50km/h        | 6                         | 21                    | 
# 50km/h        | 9                         | 28                    |

experiments = [
    [30, 6, 21],
    [50, 6, 21],
    [70, 6, 21],
    [50, 3, 14],
    [50, 6, 21],
    [50, 9, 28]
]

for experiment in experiments:
    Environment.SPEED = experiment[0]
    Environment.AVANCADAS = experiment[1]
    Environment.BASICAS = experiment[2]
    
    experimento = execute()
    
    with open(f"EXPERIMENTO_{experiment[0]}_{experiment[1]}_{experiment[2]}.json", "w") as arquivo:
        json.dump(experimento, arquivo)
    
