import models
import numpy as np
import pandas as pd

class NormalizarSinal():

    COLUNAS_FREQ_SOMA = models.colunas_freq_soma
    COLUNAS_FREQ_SOMA_RELATIVA = models.colunas_freq_soma_relativa
    
    def __init__(self,dataframe,ordem,metodo = 1) -> None:
        self.dataframe = pd.DataFrame(dataframe)

        self.colunas = models.colunas
        self.ordem = ordem
        defeito = 'defeito'
        normal = 'normal'

        self.df_sem_defeito = self.dataframe[self.dataframe[defeito]==normal]

        self.df_freq_soma = self.dataframe[self.COLUNAS_FREQ_SOMA]
        self.df_freq_soma_relativa = self.dataframe[self.COLUNAS_FREQ_SOMA_RELATIVA]

        self.df_tempo = self.dataframe[models.colunas_tempo]

        self.df_freq_soma_sem_defeito = self.df_freq_soma[self.df_freq_soma[defeito]==normal]
        self.df_freq_soma_relativa_sem_defeito = self.df_freq_soma_relativa[self.df_freq_soma_relativa[defeito]==normal]
        self.df_tempo_sem_defeito = self.df_tempo[self.df_tempo[defeito]==normal]

        self.df_sensor = self.dataframe[models.coluna_sensor]

        self.df_defeito = self.dataframe[defeito]
        if metodo == 1:
            self.calcular_max_min_metodo1()
        else:
            self.calcular_max_min_metodo2()


    def calcular_max_min_metodo1(self):

        self.ymax_freq_soma = np.max(np.array(self.df_freq_soma[self.COLUNAS_FREQ_SOMA[0:-1]]))
        self.ymin_freq_soma = np.min(np.array(self.df_freq_soma[self.COLUNAS_FREQ_SOMA[0:-1]]))

        self.ymax_freq_soma_relativa = np.max(np.array(self.df_freq_soma_relativa[self.COLUNAS_FREQ_SOMA_RELATIVA[0:-1]]))
        self.ymin_freq_soma_relativa = np.min(np.array(self.df_freq_soma_relativa[self.COLUNAS_FREQ_SOMA_RELATIVA[0:-1]]))

        self.ymax_rotacao =         np.max(np.array(self.dataframe['rotacao_hz']))
        self.ymax_maximo =          np.max(np.array(self.dataframe['maximo']))
        self.ymax_rms =             np.max(np.array(self.dataframe['rms']))
        self.ymax_assimetria =      np.max(np.array(self.dataframe['assimetria']))
        self.ymax_curtose =         np.max(np.array(self.dataframe['curtose']))
        self.ymax_fator_crista =    np.max(np.array(self.dataframe['fator_crista']))

        self.ymin_rotacao =         np.min(np.array(self.dataframe['rotacao_hz']))
        self.ymin_maximo =          np.min(np.array(self.dataframe['maximo']))
        self.ymin_rms =             np.min(np.array(self.dataframe['rms']))
        self.ymin_assimetria =      np.min(np.array(self.dataframe['assimetria']))
        self.ymin_curtose =         np.min(np.array(self.dataframe['curtose']))
        self.ymin_fator_crista =    np.min(np.array(self.dataframe['fator_crista']))

        self.xmax = 1
        self.xmin = 0

        self.x = (self.xmax - self.xmin) + self.xmin

    def calcular_max_min_metodo2(self):
        # Modificar o ymin e ymax relativo apenas para os dados do rolamento bom
        
        self.ymax_freq_soma = np.max(np.array(self.df_freq_soma_sem_defeito[self.COLUNAS_FREQ_SOMA[0:-1]]))
        self.ymin_freq_soma = np.min(np.array(self.df_freq_soma_sem_defeito[self.COLUNAS_FREQ_SOMA[0:-1]]))

        self.ymax_freq_soma_relativa = np.max(np.array(self.df_freq_soma_relativa_sem_defeito[self.COLUNAS_FREQ_SOMA_RELATIVA[0:-1]]))
        self.ymin_freq_soma_relativa = np.min(np.array(self.df_freq_soma_relativa_sem_defeito[self.COLUNAS_FREQ_SOMA_RELATIVA[0:-1]]))

        self.ymax_rotacao =         np.max(np.array(self.df_sem_defeito['rotacao_hz']))
        self.ymax_maximo =          np.max(np.array(self.df_sem_defeito['maximo']))
        self.ymax_rms =             np.max(np.array(self.df_sem_defeito['rms']))
        self.ymax_assimetria =      np.max(np.array(self.df_sem_defeito['assimetria']))
        self.ymax_curtose =         np.max(np.array(self.df_sem_defeito['curtose']))
        self.ymax_fator_crista =    np.max(np.array(self.df_sem_defeito['fator_crista']))

        self.ymin_rotacao =         np.min(np.array(self.df_sem_defeito['rotacao_hz']))
        self.ymin_maximo =          np.min(np.array(self.df_sem_defeito['maximo']))
        self.ymin_rms =             np.min(np.array(self.df_sem_defeito['rms']))
        self.ymin_assimetria =      np.min(np.array(self.df_sem_defeito['assimetria']))
        self.ymin_curtose =         np.min(np.array(self.df_sem_defeito['curtose']))
        self.ymin_fator_crista =    np.min(np.array(self.df_sem_defeito['fator_crista']))

        self.xmax = 1
        self.xmin = 0

        self.x = (self.xmax - self.xmin) + self.xmin

    def normalizar_freq(self):
        self.df_freq_soma_normalizado =             ( (self.dataframe[self.COLUNAS_FREQ_SOMA[0:-1]]             - self.ymin_freq_soma)          / (self.ymax_freq_soma          - self.ymin_freq_soma           ) ) * self.x
        self.df_freq_soma_relativa_normalizado =    ( (self.dataframe[self.COLUNAS_FREQ_SOMA_RELATIVA[0:-1]]    - self.ymin_freq_soma_relativa) / (self.ymax_freq_soma_relativa - self.ymin_freq_soma_relativa  ) ) * self.x
    
    def normalizar_tempo(self):

        self.df_rotacao_normalizado =       ( (self.dataframe['rotacao_hz']     - self.ymin_rotacao)        / (self.ymax_rotacao        - self.ymin_rotacao) )          * self.x
        self.df_maximo_normalizado =        ( (self.dataframe['maximo']         - self.ymin_maximo)         / (self.ymax_maximo         - self.ymin_maximo) )           * self.x
        self.df_rms_normalizado =           ( (self.dataframe['rms']            - self.ymin_rms)            / (self.ymax_rms            - self.ymin_rms) )              * self.x
        self.df_assimetria_normalizado =    ( (self.dataframe['assimetria']     - self.ymin_assimetria)     / (self.ymax_assimetria     - self.ymin_assimetria) )       * self.x
        self.df_curtose_normalizado =       ( (self.dataframe['curtose']        - self.ymin_curtose)        / (self.ymax_curtose        - self.ymin_curtose) )          * self.x
        self.df_fator_crista_normalizado =  ( (self.dataframe['fator_crista']   - self.ymin_fator_crista)   / (self.ymax_fator_crista   - self.ymin_fator_crista) )     * self.x

    def normalizar_sensor(self):

        self.dataframe['sensor'] = self.dataframe['sensor'].replace(models.sensores)

        self.ymax_sensor = np.max(np.array(self.dataframe['sensor']))

        self.ymin_sensor = np.min(np.array(self.dataframe['sensor']))

        self.dataframe['sensor'] = ( (self.dataframe['sensor'] - self.ymin_sensor) / (self.ymax_sensor - self.ymin_sensor) ) * self.x
        
        self.df_sensor = self.dataframe['sensor']

    def Get(self):

        self.normalizar_tempo()
        self.normalizar_freq()
        self.normalizar_sensor()

        lista_dataframes = [self.df_rotacao_normalizado,
                            self.df_maximo_normalizado,
                            self.df_rms_normalizado,
                            self.df_assimetria_normalizado,
                            self.df_curtose_normalizado,
                            self.df_fator_crista_normalizado,
                            self.df_freq_soma_normalizado,
                            self.df_freq_soma_relativa_normalizado,
                            self.df_sensor,
                            self.df_defeito]

        df = pd.concat(lista_dataframes,axis=1,ignore_index=False)
        df = pd.DataFrame(df.reset_index(drop=False))

        df = df[df.columns[len(df.columns)-len(models.colunas):len(df.columns)]]

        return df

    def save_as_csv(self):
        df = self.Get()

        df.to_csv(f'{models.path_dados_tratados}/ordens_{self.ordem}/Dados_Normalizados.csv')
        print(f'Arquivo salvo com sucesso!\n{models.path_dados_tratados}/ordens_{self.ordem}/Dados_Normalizados.csv')