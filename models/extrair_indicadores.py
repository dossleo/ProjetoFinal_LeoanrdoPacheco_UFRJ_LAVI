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
                                                                            rpm=self.rpm_medio
                                                                            )

        self.Objeto_Temporal = indicadores_tempo.DominioTempo(sinal)

    def ExtrairHarmonicos(self,sinal,index=0,no_harmonicos=1):
        self.CriarObjeto(sinal)

        
        self.largura = self.rpm_medio

        # self.pot_relativa_lista = []
        self.pot_list = []

        
        harmonicos_fourier, harmonicos_frequencia = self.Objeto_Frequencia.banda_frequencia(self.freq_referencia[index],self.largura,no_harmonicos)
        # self.pot_relativa = self.Objeto_Frequencia.pot_relativa_sinal(harmonicos_fourier,self.Objeto_Frequencia.fft_transform)
        self.pot = self.Objeto_Frequencia.pot_sinal(harmonicos_fourier)

    def Get(self,no_harmonicos=1):
        
        indice = 0
        janela = models.time_window

        sobreposicao = models.overlap

        janela_pontos = janela*self.FREQ_AQUISICAO
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
                self.ExtrairHarmonicos(sinal,index,no_harmonicos)

                # data_json[f'pot_relativa_{local}'] = np.abs(self.pot_relativa)
                data_json[f'Pot_{local}'] = np.abs(self.pot)

            data_json['sensor'] = self.sensor
            data_json['defeito'] = self.defeito

            df.append(data_json)

        return df

