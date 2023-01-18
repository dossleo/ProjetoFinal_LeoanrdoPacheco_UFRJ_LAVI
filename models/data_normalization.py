import glob
import os
from math import *

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import scipy.fftpack
from scipy.signal import chirp, hilbert

import models


class DataNormalized():

    """
    Classe DataNormalized() aplica o método NAMVOC de normalização.
    Este método corrige mudanças na amplitude devido à variação da frequência de um sinal.

    Parameters
    ----------

    data : (N,) array_like
    
    Returns
    -------
    None
    """


    def __init__(self,data):

        self.fs = models.freq_sample
        self.data = data
        self.dt = int(len(data))/self.fs

    def signal_squared(self):
        """
        signal_squared() aplica a potência de 2 no input data
        """

        self.signal = np.power(self.data,2)

    def temporal_window(self):
        """
        temporal_window() define uma janela temporal em que a normalização será aplicada.
        """

        self.signal_squared()

        self.duration = 1.0
        self.samples = int(self.fs*self.duration)
        self.t = np.arange(self.samples) / self.fs

    def amplitude_envelope(self):
        """
        amplitude_envelope() cria, a partir da janela temporal, um envelope para o sinal ao quadrado.
        Este envelope é obtido pela transofrmada de hilbert.
        """

        self.temporal_window()

        self.analytic_signal = hilbert(self.signal)
        self.envelope = abs(self.analytic_signal)
    
    def moving_median(self):
        """
        moving_median() aplica a média móvel
        """

        #Todo: verificar se este método está correto

        self.amplitude_envelope()

        self.mediana = sqrt(np.median(self.envelope))

    def get(self):
        """
        get() aplica todos os métodos da classe para calcular a amplitude normalizada.
        Retorna a amplitude normalizada
        """

        self.moving_median()

        self.x = np.array(self.signal/self.mediana)

        self.d = {'x': self.x, 't': self.t}
        self.df = pd.DataFrame(self.d)

        return self.x

    def plot_normal_data(self):
        """
        plot_normal_data calcula() a amplitude normalizada.
        Depois cria um plot dessa amplitude no domínio do tempo.
        """

        self.get()

        plt.plot(self.t,self.x)
        plt.show()
