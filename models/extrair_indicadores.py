import models
from models import indicadores_frequencia, indicadores_tempo, filtro_passa_baixa, get_rpm, get_raw_data
import numpy as np
import pandas as pd

class ExtrairIndicadores:
    def __init__(self,pasta,arquivo,coluna,freq_referencia,rpm,defeito = 'normal',sensor = ''):
        self.pasta = pasta
        self.arquivo = arquivo
        self.coluna = coluna
        self.defeito = defeito
        self.sensor = sensor
        self.rpm_medio = rpm

        self.sinal = get_raw_data.GetData(self.pasta,self.arquivo,self.coluna).Get()

        self.freq_referencia = freq_referencia
        self.freq_referencia.append(self.rpm_medio)

    def CriarObjeto(self,sinal,freq_aquisicao):

        self.Objeto_Frequencia = indicadores_frequencia.DominioFrequencia(sinal,freq_aquisicao)

        # self.Objeto_Frequencia.banda_frequencia()
        # indice_rpm_correto = list(self.fourier_banda).index(np.max(self.fourier_banda),0,-1)
        # self.rpm = np.abs(self.frequencia_banda[indice_rpm_correto])

        # Criando o array no domínio do tempo
        self.Objeto_Temporal = indicadores_tempo.DominioTempo(sinal)

    def ExtrairOrdens(self,sinal,freq_aquisicao,index=0,no_ordens=1):
        self.CriarObjeto(sinal,freq_aquisicao)

        self.erro = 0.1
        self.largura = 14

        self.soma_relativa_lista = []
        self.soma_list = []

        for i in range(0,no_ordens):
            self.largura = self.largura*(1+self.erro*no_ordens)
            self.sinal_fourier,self.sinal_frequencia = self.Objeto_Frequencia.banda_frequencia(self.freq_referencia[index]*(i+1),self.largura)
            self.soma_relativa_lista.append(self.Objeto_Frequencia.soma_relativa_sinal(self.sinal_fourier))
            # self.soma_list.append(self.Objeto_Frequencia.soma_sinal(np.real(self.sinal_fourier)))

        self.soma_relativa_media = np.sum(self.soma_relativa_lista)
        # self.som = np.mean(self.soma_list)

    def Get(self,no_ordens=1):
        freq_aquisicao = models.freq_aquisicao
        indice = 0
        janela = 2.0 #segundo
        janela_pontos = janela*freq_aquisicao

        sobreposicao = 0.90 # %

        incrementer = int((janela*(1-sobreposicao))*freq_aquisicao)

        while indice < len(self.sinal):
            sinal = self.sinal[int(indice):int(indice+janela_pontos)]
            indice += incrementer

            self.CriarObjeto(sinal,freq_aquisicao)

            data_json = {
                'rotacao_hz' : self.rpm_medio,
                'maximo':np.abs(self.Objeto_Temporal.maximum()),
                'rms':np.abs(self.Objeto_Temporal.rms()),
                'assimetria':np.abs(self.Objeto_Temporal.skewness()),
                'curtose':np.abs(self.Objeto_Temporal.kurtosis())
                ,'fator_forma':np.abs(self.Objeto_Temporal.form_factor()),
                'fator_crista':np.abs(self.Objeto_Temporal.crest_factor())
                }
            
            for index in range(len(self.freq_referencia)):
                local = models.defeito_rolamento[index]
                self.ExtrairOrdens(sinal,freq_aquisicao,index,no_ordens)

                data_json[f'soma_relativa_{local}'] = np.abs(self.soma_relativa_media)

            # data_json[f'soma_{local}'] = np.abs(self.som)
            data_json['sensor'] = self.sensor
            data_json['defeito'] = self.defeito

        return data_json

