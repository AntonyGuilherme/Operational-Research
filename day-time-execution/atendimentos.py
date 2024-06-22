from typing import Dict, List
from numpy import random
from environment import Environment

class Atendimentos:
    
    @staticmethod
    def generate(atendimentosNaoRealizados: List[Dict[str, int]] = [], max: int = 3) -> List[Dict[str, int]]:
        atendimentos = []
        pesos = [1,1,2,3,5,8,13,21,34,55]
        
        for atendimento in atendimentosNaoRealizados:
            atendimentos.append(atendimento)
        
        quantidade = random.randint(0, max)
        for _ in range(quantidade):
            atendimentos.append({
                "x": random.randint(0, Environment.MAP_SIZE),
                "y": random.randint(0, Environment.MAP_SIZE),
                "peso": pesos[random.randint(0, 10)]
            })
        
        return atendimentos
        
        
        
    