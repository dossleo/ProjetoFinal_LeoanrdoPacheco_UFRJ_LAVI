# Importando bibliotecas 
# %%
from msilib.schema import SelfReg
import matplotlib.pyplot as plt
from scipy.signal import hilbert, chirp
import numpy as np
import pandas as pd
import os
import glob
from math import *
import scipy.fftpack

class DataNormalized():
    def __init__(self,
                path='C:/Users/leona/Documents/ProjetoFinal_LeonardoPacheco_UFRJ_LAVI/database/brutos/2nd_test',
                file='2004.02.12.11.02.39',
                column=-1,
                dt = 1,
                fs = 20480):

        self.path = path
        self.file = file
        self.column = column
        self.dt = dt
        self.fs = fs
        self.dataset=pd.read_csv(os.path.join(self.path, self.file), sep='\t',header=None)

    def SignalSquared(self):
        self.y = self.dataset.iloc[:,self.column]
        self.signal = np.power(self.y,2)

    def TemporalWindow(self):

        self.SignalSquared()

        self.duration = 1.0
        self.samples = int(self.fs*self.duration)
        self.t = np.arange(self.samples) / self.fs

    def AmplitudeEnvelope(self):
        
        self.TemporalWindow()

        self.analytic_signal = hilbert(self.signal)
        self.amplitude_envelope = abs(self.analytic_signal)
    
    def MovingMedian(self):

        self.AmplitudeEnvelope()

        self.mediana = sqrt(np.median(self.amplitude_envelope))

    def DataNormalized(self):

        self.MovingMedian()

        self.x = self.signal/self.mediana

        self.d = {'x': self.x, 't': self.t}
        self.df = pd.DataFrame(self.d)

        return self.df

    def RawData(self):
        self.MovingMedian()

        self.d = {'y': self.y, 't': self.t}
        self.df = pd.DataFrame(self.d)

        return self.df

    def PlotNormalData(self):

        self.DataNormalized()

        plt.plot(self.t,self.x)
        plt.show()

# %%
# path = 'C:/Users/leona/Documents/ProjetoFinal_LeonardoPacheco_UFRJ_LAVI/database/brutos/2nd_test'
# file = '2004.02.12.11.02.39'
# column = -1

Teste1 = DataNormalized()
normalizados = Teste1.DataNormalized()


# %%]

brutos = Teste1.RawData()

# %%

plt.plot(Teste1.t,normalizados["x"])
plt.show
# %%

# %%
plt.plot(Teste1.t,brutos["y"])
plt.show
# %%
