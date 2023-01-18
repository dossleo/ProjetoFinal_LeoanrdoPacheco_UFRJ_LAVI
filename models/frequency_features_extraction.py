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
    """
    Classe FrequencyFeaturesExtraction() tem o objetivo de fazer a análise dos dados no domínio da frequência.

    Parameters
    ----------

    data : (N,) array_like
    rpm : integer
    label : string
    
    Returns
    -------
    None
    """

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
        """
        run_fft() é um método da Classe FrequencyFeaturesExtraction() 
        que aplica a fft nos dados de entrada.
        A aplicação da fft segue o seguinte princípio:

        S(f) : transformada de fourier -> a + bi
        S(f)* : transformada de fourier conjugada -> a - bi

        Saída : sqrt(S(f).S(f)*) -> sqrt(a² + b²)

        Parameters
        ----------

        None
        
        Returns
        -------
        None
        """

        # Todo: verificar unidades do dado de entrada e saída da FFT

        # Definindo o valor da amplitude de FFT
        self.fourier_transform = fft(self.data)[0:self.length//2]
        self.fourier_conjugado = np.conj(self.fourier_transform)
        self.eixo_y_fourier = np.sqrt(self.fourier_transform*self.fourier_conjugado)

        # Tornando os n primeiros pontos nulos, pois há um ruído grande em frequências próximas a 0 Hz
        primeiros_pontos = 2
        self.eixo_y_fourier[0:primeiros_pontos] = np.zeros(primeiros_pontos)
        self.eixo_freq = fftfreq(self.length,self.T)[0:self.length//2]
        
        # Definindo os eixos x e y após aplicação da transformada
        self.eixo_y_fourier = np.real(self.eixo_y_fourier)
        self.eixo_freq = np.real(self.eixo_freq)
        self.eixo_freq = self.eixo_freq/self.rpm

    def plot_frequency_domain(self,freq_referencia,no_ordens = 1):
        """
        plot_frequency_domain() é um método da Classe FrequencyFeaturesExtraction() 
        que tem por objetivo plotar o gráfico da FFT.

        Parameters
        ----------

        freq_referencia : float -> frequência a qual o gráfico será centrado
        no_ordens : integer -> número de ordens que deverão ser apresentadas
        
        Returns
        -------
        None
        """

        self.run_fft()

        plt.plot(self.eixo_freq, self.eixo_y_fourier)
        plt.title('Domínio da Frequência')
        plt.xlabel('Frequency (Hz)')
        plt.ylabel('Amplitude')

        # Criando linhas verticais centradas em cada ordem
        for i in range(no_ordens):
            plt.vlines(freq_referencia*(i+1)/self.rpm,self.ymin,self.ymax,'red','dashed')

        plt.grid(True)
        plt.show()

    def window_around_frequency(self,freq_referencia,tamanho_janela_hz = 4):
        """
        window_around_frequency() é um método da Classe FrequencyFeaturesExtraction() 
        que tem por objetivo criar uma banda em torno de uma frequência.
        Esta banda tem uma largura definida.

        Parameters
        ----------

        freq_referencia : float -> frequência a qual a janela / banda será centrada
        tamanho_janela_hz : float -> largura da banda
        
        Returns
        -------
        janela_fourier : data : (N,) array_like -> array do intervalo da janela
        """

        # Todo: verificar, linha a linha, se o processo de criação de janela está correto
        # Todo: Entender e corrigir o motivo da modificação do tamanho_janela_hz não alterar o resultado

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

    def plot_window(self,freq_referencia,tamanho_janela_hz = 4):

        """
        plot_window() é um método da Classe FrequencyFeaturesExtraction() 
        que tem por objetivo criar um gráfico da banda centrada na frequência de referência

        Parameters
        ----------

        freq_referencia : float -> frequência a qual a janela / banda será centrada
        tamanho_janela_hz : float -> largura da banda
        
        Returns
        -------
        None
        """

        self.window_around_frequency(freq_referencia,tamanho_janela_hz)

        plt.plot(self.janela_freq,self.janela_fourier)
        plt.vlines(freq_referencia/self.rpm,self.ymin,self.ymax,'red','dashed')
        plt.ylim((self.ymin,self.ymax))
        plt.show()

    def get_features(self,freq_referencia,tamanho_janela_hz = 4,no_ordens = 1):
        """
        get_features() é um método da Classe FrequencyFeaturesExtraction() 
        que tem por objetivo extrair um indicador relevante dos dados de entrada.
        Este indicador é extraído no domínio da frequência, e sinaliza a energia contida dentro da banda.

        Parameters
        ----------

        freq_referencia : float -> frequência a qual a janela / banda será centrada
        tamanho_janela_hz : float -> largura da banda
        no_ordens : integer -> número de ordens que se quer utilizar para extrair o indicador

        Returns
        -------
        data_jason : dic -> dicionário que contém o indicador
        """

        # Todo: modificar todo esse trecho de código para que o feature extraído seja a soma da energia dentro da banda/janela


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
 
