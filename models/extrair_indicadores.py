import models
from models import indicadores_frequencia, indicadores_tempo, filtro_passa_baixa, get_rpm, get_raw_data
import numpy as np
import pandas as pd

class ExtrairIndicadores:

    def __init__(self,sinal,freq_referencia,rpm,defeito = 'normal',sensor = '',freq_aquisicao = models.freq_aquisicao):
        self.sinal = sinal
        self.defeito = defeito
        self.sensor = sensor
        self.rpm_medio = rpm
        self.FREQ_AQUISICAO = freq_aquisicao
        self.freq_referencia = np.append(freq_referencia, self.rpm_medio)

    def CriarObjeto(self,sinal):

        self.Objeto_Frequencia = indicadores_frequencia.DominioFrequencia(  sinal=sinal,
                                                                            rpm=self.rpm_medio,
                                                                            )

        self.Objeto_Temporal = indicadores_tempo.DominioTempo(sinal)

    def ExtrairOrdens(self,sinal,index=0,no_ordens=1):
        self.CriarObjeto(sinal)

        
        self.largura = self.rpm_medio

        self.soma_relativa_lista = []
        self.soma_list = []

        
        ordens_fourier, ordens_frequencia = self.Objeto_Frequencia.banda_frequencia(self.freq_referencia[index],self.largura,no_ordens)
        self.soma_relativa = self.Objeto_Frequencia.soma_relativa_sinal(ordens_fourier,self.Objeto_Frequencia.fft_transform)
        self.soma = self.Objeto_Frequencia.soma_sinal(ordens_fourier)

    def Get(self,no_ordens=1):
        
        indice = 0
        janela = 3.0 #segundo
        janela_pontos = janela*self.FREQ_AQUISICAO

        sobreposicao = 0.95 # %

        incrementer = int((janela*(1-sobreposicao))*self.FREQ_AQUISICAO)
        df = []

        while int(indice+janela_pontos) < len(self.sinal):
            sinal = self.sinal[int(indice):int(indice+janela_pontos)]
            indice += incrementer

            self.CriarObjeto(sinal)

            data_json = {
                'rotacao_hz' : self.rpm_medio,
                'maximo':np.abs(self.Objeto_Temporal.maximum()),
                'rms':np.abs(self.Objeto_Temporal.rms()),
                'assimetria':np.abs(self.Objeto_Temporal.skewness()),
                'curtose':np.abs(self.Objeto_Temporal.kurtosis()),
                # ,'fator_forma':np.abs(self.Objeto_Temporal.form_factor()),
                'fator_crista':np.abs(self.Objeto_Temporal.crest_factor())
                }
            
            for index in range(len(self.freq_referencia)):
                local = models.defeito_rolamento[index]
                self.ExtrairOrdens(sinal,index,no_ordens)

                data_json[f'soma_relativa_{local}'] = np.abs(self.soma_relativa)
                data_json[f'soma_{local}'] = np.abs(self.soma)

            data_json['sensor'] = self.sensor
            data_json['defeito'] = self.defeito

            df.append(data_json)

        return df

