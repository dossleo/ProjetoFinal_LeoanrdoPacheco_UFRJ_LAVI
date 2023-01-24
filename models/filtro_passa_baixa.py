import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import plotly.graph_objects as go
from scipy.signal import butter, filtfilt, freqz, lfilter

import models

class LowPassFilter():
    """
    Classe LowPassFilter() tem por objetivo aplicar um filtro passa-baixa nos dados brutos

    Parameters
    ----------

    data : array like -> array coluna dos dados brutos
    cutoff : float -> frequência de aplicação do filtro
    order : integer -> ordem de aplicação do filtro

    Returns
    -------
    None
    """
    def __init__(self,data, cutoff = models.rpm*(2/60), order = 5):
        self.data = data
        self.cutoff = cutoff
        self.order = order
        self.nyq = models.freq_sample//2

        t_final = len(self.data)/models.freq_sample
        n = int(len(self.data))

        self.vetor_tempo = np.linspace(0,t_final,n)

    def lowpass_filter(self):
        """
        lowpass_filter() é um método que tem por objetivo aplicar o filtro passa-baixa e retornar o valor filtrado.

        Parameters
        ----------

        None

        Returns
        -------
        y : array like -> dados de amplitude filtrada
        """
        normal_cutoff = self.cutoff / self.nyq
        # Get the filter coefficients 
        b, a = butter(self.order, normal_cutoff, btype='low', analog=False)
        y = filtfilt(b, a, self.data)
        return y

    def plot_plotly(self):
        """
        plot_plotly() é um método que exibe os dados filtrados utilizando a biblioteca plotly ao invés do matplotlib

        Parameters
        ----------

        None

        Returns
        -------
        None
        """
        y = self.lowpass_filter()
        fig = go.Figure()
        fig.add_trace(go.Scatter(
                    y = self.data,
                    line =  dict(shape =  'spline' ),
                    name = 'signal with noise'
                    ))
        fig.add_trace(go.Scatter(
                    y = y,
                    line =  dict(shape =  'spline' ),
                    name = 'filtered signal'
                    ))
        fig.show()
    
    def plot_time_domain(self,plot_raw_data = False):
        """
        plot_time_domain() é um método que tem por objetivo exibir os dados filtrados no domínio do tempo

        Parameters
        ----------

        None

        Returns
        -------
        None
        """
        y = self.lowpass_filter()

        plt.plot(self.vetor_tempo,y)
        if plot_raw_data:
            plt.plot(self.vetor_tempo,self.data)
            plt.legend(['Filtrado','Dados Brutos'])
        plt.show()