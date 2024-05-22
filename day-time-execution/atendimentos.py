from typing import Dict, List
from numpy import random

class Atendimentos:
    
    @staticmethod
    def generate(atendimentosNaoRealizados: List[Dict[str, int]] = []) -> List[Dict[str, int]]:
        atendimentos = []
        pesos = [1,1,2,3,5,8,13,21,34,55]
        
        for atendimento in atendimentosNaoRealizados:
            atendimentos.append(atendimento)
        
        quantidade = random.randint(0, 25)
        for _ in range(quantidade):
            atendimentos.append({
                "axisX": random.randint(0, 100),
                "axisY": random.randint(0, 100),
                "peso": pesos[random.randint(0, 10)]
            })
        
        return atendimentos
        
        
        
    