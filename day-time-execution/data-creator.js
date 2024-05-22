const fs = require('fs');


const criarAmbulancia = (id, axisX, axisY) => ({
    id,
    axisX,
    axisY,
    disponivelEm: Date().toString()
});


const data = {
    avancadas: [],
    basicas: []
};


for (i = 0; i < 6; i++)
    data.avancadas.push(criarAmbulancia(i, 10, 10))

for (i = 0; i < 21; i++)
    data.basicas.push(criarAmbulancia(i, 10, 10))

fs.writeFileSync('./day-time-execution/ambulancias.json', JSON.stringify(data), 'utf8');