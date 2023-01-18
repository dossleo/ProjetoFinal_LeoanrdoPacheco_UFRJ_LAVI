import os

import pandas as pd
from numpy import array

import models


class GetData():
    """
    Classe GetData() tem por objetivo extrair informações de um sinal de sensor.

    Parameters
    ----------

    path : string -> caminho onde se encontra o arquivo de sinal do sensor
    filename : string -> nome do arquivo do sinal de interesse
    column : integer -> coluna dentro do arquivo csv onde se encontra o sinal de interesse

    Returns
    -------
    None
    """

    def __init__(self,path,filename,column):
        
        self.path = path
        self.filename = filename
        self.dataset=pd.read_csv(os.path.join(path, self.filename), sep='\t',header=None)

        self.bearing_no = column
        self.bearing_data = array(self.dataset.iloc[:,self.bearing_no-1])
    
    def Get(self):
        """
        Get() é um método que tem por objetivo extrair os dados do sensor de interesse

        Parameters
        ----------

        None

        Returns
        -------
        bearing_data : (N,) Array like -> array coluna contendo o sinal do sensor
        """

        return self.bearing_data