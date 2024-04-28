import matplotlib.pyplot as plt
from statistics import variance
import json
from typing import Dict, List
import numpy as np



with open("sequencial.json") as prioridades_selecionadas:
    dados: Dict[int, List[int]] = json.load(prioridades_selecionadas)
    
    # data to plot
    n = 10
    
    media = []
    variancia = []
    
    for prioridade in dados:
        
        media_ = 0
        for p in dados[prioridade]:
            media_ += p
        
        media_ /= dados[prioridade].__len__()
        media.append(np.average(dados[prioridade]))
        variancia.append(np.var(dados[prioridade]))

    # create plot
    fig, ax = plt.subplots()
    index = np.arange(n)

    bar_width = 0.35
    opacity = 0.8

    bar_A = plt.bar(index, media, bar_width, alpha=opacity, color='r', label='Média')
    bar_B = plt.bar(index + bar_width, variancia, bar_width, alpha=opacity, color='y', label='Variância')

    plt.xlabel('Prioridades')
    plt.ylabel('Valores')
    plt.title('Prioridades Selecionadas')
    plt.xticks(index + bar_width, ('1', '2', '3', '4', '5', '6', '7', '8', '9', '10'))
    plt.legend()

    plt.show()
