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
    def __init__(self,data):

        self.fs = models.freq_sample
        self.data = data
        self.dt = int(len(data))/self.fs

    def signal_squared(self):
        self.signal = np.power(self.data,2)

    def temporal_window(self):

        self.signal_squared()

        self.duration = 1.0
        self.samples = int(self.fs*self.duration)
        self.t = np.arange(self.samples) / self.fs

    def amplitude_envelope(self):
        
        self.temporal_window()

        self.analytic_signal = hilbert(self.signal)
        self.envelope = abs(self.analytic_signal)
    
    def moving_median(self):

        self.amplitude_envelope()

        self.mediana = sqrt(np.median(self.envelope))

    def get(self):

        self.moving_median()

        self.x = np.array(self.signal/self.mediana)

        self.d = {'x': self.x, 't': self.t}
        self.df = pd.DataFrame(self.d)

        return self.x

    def raw_data(self):
        self.moving_median()

        self.d = {'y': self.y, 't': self.t}
        self.df = pd.DataFrame(self.d)

        return self.df

    def plot_normal_data(self):

        self.get()

        plt.plot(self.t,self.x)
        plt.show()
