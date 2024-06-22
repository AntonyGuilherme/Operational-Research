from typing import Dict, List, Tuple


class Ambulancias:
    
    @staticmethod
    def generate(quantidade, bases: List[Tuple[int, int]]) -> List[Dict[str, str]]:
        ambulancias = []
        quantidadeDeBases = len(bases)
        
        for baseIndex in range(quantidadeDeBases):
            for _ in range((int) (quantidade / quantidadeDeBases)):
                ambulancias.append({
                    "x": bases[baseIndex][0],
                    "y": bases[baseIndex][1]
                })
        
        return ambulancias
        
        
        
    