import numpy as np
import matplotlib.pyplot as plt

class NumeroDeAtendimentosPorIntervaloDeTempo: 
    @staticmethod
    def generate(total_ocorrencias:int) :

        # Definindo os parâmetros das distribuições normais
        mean_1 = 8 * 4   # Média da primeira distribuição (8 horas) em intervalos de 15 minutos
        mean_2 = 18 * 4  # Média da segunda distribuição (18 horas) em intervalos de 15 minutos
        std_dev = 2 * 4  # Desvio padrão, ajustável conforme necessário, em intervalos de 15 minutos

        # Criando um array de 96 intervalos de 15 minutos (24 horas * 4)
        intervalos = np.arange(96)

        # Calculando as distribuições normais
        dist_1 = np.exp(-(intervalos - mean_1)**2 / (2 * std_dev**2))
        dist_2 = np.exp(-(intervalos - mean_2)**2 / (2 * std_dev**2))

        # Combinando as distribuições
        combined_dist = dist_1 + dist_2

        # Normalizando a distribuição combinada
        normalized_dist = combined_dist / np.sum(combined_dist)

        # Gerando as ocorrências com base na distribuição normalizada
        ocorrencias_por_intervalo = np.random.choice(intervalos, size=total_ocorrencias, p=normalized_dist)

        # Contando as ocorrências por intervalo de 15 minutos
        contagem_ocorrencias, _ = np.histogram(ocorrencias_por_intervalo, bins=np.arange(97))
        
        return contagem_ocorrencias


contagem_ocorrencias = NumeroDeAtendimentosPorIntervaloDeTempo.generate(300)

# Exibindo o histograma
plt.figure(figsize=(15, 5))
plt.bar(np.arange(96), contagem_ocorrencias, width=0.8, align='center')
plt.xlabel('Intervalo de 15 minutos ao longo do dia')
plt.ylabel('Número de ocorrências')
plt.title('Distribuição de Ocorrências ao Longo do Dia')
plt.xticks(np.arange(0, 96, 4))
plt.grid(True)
plt.show()

# Imprimindo a contagem de ocorrências por intervalo de 15 minutos
for i in range(96):
    hora = i // 4
    minuto = (i % 4) * 15
    print(f"{hora:02d}:{minuto:02d} - {contagem_ocorrencias[i]} ocorrências")