import models

from models import (
                    extrair_indicadores,
                    listar_rpms
                    )

import numpy as np
import pandas as pd
import os

import time
import datetime

class GerarCSV():
    def __init__(self,
                ordem_inicial=1,
                ordem_final=1,
                qtd_sensores_extraidos_na_pasta = 0,
                nome_padrao_de_arquivo=models.nome_padrao_de_arquivo
                ) -> None:

        self.PATH = models.PATH
        self.numero_de_pastas = len(self.PATH)
        self.nome_padrao_de_arquivo = nome_padrao_de_arquivo

        self.ball_fault = models.ball_fault
        self.cage_fault = models.cage_fault
        self.outer_race = models.outer_race
        self.inner_race = models.inner_race

        self.no_ordens = ordem_final
        self.ordem_final = ordem_final # Precisa ser >= 1
        self.ordem_inicial = ordem_inicial # Precisa ser >=1 e <= self.no_ordens
        self.no_ordens = range(self.no_ordens)[self.ordem_inicial:self.no_ordens]


        self.sensores = models.sensores
        self.sensor_inicial = qtd_sensores_extraidos_na_pasta
        self.lista_sensores = list(self.sensores)[self.sensor_inicial:len(self.sensores)]
        self.ciclo_atual = 0
        self.ciclos_totais = self.Calcula_Ciclos_Totais()

        
    def run(self):
        self.start = time.time()
        now = datetime.datetime.now()
        now = now.strftime("%d/%m/%Y - %H:%M:%S")

        print(f'___________________________\nInício: {now}\n')

        for ordem in self.no_ordens:
            self.dataframe_temp = []

        # Hierarquia para percorrer tudo

        # for ordem in self.no_ordens
            self.Percorrer_Sensores(ordem)
                # self.Percorrer_Pastas(ordem,sensor)
                    # self.Percorrer_Arquivos(ordem,sensor,pasta)

            self.ConcatenaCSV(ordem=ordem)

            self.lista_sensores = list(self.sensores)

            print(f'\nOrdem n° {ordem} concluída!')
            self.Tempo_Decorrido()

        print('Dados Extraídos com sucesso!!!')
        self.Tempo_Decorrido()

    def Percorrer_Sensores(self,ordem):
        for sensor in self.lista_sensores:
            self.cont = 0

    # Hierarquia para percorrer tudo

    # for ordem in self.no_ordens
        # self.Percorrer_Sensores(ordem)
            self.Percorrer_Pastas(ordem,sensor)
                # self.Percorrer_Arquivos(ordem,sensor,pasta)


            df_temp = pd.json_normalize(self.dataframe_temp)
            df_temp.to_csv(f'{models.path_dados_tratados}/ordens_{ordem}/{self.nome_padrao_de_arquivo}_{sensor}.csv')
            self.dataframe_temp = []

            print(df_temp)
            
            self.Tempo_Decorrido()            
            print(f'Sensor: {sensor} - concluído\n___________________________\n')

    def Percorrer_Pastas(self,ordem,sensor):
        for pasta in self.PATH: 
            self.coluna = self.sensores[sensor]

            self.arquivos = []
            self.arquivos = os.listdir(pasta)
            
            self.defeito = self.PATH[pasta]

            self.rpms = listar_rpms.ListaRPM(pasta).Get()

# Hierarquia para percorrer tudo

# for ordem in self.no_ordens
    # self.Percorrer_Sensores(ordem)
        # self.Percorrer_Pastas(ordem,sensor)
            self.Percorrer_Arquivos(ordem,sensor,pasta)

            self.cont+=1
            self.ciclo_atual+=1
            
            print(f'Ordem: {ordem}\nSensor: {sensor}\nPastas Percorridas: {self.cont}/{self.numero_de_pastas}\nAndamento Total: {np.round(100*self.ciclo_atual/self.ciclos_totais,2)}%')
            self.Tempo_Decorrido()            
            print(f'Pasta concluída: {pasta}\n')

    def Percorrer_Arquivos(self,ordem,sensor,pasta):
        for index in range(len(self.arquivos)):
            arquivo = self.arquivos[index]
            freq = [self.ball_fault,
                    self.cage_fault,
                    self.outer_race
                    ,self.inner_race]
                    
            rpm_medio = self.rpms[index]

            for i in range(len(freq)):
                freq[i] = freq[i]*rpm_medio


            Objeto_Extrair = extrair_indicadores.ExtrairIndicadores(
                                                                    pasta           =pasta,
                                                                    arquivo         =arquivo,
                                                                    coluna          =self.coluna,
                                                                    freq_referencia =freq,
                                                                    rpm             =rpm_medio,
                                                                    defeito         =self.defeito,
                                                                    sensor          =sensor
                                                                    )

            dados = Objeto_Extrair.Get(ordem)   
            self.dataframe_temp.append(dados)

            dados = 0

    def ConcatenaCSV(self,ordem):
        # Lista dos nomes dos arquivos CSV
        pasta = f'{models.path_dados_tratados}/ordens_{ordem}'
        arquivos = os.listdir(pasta)

        # Lê cada arquivo CSV, considerando a primeira linha como cabeçalho e a primeira coluna como ID
        dfs = [pd.read_csv(f'{pasta}/{arquivo}', header=0, index_col=0) for arquivo in arquivos]

        # Concatena todos os DataFrames em um único DataFrame
        result = pd.concat(dfs)

        # Salva o resultado em um arquivo CSV único
        result.to_csv(f'{pasta}/{self.nome_padrao_de_arquivo}_geral.csv')

    def Tempo_Decorrido(self):
        elapsed_time = time.time() - self.start

        tempo_estimado = elapsed_time*((self.ciclos_totais/self.ciclo_atual)-1)

        print("Tempo decorrido: {:02}:{:02}:{:02}".format(int(elapsed_time // 3600), int(elapsed_time % 3600 // 60), int(elapsed_time % 60)))
        print("Tempo Estimado até o Fim: {:02}:{:02}:{:02}".format(int(tempo_estimado // 3600), int(tempo_estimado % 3600 // 60), int(tempo_estimado % 60)))
    
    def Calcula_Ciclos_Totais(self):

        cont = 0
        sensor_inicial = self.sensor_inicial
        lista_sensores = list(self.sensores)[sensor_inicial:len(self.sensores)]
        for ordem in self.no_ordens:
            for sensor in range(len(lista_sensores)):
                for pasta in self.PATH: 
                    cont+=1
            lista_sensores = list(self.sensores)

        return cont
    
class RunCSV():
    def __init__(self,total_de_ordens=1) -> None:
        ordem_final = total_de_ordens
        ordens = []
        for i in range(ordem_final):
            ordens.append(f'ordens_{i+1}')
            
        for ordem in ordens:
            pasta = f'{models.path_dados_tratados}/{ordem}'
            num_arquivos = len(os.listdir(pasta))
            if num_arquivos <7:
                ordem_inicial = int(ordem.split("_")[1])
                break
            else:
                ordem_inicial = ordem_final

        qtd_sensores_extraidos_na_pasta = len(os.listdir(f'{models.path_dados_tratados}/ordens_{ordem_inicial}'))

        self.Objeto_GerarCSV = GerarCSV(
                                    ordem_inicial=int(ordem_inicial),
                                    ordem_final=int(ordem_final),
                                    qtd_sensores_extraidos_na_pasta=int(qtd_sensores_extraidos_na_pasta)
                                    )

    def Run(self):
        self.Objeto_GerarCSV.run()