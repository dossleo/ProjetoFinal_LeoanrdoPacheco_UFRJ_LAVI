import models
from models import indicadores_frequencia, indicadores_tempo
import numpy as np

class ExtrairIndicadores:
    def __init__(self,sinal_bruto,freq_referencia,largura_banda):
        self.sinal = sinal_bruto
        self.freq_referencia = []

        for freq in freq_referencia:
            self.freq_referencia.append(int(freq*models.rotacao_hz))

        self.largura = largura_banda

        self.Objeto_Frequencia = indicadores_frequencia.DominioFrequencia(self.sinal,models.rpm,models.freq_sample)
        self.Objeto_Temporal = indicadores_tempo.DominioTempo(self.sinal)
        

    def ExtrairOrdens(self,index=0,no_ordens=1):

        self.potencia_list = []
        self.soma_list = []

        for i in range(0,no_ordens):
            self.sinal_fourier,self.sinal_frequencia = self.Objeto_Frequencia.banda_frequencia(self.freq_referencia[index]*(i+1),self.largura)
            self.potencia_list.append(self.Objeto_Frequencia.potencia_sinal(self.sinal_fourier))
            self.soma_list.append(self.Objeto_Frequencia.soma_sinal(self.sinal_fourier))

        self.pot = np.mean(self.potencia_list)
        self.som = np.mean(self.soma_list)

    def Get(self,no_ordens=1):

        data_json = {
            'maximum':np.abs(self.Objeto_Temporal.maximum()),
            # 'minimum':np.abs(self.Objeto_Temporal.minimum()),
            # 'mean':np.abs(self.Objeto_Temporal.mean()),
            # 'standard_deviation':np.abs(self.Objeto_Temporal.standard_deviation()),
            'rms':np.abs(self.Objeto_Temporal.rms()),
            'skewness':np.abs(self.Objeto_Temporal.skewness()),
            'kurtosis':np.abs(self.Objeto_Temporal.kurtosis())
            # ,'form_factor':np.abs(self.Objeto_Temporal.form_factor()),
            # 'crest_factor':np.abs(self.Objeto_Temporal.crest_factor())
            }
        
        for index in range(len(self.freq_referencia)):
            defeito = models.fault_names[index]
            self.ExtrairOrdens(index,no_ordens)

            data_json[f'potencia_{defeito}'] = np.abs(self.pot)
            data_json[f'soma_{defeito}'] = np.abs(self.som)

        return data_json