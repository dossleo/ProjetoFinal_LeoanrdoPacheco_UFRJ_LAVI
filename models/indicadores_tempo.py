import models
import numpy as np
import matplotlib.pyplot as plt
import scipy.stats

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
    def __init__(self,sinal,freq_aquisicao = models.freq_aquisicao):
        self.sinal = np.array(sinal)
        self.length = len(self.sinal)
        self.freq_aquisicao = freq_aquisicao

        self.t_vector = np.linspace(0,1,self.freq_aquisicao)

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
        self.rms_value = np.sqrt(np.mean(self.sinal**2)) 
        return self.rms_value 

    def skewness(self):
        self.n = len(self.sinal)
        self.third_moment = np.sum((self.sinal - np.mean(self.sinal))**3) / self.length
        self.s_3 = np.std(self.sinal, ddof = 1) ** 3
        self.skew = self.third_moment/self.s_3
        return self.skew

    def kurtosis(self):
        self.kurt = scipy.stats.kurtosis(self.sinal,fisher=False)
        return self.kurt

    def crest_factor(self):
        self.cf = self.maximum()/self.rms()
        return self.cf
