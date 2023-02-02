import models

from models import (get_raw_data,
                    extrair_indicadores,
                    get_rpm,
                    listar_rpms)

import numpy as np
import pandas as pd
import os
import matplotlib.pyplot as plt
import time

start = time.time()
print(f'start: {start}')

ball_fault = models.ball_fault
cage_fault = models.cage_fault
outer_race = models.outer_race
inner_race = models.inner_race

PATH = models.PATH
sensores = models.sensores
ordens = 10

ordens = range(ordens)[1:ordens]

for ordem in ordens:
    # cont = 0++
    dataframe = []
    for sensor in sensores:
        for pasta in PATH: 
            
            coluna = sensores[sensor]

            arquivos = []
            arquivos = os.listdir(pasta)
            defeito = PATH[pasta]

            rpms = listar_rpms.ListaRPM(pasta).Get()

            for index in range(len(arquivos)):
                arquivo = arquivos[index]
                freq = [ball_fault,
                        cage_fault,
                        outer_race
                        ,inner_race]
                        
                sinal = get_raw_data.GetData(pasta,arquivo,coluna).Get()

                rpm_medio = rpms[index]

                for i in range(len(freq)):
                    freq[i] = freq[i]*rpm_medio


                Objeto_Extrair = extrair_indicadores.ExtrairIndicadores(pasta,
                                                                    arquivo,
                                                                    coluna,
                                                                    freq,
                                                                    rpm=rpm_medio,
                                                                    defeito=defeito,
                                                                    sensor=sensor)
                                                                
                dataframe.append(Objeto_Extrair.Get(ordem))
                # cont+=1
                # print(cont)

            end = time.time()
            elapsed_time = end - start
            elapsed_minutes = elapsed_time / 60

            print(f"Tempo de execução: {elapsed_minutes} minutos")
            print(f'pasta {pasta} concluída')

        end = time.time()
        elapsed_time = end - start
        elapsed_minutes = elapsed_time / 60

        df = pd.json_normalize(dataframe)
        df.to_csv(f'{models.path_dados_tratados}/ordens_{ordem}/dados_extraidos_{sensor}.csv')

        print(f"Tempo de execução: {elapsed_minutes} minutos")
        print(f'sensor {sensor} concluído')
        print(df)

    df = pd.json_normalize(dataframe)
    df.to_csv(f'{models.path_dados_tratados}/ordens_{ordem}/dados_extraidos_geral.csv')
    print(df)



    end = time.time()

    elapsed_time = end - start

    elapsed_minutes = elapsed_time / 60

    print("Tempo de execução: {:.2f} minutos".format(elapsed_minutes))

end = time.time()

elapsed_time = end - start

elapsed_minutes = elapsed_time / 60

print("Tempo de execução: {:.2f} minutos".format(elapsed_minutes))

breakpoint()

