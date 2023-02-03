import models
import numpy as np
import pandas as pd

class NormalizarSinal():
    def __init__(self,dataframe) -> None:
        self.dataframe = dataframe
        self.df_sem_defeito = self.dataframe[self.dataframe['defeito']=='normal']

        self.df_freq = self.dataframe[models.colunas_freq]
        self.df_tempo = self.dataframe[models.colunas_tempo]

        self.df_sensor = self.dataframe[models.coluna_sensor]

        self.df_freq_sem_defeito = self.df_freq[self.df_freq[['defeito']=='normal']]
        self.df_tempo_sem_defeito = self.df_tempo[self.df_tempo[['defeito']=='normal']]

        self.calcular_max_min_sem_defeito()

    def calcular_max_min_sem_defeito(self):
        self.ymax_freq = np.max(np.array(self.df_freq_sem_defeito))
        self.ymin_freq = np.min(np.array(self.df_freq_sem_defeito))

					
        self.ymax_rotacao = np.max(np.array(self.df_sem_defeito['rotacao_hz']))
        self.ymax_maximo = np.max(np.array(self.df_sem_defeito['maximo']))
        self.ymax_rms = np.max(np.array(self.df_sem_defeito['rms']))
        self.ymax_assimetria = np.max(np.array(self.df_sem_defeito['assimetria']))
        self.ymax_curtose = np.max(np.array(self.df_sem_defeito['curtose']))
        self.ymax_fator_crista = np.max(np.array(self.df_sem_defeito['fator_crista']))

        self.ymin_rotacao = np.min(np.array(self.df_sem_defeito['rotacao_hz']))
        self.ymin_maximo = np.min(np.array(self.df_sem_defeito['maximo']))
        self.ymin_rms = np.min(np.array(self.df_sem_defeito['rms']))
        self.ymin_assimetria = np.min(np.array(self.df_sem_defeito['assimetria']))
        self.ymin_curtose = np.min(np.array(self.df_sem_defeito['curtose']))
        self.ymin_fator_crista = np.min(np.array(self.df_sem_defeito['fator_crista']))

        self.xmax = 1
        self.xmin = 0

    def normalizar_freq(self):
        self.df_freq_normalizado = ( (self.df_freq - self.ymin_freq) / (self.ymax_freq - self.ymin_freq) ) * (self.xmax - self.xmin) + self.xmin

    def normalizar_tempo(self):

        self.df_rotacao_normalizado = ( (self.df_tempo['rotacao_hz'] - self.ymin_rotacao) / (self.ymax_rotacao - self.ymin_rotacao) ) * (self.xmax - self.xmin) + self.xmin
        self.df_maximo_normalizado = ( (self.df_tempo['maximo'] - self.ymin_maximo) / (self.ymax_maximo - self.ymin_maximo) ) * (self.xmax - self.xmin) + self.xmin
        self.df_rms_normalizado = ( (self.df_tempo['rms'] - self.ymin_rms) / (self.ymax_rms - self.ymin_rms) ) * (self.xmax - self.xmin) + self.xmin
        self.df_assimetria_normalizado = ( (self.df_tempo['assimetria'] - self.ymin_assimetria) / (self.ymax_assimetria - self.ymin_assimetria) ) * (self.xmax - self.xmin) + self.xmin
        self.df_curtose_normalizado = ( (self.df_tempo['curtose'] - self.ymin_curtose) / (self.ymax_curtose - self.ymin_curtose) ) * (self.xmax - self.xmin) + self.xmin
        self.df_fator_crista_normalizado = ( (self.df_tempo['fator_crista'] - self.ymin_fator_crista) / (self.ymax_fator_crista - self.ymin_fator_crista) ) * (self.xmax - self.xmin) + self.xmin

    def Get(self):

        self.normalizar_tempo()
        self.normalizar_freq()

        lista_dataframes = [self.df_rotacao_normalizado,
                            self.df_maximo_normalizado,
                            self.df_rms_normalizado,
                            self.df_assimetria_normalizado,
                            self.df_curtose_normalizado,
                            self.df_fator_crista_normalizado,
                            self.df_freq_normalizado,
                            self.df_sensor]

        df = pd.concat(lista_dataframes)

        return df