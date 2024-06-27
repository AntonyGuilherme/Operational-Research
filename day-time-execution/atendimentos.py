from typing import Dict, List
from numpy import random
from environment import Environment
import uuid

class Atendimentos:
    
    @staticmethod
    def generate(atendimentosNaoRealizados: List[Dict[str, int]] = [], todosOsAtendimentosNaoRealizadosByUID: Dict[str, float] = {}, quantidade: int = 1) -> List[Dict[str, int]]:
        atendimentos = []
        pesos = [1,1,2,3,5,8,13,21,34,55]
        
        for atendimento in atendimentosNaoRealizados:
            atendimento["peso"] += todosOsAtendimentosNaoRealizadosByUID[atendimento["id"]]
            atendimentos.append(atendimento)
        
        for _ in range(quantidade):
            atendimentos.append({
                "id": str(uuid.uuid4()),
                "x": random.randint(0, Environment.MAP_SIZE),
                "y": random.randint(0, Environment.MAP_SIZE),
                "peso": pesos[random.randint(0, 10)]
            })
        
        return atendimentos
        
        
        
    