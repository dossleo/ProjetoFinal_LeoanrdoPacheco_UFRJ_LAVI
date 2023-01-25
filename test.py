import models
from models import indicadores_frequencia, indicadores_tempo, get_raw_data, extrair_indicadores, filtro_passa_baixa
import os
import pandas as pd
import numpy as np

from sklearn.preprocessing import MinMaxScaler

import matplotlib.pyplot as plt

#Path
pasta = models.PATH_1ST_DATABASE
lista_arquivos = os.listdir(pasta)

# Setup de variáveis
rotacao_da_maquina = models.rotacao_hz
freq_passa_baixa = models.rotacao_hz*2
ordem_filtro = 5
rpm = models.rpm
frequencia_de_aquisicao = models.freq_sample
ordens_frequencia = 5

# Criando o Dataframe
dataframe = []

rolamento = 0

frequencia_de_referencia = models.fault_frequency

for arquivo in lista_arquivos:
    sinal = get_raw_data.GetData(pasta,arquivo,rolamento).Get()
    Filtro = filtro_passa_baixa.LowPassFilter(sinal,cutoff=freq_passa_baixa,order=2)
    sinal_filtrado = Filtro.lowpass_filter()

    Objeto_Extrair = extrair_indicadores.ExtrairIndicadores(sinal_filtrado,frequencia_de_referencia,2)
    dataframe.append(Objeto_Extrair.Get(ordens_frequencia))

dataframe = pd.json_normalize(dataframe)
df_num = dataframe.select_dtypes(include=[np.number])

# Instanciando o Scaler
scaler = MinMaxScaler()

# Aplicando a normalização
df_scaled = scaler.fit_transform(df_num)

# Atualizando o DataFrame original
df_num = pd.DataFrame(df_scaled, columns=df_num.columns)

print(df_num)

plt.plot(range(len(df_num['rms'])),df_num['rms'])

