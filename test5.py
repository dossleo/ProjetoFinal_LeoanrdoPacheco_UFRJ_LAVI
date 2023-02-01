import models
from models import get_raw_data, extrair_indicadores, indicadores_frequencia, get_rpm, filtro_passa_baixa
import numpy as np
import pandas as pd
import os
import matplotlib.pyplot as plt

pasta = 'database/normal'
coluna = 1
arquivos = os.listdir(pasta)
dataframe = []

ball_fault = 1.8710
cage_fault = 0.3750
outer_race = 2.9980
inner_race = 5.0020

frequencias_rolamento = [ball_fault,
                        cage_fault,
                        outer_race
                        ,inner_race]

for arquivo in arquivos:
    freq = [ball_fault,
            cage_fault,
            outer_race
            ,inner_race]
            
    sinal = get_raw_data.GetData(pasta,arquivo,coluna).Get()
    sinal_rpm = get_raw_data.GetData(pasta,arquivo,0).Get()

    rpm = get_rpm.GetRPM(sinal_rpm).get_rpm_medio()

    for i in range(len(freq)):
        freq[i] = freq[i]*rpm
    # print(f'rpm {rpm} - frequencias {freq}')
    Objeto_Extrair = extrair_indicadores.ExtrairIndicadores(pasta,
                                                        arquivo,
                                                        1,
                                                        freq)
                                                    

    dataframe.append(Objeto_Extrair.Get())
    
df = pd.json_normalize(dataframe)

print(df)
breakpoint()

