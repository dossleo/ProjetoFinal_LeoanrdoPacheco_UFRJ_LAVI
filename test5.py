import models

from models import (get_raw_data,
                    extrair_indicadores,
                    get_rpm)

import numpy as np
import pandas as pd
import os
import matplotlib.pyplot as plt

dataframe = []
for pasta in models.PATH:
    arquivos = os.listdir(pasta)

    ball_fault = 1.8710
    cage_fault = 0.3750
    outer_race = 2.9980
    inner_race = 5.0020

    frequencias_rolamento = [ball_fault,
                            cage_fault,
                            outer_race
                            ,inner_race]

    for sensor in models.sensores:
        coluna = models.sensores[sensor]

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
            Objeto_Extrair = extrair_indicadores.ExtrairIndicadores(pasta,
                                                                arquivo,
                                                                1,
                                                                freq,
                                                                defeito=models.PATH[pasta],
                                                                sensor=sensor)
                                                            

            dataframe.append(Objeto_Extrair.Get())
            arquivos = []
    
df = pd.json_normalize(dataframe)
df.to_csv(f'{models.path_dados_tratados}/dados_extraidos.csv')
print(df)
breakpoint()

