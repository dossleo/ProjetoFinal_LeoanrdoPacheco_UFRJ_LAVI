from msilib.schema import SelfReg
import matplotlib.pyplot as plt
import scipy.io
import numpy as np
import pandas as pd
import os
import glob
from math import sqrt
from scipy.fft import fft, fftfreq
import models

class FrequencyFeaturesExtraction():
    def __init__(self,data):
        
        self.data = data
        self.length = len(self.data)

        t_final = self.length/models.freq_sample
        self.T = t_final/models.freq_sample
        self.time_vector = np.linspace(0.0, t_final, self.length, endpoint=False)
        self.ymin = -100
        self.ymax = 100

    def RunFFT(self):
        self.fourier = fft(self.data)[0:self.length//2]
        primeiros_pontos = 2
        self.fourier[0:primeiros_pontos] = np.zeros(primeiros_pontos)
        self.freq = fftfreq(self.length,self.T)[0:self.length//2]

    def PlotFrequencyDomain(self):
        self.RunFFT()
        # self.fourier = self.rms()
        self.fig, self.ax = plt.subplots()
        self.ax.plot(self.freq, self.fourier)
        plt.title('Legenda')
        plt.xlabel('Frequency (Hz)')
        plt.ylabel('Amplitude')

        freq1 = models.fault_frequency[0]
        freq2 = models.fault_frequency[1]
        freq3 = models.fault_frequency[2]
        freq4 = models.fault_frequency[3]
        freq_plot = freq3
        ordens = 10

        for i in range(ordens):
            plt.vlines(freq_plot*(i+1),self.ymin,self.ymax,'red','dashed')

        plt.grid(True)
        plt.show()

    def JanelaFrequencia(self,freq_referencia,tamanho_janela_hz = 40):
        self.RunFFT()
        
        delta_f = (models.freq_sample/2)/len(self.freq)
        tamanho_janela_samples = int((delta_f*tamanho_janela_hz))

        elemento_referencia = int(freq_referencia/delta_f)

        inicio_janela = int(elemento_referencia-tamanho_janela_samples/2)
        fim_janela = int(elemento_referencia+tamanho_janela_samples/2)

        self.intervalo_janela = [inicio_janela,fim_janela]

        self.janela_freq = self.freq[inicio_janela:fim_janela]
        self.janela_fourier = self.fourier[inicio_janela:fim_janela]

        plt.plot(self.janela_freq,self.janela_fourier)
        plt.vlines(freq_referencia,self.ymin,self.ymax,'red','dashed')
        plt.show()

    def PicosRPM(self):
        pass
        # self.RunFFT()
    
    def PicosPistaExterna(self):
        pass
        # self.RunFFT()

    def PicosPistaInterna(self):
        pass
        # self.RunFFT()

    def PicosGaiola(self):
        pass
        # self.RunFFT()

    def PicosRolo(self):
        pass
        # self.RunFFT()

    def rms(self):
        pass
        # self.RunFFT()
        # self.rms_value = sqrt(sum(n*n for n in self.data[0:int(len(self.data))//100])//self.length)        
        # return self.rms_value 