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
                data,
                fs = 20480):

        self.fs = fs
        self.data = data
        self.dt = int(len(data))/self.fs

    def SignalSquared(self):
        self.signal = np.power(self.data,2)

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

    def Get(self):

        self.MovingMedian()

        self.x = np.array(self.signal/self.mediana)

        #Tentativa de passar a raiz quadrada no sinal
        # self.x = np.power(self.x,0.5)

        self.d = {'x': self.x, 't': self.t}
        self.df = pd.DataFrame(self.d)

        return self.x

    def RawData(self):
        self.MovingMedian()

        self.d = {'y': self.y, 't': self.t}
        self.df = pd.DataFrame(self.d)

        return self.df

    def PlotNormalData(self):

        self.Get()

        plt.plot(self.t,self.x)
        plt.show()