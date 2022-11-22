from scipy.signal import butter,filtfilt
import plotly.graph_objects as go
from msilib.schema import SelfReg
import matplotlib.pyplot as plt
import scipy.io
import numpy as np
import pandas as pd
import os
import glob
from math import sqrt

path=r'database/brutos/2nd_test'
filename = '2004.02.12.10.32.39'

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

    def butter_lowpass_filter(self):
        normal_cutoff = self.cutoff / nyq
        # Get the filter coefficients 
        b, a = butter(self.order, normal_cutoff, btype='low', analog=False)
        y = filtfilt(b, a, self.data)
        return y

    def plot_plotly(self):
        y = self.butter_lowpass_filter()
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
    
    def plot_matplotlib(self):
        y = self.butter_lowpass_filter()
        plt.plot(np.linspace(0,self.data[-1],int(len(self.data))),y)
        plt.plot(np.linspace(0,self.data[-1],int(len(self.data))),self.data)
        plt.legend(['Filtrado','Dados Brutos'])
        plt.show()

if __name__ == "__main__":
    # Filter requirements.
    data = GetData(path,filename,1).Get()
    # data = data[0:len(data)//4]


    fs = 20000
    cutoff = 500
    T = len(data)/fs
    nyq = 0.5 * fs
    order = 5
    n = int(T * fs)

    teste = LowPassFilter(data,cutoff,fs,order)
    teste.plot_matplotlib()