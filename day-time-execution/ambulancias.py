from typing import Dict, List
from numpy import random

class Ambulancias:
    
    @staticmethod
    def generate(quantidade) -> List[Dict[str, str]]:
        ambulancias = []
        
        for _ in range(quantidade):
            ambulancias.append({
                "x": random.randint(0, 100),
                "y": random.randint(0, 100)
            })
        
        return ambulancias
        
        
        
    