import models
from models import get_raw_data, extrair_indicadores
import numpy as np
import pandas as pd
import os
import matplotlib.pyplot as plt

pasta = 'database/normal'
coluna = 1
arquivos = os.listdir(pasta)
frequencia_de_referencia = models.frequencias_rolamento
dataframe = []
ordens_frequencia = 5
largura_banda = 1

for arquivo in arquivos:
    sinal = get_raw_data.GetData(pasta,arquivo,coluna)
    sinal = sinal.Get()
    Objeto_Extrair = extrair_indicadores.ExtrairIndicadores(pasta,
                                                            arquivo,
                                                            coluna,
                                                            frequencia_de_referencia)

    dataframe.append(Objeto_Extrair.Get(ordens_frequencia))

dataframe = pd.json_normalize(dataframe)
print(dataframe)
breakpoint()