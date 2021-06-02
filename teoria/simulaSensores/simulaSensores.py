'''
    NOME        Fabio de Moura Camargo Neto
    CURSO       Engenharia de Software
    SIGLA       GES
    NÚM.        22
'''

# ----------------------------------------------------------

# Imports ...

import threading    # Biblioteca p/ Threads
import time         # Controle de tempo
import random       # Números aleatórios

# Conexão c/ o MongoDB => Importar o "pymongo"
from pymongo import MongoClient

# ----------------------------------------------------------

# 1. Conexão c/ o MongoDB
client = MongoClient('mongodb://localhost:27017')

# 2. Acessando um banco (database) específico
db = client['bancoiot']

# 3. Acessando uma collection do banco
sensors = db.sensores

# ----------------------------------------------------------

# Projetando as Threads ...


def simulateTemp(num, sensor, interval):
    temp = random.randint(30, 40)
    # Criando o documento
    document = {
        "nomeSensor": sensor,
        "valorSensor": temp,
        "unidadeMedida": "C",
        "sensorAlarmado": False
    }
    # Inserindo o documento
    insertion = sensors.insert_one(document)
    if insertion.acknowledged:
        print('Sensor', num, 'criado!')
    else:
        print('Erro ao criar sensor', num, '!')
    while temp <= 38:
        temp = random.randint(30, 40)
        update_temp = sensors.update_one(
            {"nomeSensor": sensor},
            {"$set": {"valorSensor": temp}}
        )
        if update_temp.acknowledged:
            print('Temperatura', num, 'atualizada!')
        else:
            print('Erro ao atualizar temperatura', num, '!')
        time.sleep(interval)
    update_alarm = sensors.update_one(
        {"nomeSensor": sensor},
        {"$set": {"sensorAlarmado": True}}
    )
    if update_alarm.acknowledged:
        print('Alarme', num, 'atualizado!')
    else:
        print('Erro ao atualizar alarme', num, '!')
    print('Atenção! Temperatura muito alta! Verificar Sensor', num, '!')

# ----------------------------------------------------------

# Deletando caso dê chabu (sdds Rosanna) ...


deletion = sensors.delete_many(
    {"nomeSensor": {"$exists": True}}
)

if deletion.acknowledged:
    print('Cachê limpo, chefe!')
else:
    print('Moiô!')

# ----------------------------------------------------------

# Criando as Threads ...

# Tempo em segundos
time_value = 5

x = threading.Thread(target=simulateTemp, args=(1, 'Temp1', time_value))
x.start()

y = threading.Thread(target=simulateTemp, args=(2, 'Temp2', time_value))
y.start()

z = threading.Thread(target=simulateTemp, args=(3, 'Temp3', time_value))
z.start()
