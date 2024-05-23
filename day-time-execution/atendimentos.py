from typing import Dict, List
from numpy import random

class Atendimentos:
    
    @staticmethod
    def generate(atendimentosNaoRealizados: List[Dict[str, int]] = []) -> List[Dict[str, int]]:
        atendimentos = []
        pesos = [1,1,2,3,5,8,13,21,34,55]
        
        for atendimento in atendimentosNaoRealizados:
            atendimentos.append(atendimento)
        
        quantidade = random.randint(0, 3)
        for _ in range(quantidade):
            atendimentos.append({
                "x": random.randint(0, 10),
                "y": random.randint(0, 10),
                "peso": pesos[random.randint(0, 10)]
            })
        
        return atendimentos
        
        
        
    