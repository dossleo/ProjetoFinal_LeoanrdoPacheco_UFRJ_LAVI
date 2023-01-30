import models
import os
import pandas as pd
from models import get_raw_data, get_rpm
import matplotlib.pyplot as plt
import numpy as np


pasta = 'database/normal'

arquivos = os.listdir(pasta)

tamanho = 150000

sinal = get_raw_data.GetData(pasta,arquivos[0],0)
sinal = sinal.Get()
# sinal = pd.json_normalize(sinal)


frequencia_aquisicao = models.freq_aquisicao
n_points = len(sinal)

t_total = n_points/frequencia_aquisicao

vetor_tempo = np.linspace(0,t_total,n_points)

plt.plot(vetor_tempo,sinal)
# plt.axis('off')
plt.show()

rpm = get_rpm.GetRPM(sinal,frequencia_aquisicao)
rpm_medio = rpm.get_rpm_medio()
print(rpm_medio)
rpm.plot_picos()
rpm.plot_rpm()

print(rpm)


breakpoint()
