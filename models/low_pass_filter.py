from scipy.signal import butter,filtfilt
import plotly.graph_objects as go
from msilib.schema import SelfReg
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


class LowPassFilter():
    def __init__(self,data, cutoff, fs, order = 5):
        self.data = data
        self.cutoff = cutoff
        self.fs = fs
        self.order = order
        self.nyq = 0.5 * fs

    def butter_lowpass_filter(self):
        normal_cutoff = self.cutoff / self.nyq
        # Get the filter coefficients 
        b, a = butter(self.order, normal_cutoff, btype='low', analog=False)
        y = filtfilt(b, a, self.data)
        return y

    def plot_filtered_plotly(self):
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
    
    def plot_filtered_matplotlib(self):
        y = self.butter_lowpass_filter()
        plt.plot(np.linspace(0,self.data[-1],int(len(self.data))),y)
        plt.plot(np.linspace(0,self.data[-1],int(len(self.data))),self.data)
        plt.legend(['filtered signal','signal with noise'])
        plt.show()