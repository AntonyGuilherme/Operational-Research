import matplotlib.pyplot as plt
from typing import Dict, List
import random

coordenates: List[Dict[str,int]] = []

for x in range(0, 3):
    coordenates.append({ 'x': random.randint(0, 100), 'y': random.randint(0, 100) })


fig = plt.figure()

x_list, y_list = [], []
for city in coordenates:
    x_list.append(city['x'])
    y_list.append(city['y'])

plt.plot(x_list, y_list, 'ro', color="blue")
plt.show(block=True)