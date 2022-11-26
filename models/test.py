from scipy.signal import butter,filtfilt, hilbert, chirp
import plotly.graph_objects as go
import scipy.io
import numpy as np
import pandas as pd
import os
from msilib.schema import SelfReg
import matplotlib.pyplot as plt
import glob
from math import *
import scipy.fftpack

path=r'database/brutos/2nd_test'
filename = '2004.02.12.10.32.39'


class DataNormalized():
    def __init__(self,
                data,
                fs = 20480):

        self.fs = fs
        self.data = data
        self.dt = int(len(data))/self.fs

    def SignalSquared(self):
        self.signal = np.power(self.data,2)
        return self.signal

    def TemporalWindow(self):

        self.SignalSquared()

        self.duration = 1.0
        self.samples = int(self.fs*self.duration)
        self.t = np.arange(self.samples) / self.fs
        return self.t

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


class GetData():

    def __init__(self,path,filename,column):
        

        self.path = path
        self.filename = filename
        self.dataset=pd.read_csv(os.path.join(path, self.filename), sep='\t',header=None)

        self.bearing_no = column
        self.bearing_data = np.array(self.dataset.iloc[:,self.bearing_no-1])

        self.length = len(self.bearing_data)
    
    def Get(self):
        return self.bearing_data


class LowPassFilter():
    def __init__(self,data, cutoff, fs, order = 5):
        self.data = data
        self.cutoff = cutoff
        self.fs = fs
        self.order = order
        self.nyq = 0.5 * fs

        t_final = int(len(self.data)/self.fs)
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
    
    def plot_matplotlib(self,plot_raw_data = False):

        y = self.lowpass_filter()

        plt.plot(self.vetor_tempo,y)
        if plot_raw_data:
            plt.plot(self.vetor_tempo,self.data)
            plt.legend(['Filtrado','Dados Brutos'])
        plt.show()

if __name__ == "__main__":
    data = GetData(path,filename,1).Get()


    fs = 20480
    cutoff = 400
    order = 5

    teste = LowPassFilter(data,cutoff,fs,order)
    teste.plot_matplotlib(plot_raw_data = False)

    data_filtered = teste.lowpass_filter()

