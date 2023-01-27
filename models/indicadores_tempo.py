import models
import numpy as np
import matplotlib.pyplot as plt

class DominioTempo():
    """
    DominioTempo é uma classe que tem por objetivo extrair indicadores no domínio do tempo

    Parameters
    ----------

    sinal : array like -> array coluna que representa os dados brutos no domínio do tempo

    Returns
    -------
    None
    """
    def __init__(self,sinal):
        self.sinal = np.array(sinal)
        self.length = len(self.sinal)

        self.t_vector = np.linspace(0,1,models.freq_aquisicao)

    def plot_sinal_bruto(self):
        plt.plot(self.t_vector,self.sinal)
        plt.show()

    def maximum(self):
        self.max = np.max(self.sinal)        
        return self.max

    def minimum(self):
        self.min = np.min(self.sinal)        
        return self.min

    def mean(self):
        self.media = np.mean(self.sinal)        
        return self.media

    def standard_deviation(self):
        self.std = np.std(self.sinal, ddof = 1)        
        return self.std

    def rms(self):
        self.rms_value = np.sqrt(np.sum(n*n for n in self.sinal)/self.length)        
        return self.rms_value 

    def skewness(self):
        self.n = len(self.sinal)
        self.third_moment = np.sum((self.sinal - np.mean(self.sinal))**3) / self.length
        self.s_3 = np.std(self.sinal, ddof = 1) ** 3
        self.skew = self.third_moment/self.s_3

        return self.skew

    def kurtosis(self):
        self.n = len(self.sinal)
        self.fourth_moment = np.sum((self.sinal - np.mean(self.sinal))**4) / self.n
        self.s_4 = np.std(self.sinal, ddof = 1) ** 4
        self.kurt = self.fourth_moment / self.s_4 - 3

        return self.kurt

    def crest_factor(self):
        self.cf = self.max/self.rms_value
        return self.cf

    def form_factor(self):
        self.ff = self.rms_value/self.media
        return self.ff