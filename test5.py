import models
from models import get_raw_data
import os
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

pasta = 'database/dados_tratados/ordens_1'
arquivos = os.listdir(pasta)
arquivo = arquivos[0]
coluna = 1

sinal = get_raw_data.GetData(pasta,arquivo,coluna).GetDataframe()
print(sinal)

rms = sinal['rms']

plt.plot(range(len(rms)),rms)
plt.show()

df_normal = sinal[sinal["defeito"] == "ball_fault_alto"]
rms = df_normal['rms']

plt.plot(range(len(rms)),rms)
plt.show()