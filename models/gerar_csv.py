import models

from models import (get_raw_data,
                    extrair_indicadores,
                    listar_rpms)

import numpy as np
import pandas as pd
import os

import time
import datetime

class GerarCSV():
    def __init__(self,sensor_inicial = 0,no_ordens=1,ordem_inicial=1) -> None:


        self.PATH = models.PATH

        self.ball_fault = models.ball_fault
        self.cage_fault = models.cage_fault
        self.outer_race = models.outer_race
        self.inner_race = models.inner_race

        self.no_ordens = no_ordens # Precisa ser >= 1
        self.ordem_inicial = ordem_inicial # Precisa ser >=1 e <= self.no_ordens
        self.no_ordens = range(self.no_ordens)[self.ordem_inicial:self.no_ordens]


        self.sensores = models.sensores
        self.sensor_inicial = sensor_inicial
        self.lista_sensores = list(self.sensores)[self.sensor_inicial:-1]

    def run(self):

        self.start = time.time()
        print(f'___________________________\nstart: {datetime.datetime.now()}\n')

        for ordem in self.no_ordens:
            # cont = 0++
            dataframe = []
            dataframe_temp = []
            for sensor in self.lista_sensores:
                cont = 0
                for pasta in self.PATH: 
                    
                    coluna = self.sensores[sensor]

                    arquivos = []
                    arquivos = os.listdir(pasta)
                    defeito = self.PATH[pasta]

                    rpms = listar_rpms.ListaRPM(pasta).Get()

                    for index in range(len(arquivos)):
                        arquivo = arquivos[index]
                        freq = [self.ball_fault,
                                self.cage_fault,
                                self.outer_race
                                ,self.inner_race]
                                
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

                        dados = Objeto_Extrair.Get(ordem)   
                        dataframe.append(dados)
                        dataframe_temp.append(dados)

                        dados = 0

                    end = time.time()
                    elapsed_time = end - self.start
                    elapsed_minutes = elapsed_time / 60

                    cont+=1
                    porcentagem = np.round(100*cont/len(arquivos),2)
                    print(f'Ordem: {ordem}\nSensor: {sensor}\nAndamento: {porcentagem}%')

                    print('Tempo de execução: {:.2f} minutos'.format(elapsed_minutes))
                    print(f'Pasta concluída!: {pasta}\n')

                end = time.time()
                elapsed_time = end - self.start
                elapsed_minutes = elapsed_time / 60

                df_temp = pd.json_normalize(dataframe_temp)
                df_temp.to_csv(f'{models.path_dados_tratados}/ordens_{ordem}/dados_extraidos_{sensor}.csv')
                dataframe_temp = []

                print(df_temp)
                print('\nTempo de execução: {:.2f} minutos'.format(elapsed_minutes))
                print(f'Sensor: {sensor} - concluído\n___________________________\n')

            df = pd.json_normalize(dataframe)
            df.to_csv(f'{models.path_dados_tratados}/ordens_{ordem}/dados_extraidos_geral.csv')
            print(df)

            self.lista_sensores = list(self.sensores)

            end = time.time()
            elapsed_time = end - self.start
            elapsed_minutes = elapsed_time / 60

            print(f'\nOrdem n° {ordem} concluída!')
            print('Tempo de execução: {:.2f} minutos'.format(elapsed_minutes))

        end = time.time()

        elapsed_time = end - self.start

        elapsed_minutes = elapsed_time / 60

        print('Dados Extraídos com sucesso!!!')
        print('Tempo de execução TOTAL: {:.2f} minutos'.format(elapsed_minutes))

