import datetime
import os
import time

import numpy as np
import pandas as pd
from rich import pretty, print

import models
from models import extrair_indicadores, get_rpm

pretty.install()



class GeneralFuncions():

    def listar_arquivos(self, pasta:str) -> list:
        arquivos = os.listdir(pasta)
        return arquivos

    def ler_dataframe(self, pasta, arquivo):
        caminho = os.path.join(pasta,arquivo)
        columns = [0,1,2,3,4,5,6,7]
        return pd.read_csv(caminho, sep=',', names=columns, header=None)

    def extrair_coluna(self, dataframe:pd.DataFrame, n_coluna:int):
        return np.array(dataframe[n_coluna])

    def iniciar_contagem(self):
        start = time.time()
        now = datetime.datetime.now()
        now = now.strftime("%d/%m/%Y - %H:%M:%S")

        print(f'___________________________\nInício: {now}\n')
        return start

    def tempo_decorrido(self, start, ciclo_atual, ciclos_totais,ordem,cont):
            elapsed_time = time.time() - start
            if ciclo_atual > 0:
                tempo_estimado = elapsed_time*((ciclos_totais/ciclo_atual)-1)
            else:
                tempo_estimado = 0
            
            print(f'\nOrdem: {ordem}\nPastas Percorridas: {cont}/{len(models.PATH)}\nAndamento Total: {np.round(100*ciclo_atual/ciclos_totais,2)}%')
            print("Tempo decorrido: {:02}:{:02}:{:02}".format(int(elapsed_time // 3600), int(elapsed_time % 3600 // 60), int(elapsed_time % 60)))
            print("Tempo Estimado até o Fim: {:02}:{:02}:{:02}".format(int(tempo_estimado // 3600), int(tempo_estimado % 3600 // 60), int(tempo_estimado % 60)))

class GerarCSV(GeneralFuncions):
    
    PASTAS = models.PATH
    SENSORES = models.sensores
    FREQUENCIAS_REF = models.frequencias_rolamento
    COLUNA_RPM = 0
    COLUNA_CONFERE_RPM = 2

    def __init__(self, ordem_inicial:int, ordem_final:int) -> None:
        self.ordem_inicial = ordem_inicial
        self.ordem_final = ordem_final
        super().__init__()

    def calcula_ciclos_totais(self,ordem_inicial,ordem_final):  # Ver como ta isso
        cont = 0
        # sensor_inicial = self.sensor_inicial
        lista_sensores = list(models.sensores) # [sensor_inicial:len(self.sensores)]

        for ordem in list(range(ordem_inicial,ordem_final+1)): # self.no_ordens:
            for pasta in self.PASTAS: 
                cont+=1
        return cont

    def gerar_lista_ordem(self):
        return list(range(self.ordem_inicial,self.ordem_final+1))

    def calcular_freq_ref(self, acelerometro:str, rpm:float):
        if acelerometro.__contains__("externo"):
            freq = models.frequencias_rolamento.get("externo")
        else:
            freq = models.frequencias_rolamento.get("interno")

        freq = np.array(freq)
        return freq*rpm

    def calcular_rpm(self, dataframe):
        sinal_rpm = self.extrair_coluna(dataframe, self.COLUNA_RPM)
        sinal_sensor = self.extrair_coluna(dataframe, self.COLUNA_CONFERE_RPM)
        rpm_medio = get_rpm.GetRPM(sinal_rpm, sinal_sensor).get_rpm_medio('hz')
        return rpm_medio

    def salvar_dados(self, dados:dict, ordem:int):
        pasta = f'{models.path_dados_tratados}/ordens_{ordem}'
        dataframe = pd.json_normalize(dados)
        dataframe.to_csv(f'{pasta}/{models.nome_padrao_de_arquivo}_geral.csv')

    def run(self):
        ciclos_totais = self.calcula_ciclos_totais(self.ordem_inicial,self.ordem_final)
        ciclo_atual = 0
        start = self.iniciar_contagem()

        ordens = self.gerar_lista_ordem()
        for ordem in ordens:
            lista_dados = []

            cont = 0
            for pasta in self.PASTAS:
                defeito = self.PASTAS.get(pasta)
                arquivos = self.listar_arquivos(pasta)
                for arquivo in arquivos:
                    dataframe = self.ler_dataframe(pasta,arquivo)
                    rpm = self.calcular_rpm(dataframe)
                    for acelerometro in self.SENSORES:
                        col_acelerometro = self.SENSORES.get(acelerometro)
                        array_sensor = self.extrair_coluna(dataframe, col_acelerometro)
                        freq_referencia = self.calcular_freq_ref(acelerometro, rpm)
    
                        dados = extrair_indicadores.ExtrairIndicadores(
                            sinal=array_sensor,
                            rpm=rpm,
                            defeito=defeito,
                            freq_referencia=freq_referencia,
                            sensor = acelerometro
                        ).Get(ordem)
                        lista_dados.append(dados)
                cont+=1
                ciclo_atual+=1
                self.tempo_decorrido(start=start, ciclo_atual=ciclo_atual, ciclos_totais = ciclos_totais,cont=cont, ordem=ordem)

            self.salvar_dados(dados, ordem)
            
