import numpy as np
from solver import Solver
from atendimentos import Atendimentos
from ambulancias import Ambulancias
from typing import List, Dict, Tuple
from tqdm import tqdm
import random
from environment import Environment
import math
from statistics import stdev, mean
from AtendimentosGenerator import NumeroDeAtendimentosPorIntervaloDeTempo

import matplotlib.pyplot as plt

TEMPO_ATUAL = 0
DIAS = 30
CICLOS_DA_SIMULACAO = 96 * DIAS # (quantidade de ciclos de 15 minutos em x dias)
TEMPO_ENTRE_SIMULACOES = 15

class DESIGNATIONS_INDICATORS_TYPES:
    TempoDeEsperaMedioParaAtendimentosAvancados = 1 
    TempoDeEsperaMedioParaAtendimentosBasicos = 2
    NumeroDeAtendimentosBasicosNaoRealizados = 3
    NumeroDeAtendimentosAvancadosNaoRealizados = 4
    MediaDasDistanciasDosAtendimentosBasicos = 5
    MediaDasDistanciasDosAtendimentosAvancados = 6
    NumeroDeAmbulanciasAvancadasDisponiveis = 7
    NumeroDeAmbulanciasBasicasDisponiveis = 8
    

def filtrar_ambulancias_nao_impedidas(ambulancias: List[Dict[str, float]]):
    ambulanciasNaoImpedidas = []
    
    for ambulancia in ambulancias:
        if 'impedida' not in ambulancia or ambulancia.get('impedida') <= TEMPO_ATUAL:
            ambulanciasNaoImpedidas.append(ambulancia)
    
    return ambulanciasNaoImpedidas

def execute() -> Dict[int, Dict[str, float]]:
    todosOsAtendimentosAvancadosNaoRealizadosByUID : Dict[str, float] = {}
    todosOsAtendimentosBasicosNaoRealizadosByUID : Dict[str, float] = {}

    mediaDeTempoDeEsperaDeAtendimentosAvancados : List[float] = []
    mediaDeTempoDeEsperaDeAtendimentosBasicos : List[float] = []

    ambulancias_avancadas_disponiveis_por_simulacao = []
    ambulancias_basicas_disponiveis_por_simulacao = []

    numero_de_atendimentos_avancados_nao_comtemplados = []
    numero_de_atendimentos_basicos_nao_comtemplados = []

    mediaDeDistanciaDosAtendimentosBasicos = []
    mediaDeDistanciaDosAtendimentosAvancados = []


    atendimentosAvancadosNaoContemplados = []
    atendimentosBasicosNaoContemplados = []

    bases: List[Tuple[float,float]] = []
    bases.append([Environment.MAP_SIZE/2, Environment.MAP_SIZE/2 + Environment.MAP_SIZE*(math.sqrt(2)/4)])
    bases.append([Environment.MAP_SIZE/2 - Environment.MAP_SIZE*(math.sqrt(2)/4), Environment.MAP_SIZE/2 - Environment.MAP_SIZE*(math.sqrt(2)/4)])
    bases.append([Environment.MAP_SIZE/2 + Environment.MAP_SIZE*(math.sqrt(2)/4), Environment.MAP_SIZE/2 - Environment.MAP_SIZE*(math.sqrt(2)/4)])

    ambulanciasAvancadas: List[Dict[str, int]] = Ambulancias.generate(Environment.AVANCADAS, bases)
    ambulanciasBasicas: List[Dict[str, int]] = Ambulancias.generate(Environment.BASICAS, bases)

    simulacao = 0

    atendimentos_avancados_por_ciclo_de_tempo = NumeroDeAtendimentosPorIntervaloDeTempo.generate(80, DIAS)
    atendimentos_basicos_por_ciclo_de_tempo = NumeroDeAtendimentosPorIntervaloDeTempo.generate(400, DIAS)

    for ciclo_de_simulacao in tqdm(range(0, CICLOS_DA_SIMULACAO)):
        TEMPO_ATUAL = simulacao * TEMPO_ENTRE_SIMULACOES
        
        quantidade_de_novos_atendimentos_basicos = atendimentos_basicos_por_ciclo_de_tempo[ciclo_de_simulacao]
        quantidade_de_novos_atendimentos_avancados = atendimentos_avancados_por_ciclo_de_tempo[ciclo_de_simulacao]
        atendimentosAvancados: List[Dict[str, int]] = Atendimentos.generate(atendimentosAvancadosNaoContemplados, todosOsAtendimentosAvancadosNaoRealizadosByUID, quantidade_de_novos_atendimentos_avancados)
        atendimentosBasicos: List[Dict[str, int]] = Atendimentos.generate(atendimentosBasicosNaoContemplados, todosOsAtendimentosBasicosNaoRealizadosByUID, quantidade_de_novos_atendimentos_basicos)
        
        ambulanciasAvancadasNaoImpedidas = filtrar_ambulancias_nao_impedidas(ambulanciasAvancadas)
        ambulanciasBasicasNaoImpedidas = filtrar_ambulancias_nao_impedidas(ambulanciasBasicas)
        
        quantidade_de_ambulancias_avancadas = len(ambulanciasAvancadasNaoImpedidas)
        quantidade_de_atendimentos_avancados = len(atendimentosAvancados)

        quantidade_de_ambulancias_basicas = len(ambulanciasBasicasNaoImpedidas)
        quantidade_de_atendimentos_basicos = len(atendimentosBasicos)

        prioridade_ocorrencias_avancadas = []

        for i in range(quantidade_de_atendimentos_avancados):
            prioridade_ocorrencias_avancadas.append(atendimentosAvancados[i]["peso"])

        prioridade_ocorrencias_basicas = []

        for i in range(quantidade_de_atendimentos_basicos):
            prioridade_ocorrencias_basicas.append(atendimentosBasicos[i]["peso"])


        tempos_ambulancias_avancadas = []

        for i in range(quantidade_de_ambulancias_avancadas):
            tempos_ambulancias_avancadas.append([])
            for j in range(quantidade_de_atendimentos_avancados):
                posicao_ambulancia = np.array([ambulanciasAvancadasNaoImpedidas[i].get("x"), ambulanciasAvancadasNaoImpedidas[i].get("y")])
                posicao_atendimento = np.array([atendimentosAvancados[j].get("x"), atendimentosAvancados[j].get("y")])
                distancia_euclidiana = np.linalg.norm(posicao_ambulancia - posicao_atendimento)
                tempo = (distancia_euclidiana / Environment.AVERAGE_SPEED) + (60 * (random.random()))
                tempos_ambulancias_avancadas[i].append(tempo)

        tempos_ambulancias_basicas = []

        for i in range(quantidade_de_ambulancias_basicas):
            tempos_ambulancias_basicas.append([])
            for j in range(quantidade_de_atendimentos_basicos):
                posicao_ambulancia = np.array([ambulanciasBasicasNaoImpedidas[i].get("x"), ambulanciasBasicasNaoImpedidas[i].get("y")])
                posicao_atendimento = np.array([atendimentosBasicos[j].get("x"), atendimentosBasicos[j].get("y")])
                distancia_euclidiana = np.linalg.norm(posicao_ambulancia - posicao_atendimento)
                tempo = (distancia_euclidiana / Environment.AVERAGE_SPEED) + (30 * (random.random()))
                tempos_ambulancias_basicas[i].append(tempo)
                
                
        solucao = Solver.solve(prioridade_ocorrencias_avancadas, prioridade_ocorrencias_basicas, tempos_ambulancias_avancadas, tempos_ambulancias_basicas)


        for i in range(quantidade_de_ambulancias_avancadas):
            for j in range(quantidade_de_atendimentos_avancados):
                if solucao["avancados"][(i,j)]:
                    ambulanciasAvancadasNaoImpedidas[i]["impedida"] = TEMPO_ATUAL + tempos_ambulancias_avancadas[i][j]
        
        atendimentosAvancadosNaoContemplados = []
        distanciasAvancadasParciais = []
        for j in range(quantidade_de_atendimentos_avancados):
            atendido = False
            for i in range(quantidade_de_ambulancias_avancadas):
                if solucao["avancados"][(i,j)]:
                    atendido = True
                    posicao_ambulancia = np.array([ambulanciasAvancadasNaoImpedidas[i].get("x"), ambulanciasAvancadasNaoImpedidas[i].get("y")])
                    posicao_atendimento = np.array([atendimentosAvancados[j].get("x"), atendimentosAvancados[j].get("y")])
                    distancia_euclidiana = np.linalg.norm(posicao_ambulancia - posicao_atendimento)
                    distanciasAvancadasParciais.append(distancia_euclidiana) 
                    break
            
            if not atendido and (atendimentosAvancados[j]["id"] not in todosOsAtendimentosAvancadosNaoRealizadosByUID or
                                todosOsAtendimentosAvancadosNaoRealizadosByUID[atendimentosAvancados[j]["id"]] < 180):
                atendimentosAvancadosNaoContemplados.append(atendimentosAvancados[j])
                
                if atendimentosAvancados[j]["id"] not in todosOsAtendimentosAvancadosNaoRealizadosByUID:
                    todosOsAtendimentosAvancadosNaoRealizadosByUID[atendimentosAvancados[j]["id"]] = 0
            
                todosOsAtendimentosAvancadosNaoRealizadosByUID[atendimentosAvancados[j]["id"]] += TEMPO_ENTRE_SIMULACOES
            
            else:
                todosOsAtendimentosAvancadosNaoRealizadosByUID[atendimentosAvancados[j]["id"]] = 0
        
        res = 0
        for ele in ambulanciasAvancadas: 
            if 'impedida' not in ele or ele.get('impedida') <= TEMPO_ATUAL: 
                res = res + 1
        
        ambulancias_avancadas_disponiveis_por_simulacao.append(res)

        for i in range(quantidade_de_ambulancias_basicas):
            for j in range(quantidade_de_atendimentos_basicos):
                if solucao["basicos"][(i,j)]:
                    ambulanciasBasicasNaoImpedidas[i]["impedida"] = TEMPO_ATUAL + tempos_ambulancias_basicas[i][j]
        
        atendimentosBasicosNaoContemplados = []
        distanciasBasicasParciais = []
        for j in range(quantidade_de_atendimentos_basicos):
            atendido = False
            for i in range(quantidade_de_ambulancias_basicas):
                if solucao["basicos"][(i,j)]:
                    atendido = True
                    posicao_ambulancia = np.array([ambulanciasBasicasNaoImpedidas[i].get("x"), ambulanciasBasicasNaoImpedidas[i].get("y")])
                    posicao_atendimento = np.array([atendimentosBasicos[j].get("x"), atendimentosBasicos[j].get("y")])
                    distancia_euclidiana = np.linalg.norm(posicao_ambulancia - posicao_atendimento)
                    distanciasBasicasParciais.append(distancia_euclidiana) 
                    break
            
            if not atendido and (atendimentosBasicos[j]["id"] not in  todosOsAtendimentosBasicosNaoRealizadosByUID or
                    todosOsAtendimentosBasicosNaoRealizadosByUID[atendimentosBasicos[j]["id"]] <= 120):
                atendimentosBasicosNaoContemplados.append(atendimentosBasicos[j])
                
                if atendimentosBasicos[j]["id"] not in todosOsAtendimentosBasicosNaoRealizadosByUID:
                    todosOsAtendimentosBasicosNaoRealizadosByUID[atendimentosBasicos[j]["id"]] = 0
            
                todosOsAtendimentosBasicosNaoRealizadosByUID[atendimentosBasicos[j]["id"]] += TEMPO_ENTRE_SIMULACOES
            
            else:
                todosOsAtendimentosBasicosNaoRealizadosByUID[atendimentosBasicos[j]["id"]] = 0
                
                
        res = 0
        for ele in ambulanciasBasicas: 
            if 'impedida' not in ele or ele.get('impedida') <= TEMPO_ATUAL: 
                res = res + 1
        
        ambulancias_basicas_disponiveis_por_simulacao.append(res)
        
        numero_de_atendimentos_basicos_nao_comtemplados.append(len(atendimentosBasicosNaoContemplados))
        numero_de_atendimentos_avancados_nao_comtemplados.append(len(atendimentosAvancadosNaoContemplados))
        
        simulacao += 1
        
        media: float = 0
        q = 0
        for uid in todosOsAtendimentosAvancadosNaoRealizadosByUID:
            media += todosOsAtendimentosAvancadosNaoRealizadosByUID[uid]
            if todosOsAtendimentosAvancadosNaoRealizadosByUID[uid] > 0:
                q = q + 1
        
        media = media / (q or 1)        
        mediaDeTempoDeEsperaDeAtendimentosAvancados.append(media)
        
        media = 0
        q = 0
        for uid in todosOsAtendimentosBasicosNaoRealizadosByUID:
            media += todosOsAtendimentosBasicosNaoRealizadosByUID[uid]
            if todosOsAtendimentosBasicosNaoRealizadosByUID[uid] > 0:
                q = q + 1
        
        media = media / (q or 1)   
        mediaDeTempoDeEsperaDeAtendimentosBasicos.append(media)
        
        mediaDeDistanciaDosAtendimentosBasicos.append(mean(distanciasBasicasParciais or [0]))
        mediaDeDistanciaDosAtendimentosAvancados.append(mean(distanciasAvancadasParciais or [0]))
    
    indicadores = {}
    
    # Tempo de Espera Médio Para Atendimentos Avançados (minutos)
    indicadores[DESIGNATIONS_INDICATORS_TYPES.TempoDeEsperaMedioParaAtendimentosAvancados] = {}
    indicadores[DESIGNATIONS_INDICATORS_TYPES.TempoDeEsperaMedioParaAtendimentosAvancados]['label'] = 'Tempo de Espera Médio Para Atendimentos Avançados (minutos)'
    indicadores[DESIGNATIONS_INDICATORS_TYPES.TempoDeEsperaMedioParaAtendimentosAvancados]['mean'] = mean(mediaDeTempoDeEsperaDeAtendimentosAvancados)
    indicadores[DESIGNATIONS_INDICATORS_TYPES.TempoDeEsperaMedioParaAtendimentosAvancados]['std'] = stdev(mediaDeTempoDeEsperaDeAtendimentosAvancados)

    # Tempo de Espera Médio Para Atendimentos Básicos (minutos)
    indicadores[DESIGNATIONS_INDICATORS_TYPES.TempoDeEsperaMedioParaAtendimentosBasicos] = {}
    indicadores[DESIGNATIONS_INDICATORS_TYPES.TempoDeEsperaMedioParaAtendimentosBasicos]['mean'] = 'Tempo de Espera Médio Para Atendimentos Básicos (minutos)'
    indicadores[DESIGNATIONS_INDICATORS_TYPES.TempoDeEsperaMedioParaAtendimentosBasicos]['mean'] = mean(mediaDeTempoDeEsperaDeAtendimentosBasicos)
    indicadores[DESIGNATIONS_INDICATORS_TYPES.TempoDeEsperaMedioParaAtendimentosBasicos]['std'] = stdev(mediaDeTempoDeEsperaDeAtendimentosBasicos)

    # Número de Atendimentos Basicos Não Realizados
    indicadores[DESIGNATIONS_INDICATORS_TYPES.NumeroDeAtendimentosBasicosNaoRealizados] = {}
    indicadores[DESIGNATIONS_INDICATORS_TYPES.NumeroDeAtendimentosBasicosNaoRealizados]['label'] = 'Número de Atendimentos Basicos Não Realizados'
    indicadores[DESIGNATIONS_INDICATORS_TYPES.NumeroDeAtendimentosBasicosNaoRealizados]['mean'] = mean(numero_de_atendimentos_basicos_nao_comtemplados)
    indicadores[DESIGNATIONS_INDICATORS_TYPES.NumeroDeAtendimentosBasicosNaoRealizados]['std'] = stdev(numero_de_atendimentos_basicos_nao_comtemplados)

    # Número de Atendimentos Avançados Não Realizados
    indicadores[DESIGNATIONS_INDICATORS_TYPES.NumeroDeAtendimentosAvancadosNaoRealizados] = {}
    indicadores[DESIGNATIONS_INDICATORS_TYPES.NumeroDeAtendimentosAvancadosNaoRealizados]['label'] = 'Número de Atendimentos Avançados Não Realizados'
    indicadores[DESIGNATIONS_INDICATORS_TYPES.NumeroDeAtendimentosAvancadosNaoRealizados]['mean'] = mean(numero_de_atendimentos_avancados_nao_comtemplados)
    indicadores[DESIGNATIONS_INDICATORS_TYPES.NumeroDeAtendimentosAvancadosNaoRealizados]['std'] = stdev(numero_de_atendimentos_avancados_nao_comtemplados)
    
    # Média das Distâncias dos Atendimentos Básicos (metros)
    indicadores[DESIGNATIONS_INDICATORS_TYPES.MediaDasDistanciasDosAtendimentosBasicos] = {}
    indicadores[DESIGNATIONS_INDICATORS_TYPES.MediaDasDistanciasDosAtendimentosBasicos]['label'] = 'Média das Distâncias dos Atendimentos Básicos (metros)'
    indicadores[DESIGNATIONS_INDICATORS_TYPES.MediaDasDistanciasDosAtendimentosBasicos]['mean'] = mean(mediaDeDistanciaDosAtendimentosBasicos)
    indicadores[DESIGNATIONS_INDICATORS_TYPES.MediaDasDistanciasDosAtendimentosBasicos]['std'] = stdev(mediaDeDistanciaDosAtendimentosBasicos)
    
    # Média das Distâncias dos Atendimentos Avançados (metros)
    indicadores[DESIGNATIONS_INDICATORS_TYPES.MediaDasDistanciasDosAtendimentosAvancados] = {}
    indicadores[DESIGNATIONS_INDICATORS_TYPES.MediaDasDistanciasDosAtendimentosAvancados]['label'] = 'Média das Distâncias dos Atendimentos Avançados (metros)'
    indicadores[DESIGNATIONS_INDICATORS_TYPES.MediaDasDistanciasDosAtendimentosAvancados]['mean'] = mean(mediaDeDistanciaDosAtendimentosAvancados)
    indicadores[DESIGNATIONS_INDICATORS_TYPES.MediaDasDistanciasDosAtendimentosAvancados]['std'] = stdev(mediaDeDistanciaDosAtendimentosAvancados)

    # Número de Ambulâncias Avançadas Disponíveis
    indicadores[DESIGNATIONS_INDICATORS_TYPES.NumeroDeAmbulanciasAvancadasDisponiveis] = {}
    indicadores[DESIGNATIONS_INDICATORS_TYPES.NumeroDeAmbulanciasAvancadasDisponiveis]['label'] = 'Número de Ambulâncias Avançadas Disponíveis'
    indicadores[DESIGNATIONS_INDICATORS_TYPES.NumeroDeAmbulanciasAvancadasDisponiveis]['mean'] = mean(ambulancias_avancadas_disponiveis_por_simulacao)
    indicadores[DESIGNATIONS_INDICATORS_TYPES.NumeroDeAmbulanciasAvancadasDisponiveis]['std'] = stdev(ambulancias_avancadas_disponiveis_por_simulacao)

    # Número de Ambulâncias Básicas Disponíveis
    indicadores[DESIGNATIONS_INDICATORS_TYPES.NumeroDeAmbulanciasBasicasDisponiveis] = {}
    indicadores[DESIGNATIONS_INDICATORS_TYPES.NumeroDeAmbulanciasBasicasDisponiveis]['label'] = 'Número de Ambulâncias Básicas Disponíveis'
    indicadores[DESIGNATIONS_INDICATORS_TYPES.NumeroDeAmbulanciasBasicasDisponiveis]['mean'] = mean(ambulancias_basicas_disponiveis_por_simulacao)
    indicadores[DESIGNATIONS_INDICATORS_TYPES.NumeroDeAmbulanciasBasicasDisponiveis]['std'] = stdev(ambulancias_basicas_disponiveis_por_simulacao)
    
    return indicadores    

print(execute())