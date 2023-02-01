import models
import os
import pandas as pd
from models import get_raw_data, get_rpm
import matplotlib.pyplot as plt
import numpy as np


pasta = 'database/dados_brutos/normal'

arquivos = os.listdir(pasta)
rpms = []
frequencia_aquisicao = models.freq_aquisicao

for i in range(len(arquivos)):
    sinal = get_raw_data.GetData(pasta,arquivos[i],models.colunas['rotacao'])
    sinal = sinal.Get()
    # sinal = pd.json_normalize(sinal)


    n_points = len(sinal)

    t_total = n_points/frequencia_aquisicao

    vetor_tempo = np.linspace(0,t_total,n_points)

    rpm = get_rpm.GetRPM(sinal,frequencia_aquisicao)
    rpm_medio = rpm.get_rpm_medio('rpm')
    
    rpms.append(rpm_medio)

plt.plot(range(len(rpms)),rpms)
plt.grid(True)
plt.show()

breakpoint()