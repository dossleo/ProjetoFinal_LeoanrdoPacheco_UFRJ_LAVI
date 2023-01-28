import models
import os
import pandas as pd
from models import get_raw_data
import matplotlib.pyplot as plt
import numpy as np


pasta = f'database/{models.testes[0]}/{models.defeitos_desalinhamento_horizontal[0]}'

arquivos = os.listdir(pasta)

sinal = get_raw_data.GetData(pasta,arquivos[0],0)
sinal = sinal.Get()

frequencia_aquisicao = models.freq_aquisicao
n_points = len(sinal)

t_total = n_points/frequencia_aquisicao

vetor_tempo = np.linspace(0,t_total,n_points)

plt.plot(vetor_tempo,sinal)
plt.show()
