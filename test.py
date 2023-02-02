import models
from models import indicadores_frequencia, indicadores_tempo, get_raw_data, extrair_indicadores, filtro_passa_baixa, get_rpm
import os
import pandas as pd
import numpy as np

from sklearn.preprocessing import MinMaxScaler

import matplotlib.pyplot as plt

#Path
pasta = 'database/dados_brutos/normal'
lista_arquivos = os.listdir(pasta)


# Criando o Dataframe
dataframe = []

coluna = 1

frequencia_de_referencia = models.frequencias_rolamento

for arquivo in lista_arquivos:
    # Setup de variáveis
    sinal = get_raw_data.GetData(pasta,arquivo,coluna).Get()
    sinal_rotacao = get_raw_data.GetData(pasta,arquivo,0).Get()
    rotacao_da_maquina = get_rpm.GetRPM(sinal_rotacao).get_rpm_medio()
    freq_passa_baixa = rotacao_da_maquina*2
    ordem_filtro = 5
    rpm = rotacao_da_maquina
    frequencia_de_aquisicao = models.freq_aquisicao
    ordens_frequencia = 5

    Objeto_Extrair = extrair_indicadores.ExtrairIndicadores(pasta,arquivo,coluna,frequencia_de_referencia)
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

for defeito in models.defeito_rolamento:
    plt.plot(range(len(df_num[defeito])),df_num[defeito])
    plt.title(defeito)
    plt.show()

breakpoint()
