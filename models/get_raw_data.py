import models
import os
import pandas as pd
import numpy as np

class GetData():
    """
    Classe GetData() tem por objetivo extrair informações de um sinal de sensor.

    Parameters
    ----------

    pasta : string -> caminho onde se encontra o arquivo de sinal do sensor
    arquivo : string -> nome do arquivo do sinal de interesse
    coluna : integer -> coluna dentro do arquivo csv onde se encontra o sinal de interesse

    Returns
    -------
    None
    """

    def __init__(self,pasta,arquivo,coluna):
        
        self.pasta = pasta
        self.arquivo = arquivo
        self.dataset=pd.read_csv(os.path.join(pasta, self.arquivo), sep='\t',header=None)

        self.coluna = coluna
        self.sinal = np.array(self.dataset.iloc[:,self.coluna-1])
    
    def Get(self):
        """
        Get() é um método da Classe GetData()
        que tem por objetivo extrair os dados do sensor de interesse

        Parameters
        ----------

        None

        Returns
        -------
        bearing_data : (N,) Array like -> array coluna contendo o sinal do sensor
        """

        return self.sinal
