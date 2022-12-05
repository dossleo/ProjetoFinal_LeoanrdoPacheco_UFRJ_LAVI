import glob
import os
from math import sqrt

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import scipy.io
from scipy.fft import fft, fftfreq

import models
from models import time_features_extraction


class FrequencyFeaturesExtraction():
    def __init__(self,data,rpm,label):
        
        self.data = data
        self.label = label
        self.length = len(self.data)
        self.rpm = rpm

        t_final = self.length/models.freq_sample

        self.T = t_final/models.freq_sample

        self.time_vector = np.linspace(0.0, t_final, self.length, endpoint=False)
        self.ymin = -200
        self.ymax = 200

        self.features = models.features

    def run_fft(self):
        self.eixo_y_fourier = fft(self.data)[0:self.length//2]
        primeiros_pontos = 2
        self.eixo_y_fourier[0:primeiros_pontos] = np.zeros(primeiros_pontos)
        self.eixo_freq = fftfreq(self.length,self.T)[0:self.length//2]
        
        self.eixo_y_fourier = np.real(self.eixo_y_fourier)
        self.eixo_freq = np.real(self.eixo_freq)
        self.eixo_freq = self.eixo_freq/self.rpm

    def plot_frequency_domain(self,freq_referencia,no_ordens = 1):

        self.run_fft()

        plt.plot(self.eixo_freq, self.eixo_y_fourier)
        plt.title('Domínio da Frequência')
        plt.xlabel('Frequency (Hz)')
        plt.ylabel('Amplitude')

        for i in range(no_ordens):
            plt.vlines(freq_referencia*(i+1)/self.rpm,self.ymin,self.ymax,'red','dashed')

        plt.grid(True)
        plt.show()

    def window_around_frequency(self,freq_referencia,tamanho_janela_hz = 40):
        self.run_fft()
        
        self.delta_f = (self.rpm*self.eixo_freq[-1]-self.eixo_freq[0])/len(self.eixo_freq)
        self.tamanho_janela_samples = int((tamanho_janela_hz/self.delta_f))

        elemento_referencia = int(freq_referencia/self.delta_f)

        self.inicio_janela = int(elemento_referencia-self.tamanho_janela_samples/2)
        self.fim_janela = int(elemento_referencia+self.tamanho_janela_samples/2)

        if self.eixo_freq[0] > self.eixo_freq[self.inicio_janela]:

            self.intervalo_janela = [self.inicio_janela,self.fim_janela]
            self.janela_freq = self.eixo_freq[self.inicio_janela:self.fim_janela]
            self.janela_fourier = self.eixo_y_fourier[self.inicio_janela:self.fim_janela]

        else:
            
            self.intervalo_janela = [0,self.fim_janela]
            self.janela_freq = self.eixo_freq[0:self.fim_janela]
            self.janela_fourier = self.eixo_y_fourier[0:self.fim_janela]

        return self.janela_fourier

    def plot_window(self,freq_referencia,tamanho_janela_hz = 40):
        self.window_around_frequency(freq_referencia,tamanho_janela_hz)

        plt.plot(self.janela_freq,self.janela_fourier)
        plt.vlines(freq_referencia/self.rpm,self.ymin,self.ymax,'red','dashed')
        plt.ylim((self.ymin,self.ymax))
        plt.show()

    def get_features(self,freq_referencia,tamanho_janela_hz = 40,no_ordens = 1):
        metricas = []
        data_jason={}

        for i in range(no_ordens):
            dados = self.window_around_frequency(freq_referencia*(i+1),tamanho_janela_hz)
            metricas_frequencia = time_features_extraction.TimeFeatures(dados)
            dicionario = metricas_frequencia.run()
            dicionario['ordem'] = i+1
            metricas.append(dicionario)

        self.metricas = pd.json_normalize(metricas)
        self.media = self.metricas.mean()

        for i in range(len(self.features)):
            data_jason[f'{self.features[i]}_{self.label}'] = self.media[i]

        return data_jason
 
