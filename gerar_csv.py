import models

from models import (get_raw_data,
                    extrair_indicadores,
                    get_rpm)

import numpy as np
import pandas as pd
import os
import matplotlib.pyplot as plt
import time

start = time.time()
print(f'start: {start}')

dataframe = []
ball_fault = 1.8710
cage_fault = 0.3750
outer_race = 2.9980
inner_race = 5.0020

PATH = {'database/dados_brutos/normal':'normal',

           'database/dados_brutos/horizontal-misalignment/0.5mm':'desalinhamento_horizontal_baixo',
           'database/dados_brutos/horizontal-misalignment/1.0mm':'desalinhamento_horizontal_médio',
           'database/dados_brutos/horizontal-misalignment/1.5mm':'desalinhamento_horizontal_alto',
           'database/dados_brutos/horizontal-misalignment/2.0mm':'desalinhamento_horizontal_alto',
           
           'database/dados_brutos/imbalance/6g':'desbalanceamento_baixo',
           'database/dados_brutos/imbalance/10g':'desbalanceamento_baixo',
           'database/dados_brutos/imbalance/15g':'desbalanceamento_medio',
           'database/dados_brutos/imbalance/20g':'desbalanceamento_medio',
           'database/dados_brutos/imbalance/25g':'desbalanceamento_alto',
           'database/dados_brutos/imbalance/30g':'desbalanceamento_alto',
           'database/dados_brutos/imbalance/35g':'desbalanceamento_alto',
           
           'database/dados_brutos/overhang/ball_fault/0g':'ball_fault_baixo',
           'database/dados_brutos/overhang/ball_fault/6g':'ball_fault_medio',
           'database/dados_brutos/overhang/ball_fault/20g':'ball_fault_alto',
           'database/dados_brutos/overhang/ball_fault/35g':'ball_fault_alto',

           'database/dados_brutos/overhang/cage_fault/0g':'cage_fault_baixo',
           'database/dados_brutos/overhang/cage_fault/6g':'cage_fault_medio',
           'database/dados_brutos/overhang/cage_fault/20g':'cage_fault_alto',
           'database/dados_brutos/overhang/cage_fault/35g':'cage_fault_alto',

           'database/dados_brutos/overhang/outer_race/0g':'outer_race_baixo',
           'database/dados_brutos/overhang/outer_race/6g':'outer_race_medio',
           'database/dados_brutos/overhang/outer_race/20g':'outer_race_alto',
           'database/dados_brutos/overhang/outer_race/35g':'outer_race_alto',
           
           'database/dados_brutos/underhang/ball_fault/0g':'ball_fault_baixo',
           'database/dados_brutos/underhang/ball_fault/6g':'ball_fault_medio',
           'database/dados_brutos/underhang/ball_fault/20g':'ball_fault_alto',
           'database/dados_brutos/underhang/ball_fault/35g':'ball_fault_alto',

           'database/dados_brutos/underhang/cage_fault/0g':'cage_fault_baixo',
           'database/dados_brutos/underhang/cage_fault/6g':'cage_fault_medio',
           'database/dados_brutos/underhang/cage_fault/20g':'cage_fault_alto',
           'database/dados_brutos/underhang/cage_fault/35g':'cage_fault_alto',

           'database/dados_brutos/underhang/outer_race/0g':'outer_race_baixo',
           'database/dados_brutos/underhang/outer_race/6g':'outer_race_medio',
           'database/dados_brutos/underhang/outer_race/20g':'outer_race_alto',
           'database/dados_brutos/underhang/outer_race/35g':'outer_race_alto',

           }

sensores = {
            # 'rotacao':0,

            'rolamento_interno_axial':1,
            'rolamento_interno_radial1':2,
            'rolamento_interno_radial2':3,
            
            'rolamento_externo_axial':4,
            'rolamento_externo_radial1':5,
            'rolamento_externo_radial2':6,
            
            # 'microfone':7
            }

cont = 0
for sensor in sensores:
    for pasta in PATH: 

        coluna = sensores[sensor]

        arquivos = []
        arquivos = os.listdir(pasta)
        defeito = PATH[pasta]

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
                                                                defeito=defeito,
                                                                sensor=sensor)
                                                            
            dataframe.append(Objeto_Extrair.Get())
            cont+=1
            print(cont)

        end = time.time()
        elapsed_time = end - start
        elapsed_minutes = elapsed_time / 60

        print(f"Tempo de execução: {elapsed_minutes} minutos")
        print(f'pasta {pasta} concluída')

    end = time.time()
    elapsed_time = end - start
    elapsed_minutes = elapsed_time / 60

    df = pd.json_normalize(dataframe)
    df.to_csv(f'{models.path_dados_tratados}/dados_extraidos_{sensor}.csv')

    print(f"Tempo de execução: {elapsed_minutes} minutos")
    print(f'sensor {sensor} concluído')
    print(df)

df = pd.json_normalize(dataframe)
df.to_csv(f'{models.path_dados_tratados}/dados_extraidos_geral.csv')
print(df)



end = time.time()

elapsed_time = end - start

elapsed_minutes = elapsed_time / 60

print("Tempo de execução: {:.2f} minutos".format(elapsed_minutes))

breakpoint()

