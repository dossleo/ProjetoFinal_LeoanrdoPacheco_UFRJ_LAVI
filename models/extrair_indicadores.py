import models
from models import indicadores_frequencia, indicadores_tempo, filtro_passa_baixa, get_rpm, get_raw_data
import numpy as np
import pandas as pd

class ExtrairIndicadores:
    def __init__(self,pasta,arquivo,coluna,freq_referencia,defeito = 'normal',sensor = ''):
        self.pasta = pasta
        self.arquivo = arquivo
        self.coluna = coluna
        self.defeito = defeito
        self.sensor = sensor

        self.sinal = get_raw_data.GetData(self.pasta,self.arquivo,self.coluna).Get()

        self.freq_referencia = freq_referencia

    def ExtrairRPM(self):
        self.sinal_rpm = get_raw_data.GetData(self.pasta,self.arquivo,0).Get()
        self.rpm = get_rpm.GetRPM(self.sinal_rpm)
        self.rpm_medio = self.rpm.get_rpm_medio(unidade='hz')

    def Filtrar(self):

        self.ExtrairRPM()

        # freq_passa_baixa = self.rpm_medio*5
        # ordens_filtro = 5

        # Criando o array no domínio da frequência
        # Filtro = filtro_passa_baixa.Filtro(self.sinal,cutoff=freq_passa_baixa,order=ordens_filtro)
        # sinal_filtrado = Filtro.FiltroPassaBaixa()

    def CriarObjeto(self):
        self.Filtrar()

        self.Objeto_Frequencia = indicadores_frequencia.DominioFrequencia(self.sinal,models.freq_aquisicao)

        # Criando o array no domínio do tempo
        self.Objeto_Temporal = indicadores_tempo.DominioTempo(self.sinal)

    def ExtrairOrdens(self,index=0,no_ordens=1):
        self.CriarObjeto()

        self.erro = 0.1
        self.largura = 2

        # self.potencia_list = []
        self.soma_list = []

        for i in range(0,no_ordens):
            self.sinal_fourier,self.sinal_frequencia = self.Objeto_Frequencia.banda_frequencia(self.freq_referencia[index]*(i+1),self.largura)
            # self.potencia_list.append(self.Objeto_Frequencia.potencia_sinal(self.sinal_fourier))
            self.soma_list.append(self.Objeto_Frequencia.soma_sinal(np.real(self.sinal_fourier)))

        # self.pot = np.mean(self.potencia_list)
        self.som = np.mean(self.soma_list)
    def ExtrairOrgens_test(self,index=0,no_ordens=1):
        self.CriarObjeto()
        
        for i in range(len(self.freq_referencia)):
            self.freq_referencia[i] = self.freq_referencia[i]*self.rpm_medio

        self.erro = 0.1
        self.largura = 2

        # self.potencia_list = []
        self.soma_list = []

        # for i in range(0,no_ordens):
        self.sinal_fourier,self.sinal_frequencia = self.Objeto_Frequencia.banda_frequencia(self.freq_referencia[index],self.largura)
        # self.potencia_list.append(self.Objeto_Frequencia.potencia_sinal(self.sinal_fourier))
        self.soma_list.append(self.Objeto_Frequencia.soma_sinal(np.real(self.sinal_fourier)))

        # self.pot = np.mean(self.potencia_list)
        self.som = np.mean(self.soma_list)
        print(self.som)

    def Get(self,no_ordens=1):
        self.CriarObjeto()

        data_json = {
            'rotacao_hz' : self.rpm_medio,
            'maximo':np.abs(self.Objeto_Temporal.maximum()),
            'rms':np.abs(self.Objeto_Temporal.rms()),
            'assimetria':np.abs(self.Objeto_Temporal.skewness()),
            'curtose':np.abs(self.Objeto_Temporal.kurtosis())
            # ,'fator_forma':np.abs(self.Objeto_Temporal.form_factor()),
            # 'fator_crista':np.abs(self.Objeto_Temporal.crest_factor())
            }
        
        for index in range(len(self.freq_referencia)):
            local = models.defeito_rolamento[index]
            self.ExtrairOrdens(index,no_ordens)

            # data_json[f'potencia_{local}'] = np.abs(self.pot)
            data_json[f'soma_{local}'] = np.abs(self.som)

        data_json['defeito'] = self.defeito
        data_json['sensor'] = self.sensor
        return data_json

