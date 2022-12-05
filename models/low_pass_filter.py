import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import plotly.graph_objects as go
from scipy.signal import butter, filtfilt, freqz, lfilter

import models

class LowPassFilter():
    def __init__(self,data, cutoff, order = 5):
        self.data = data
        self.cutoff = cutoff
        self.order = order
        self.nyq = models.freq_sample//2

        t_final = len(self.data)/models.freq_sample
        n = int(len(self.data))

        self.vetor_tempo = np.linspace(0,t_final,n)

    def lowpass_filter(self):
        normal_cutoff = self.cutoff / self.nyq
        # Get the filter coefficients 
        b, a = butter(self.order, normal_cutoff, btype='low', analog=False)
        y = filtfilt(b, a, self.data)
        return y

    def plot_plotly(self):
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

        y = self.lowpass_filter()

        plt.plot(self.vetor_tempo,y)
        if plot_raw_data:
            plt.plot(self.vetor_tempo,self.data)
            plt.legend(['Filtrado','Dados Brutos'])
        plt.show()