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


class IndicadoresFrequencia():
    """
    Classe IndicadoresFrequencia() tem o objetivo de fazer a análise dos dados no domínio da frequência.

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
        
        self.data = data # dados brutos
        self.label = label
        self.n_points_dado_bruto = len(self.data) # npoints
        self.rpm = rpm #rpm
        self.rotacao_hz = self.rpm/60

        duracao_seg = self.n_points_dado_bruto/models.freq_sample # duração em segundos

        self.dt = duracao_seg/models.freq_sample # dt

        self.vetor_tempo = np.linspace(0.0, duracao_seg, self.n_points_dado_bruto, endpoint=False)
        self.ymin = -200
        self.ymax = 200

        self.indicadores = models.features

    def run_fft(self):
        """
        run_fft() é um método da Classe IndicadoresFrequencia() 
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
        self.fourier_transform = fft(self.data)[0:self.n_points_dado_bruto//2] # fft aplicada nos npoints/2 pontos
        self.fourier_conjugado = np.conj(self.fourier_transform) # fft conjugada
        self.eixo_y_fourier = np.sqrt(self.fourier_transform*self.fourier_conjugado) # raiz(a^2 + b^2)

        # Tornando os n primeiros pontos nulos, pois há um ruído grande em frequências próximas a 0 Hz
        primeiros_pontos = 2
        self.eixo_y_fourier[0:primeiros_pontos] = np.zeros(primeiros_pontos)
        self.eixo_freq = fftfreq(self.n_points_dado_bruto,self.dt)[0:self.n_points_dado_bruto//2] # aplicando a fft no eixo da frequência -> Hz
        
        # Definindo os eixos x e y após aplicação da transformada
        self.eixo_y_fourier = np.real(self.eixo_y_fourier)
        self.eixo_freq = np.real(self.eixo_freq)
        self.eixo_freq = np.real(self.eixo_freq*60) # normalizando na rotação em hz

    def plot_dominio_frequencia(self,freq_referencia,no_ordens = 1):
        """
        plot_dominio_frequencia() é um método da Classe IndicadoresFrequencia() 
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

        plt.plot(np.real(self.eixo_freq), np.real(self.eixo_y_fourier))
        plt.title('Domínio da Frequência')
        plt.xlabel('Ordens')
        plt.ylabel('Amplitude')

        # Criando linhas verticais centradas em cada ordem
        for i in range(no_ordens):
            plt.vlines(freq_referencia*(i+1)/self.rotacao_hz,self.ymin,self.ymax,'red','dashed')

        plt.grid(True)
        plt.show()

    def banda_de_frequencia(self,freq_referencia,tamanho_janela_hz = 4):
        """
        banda_de_frequencia() é um método da Classe IndicadoresFrequencia() 
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
        
        self.delta_f = (self.rotacao_hz*self.eixo_freq[-1]-self.eixo_freq[0])/len(self.eixo_freq)
        print(f"self.delta_f = {self.delta_f}")


        self.tamanho_janela_samples = int((tamanho_janela_hz/self.delta_f))
        print(f"self.tamanho_janela_samples = {self.tamanho_janela_samples}")

        elemento_referencia = int(freq_referencia/self.delta_f)
        print(f"elemento_referencia = {elemento_referencia}")

        self.inicio_janela = int(elemento_referencia-self.tamanho_janela_samples/2)
        print(f"self.inicio_janela = {self.inicio_janela}")

        self.fim_janela = int(elemento_referencia+self.tamanho_janela_samples/2)
        print(f"self.fim_janela = {self.fim_janela}")

        if self.eixo_freq[0] > self.eixo_freq[self.inicio_janela]:

            self.intervalo_janela = [self.inicio_janela,self.fim_janela]
            print(f"self.intervalo_janela = {self.intervalo_janela}")

            self.janela_freq = self.eixo_freq[self.inicio_janela:self.fim_janela]
            print(f"self.janela_freq = {self.janela_freq}")

            self.janela_fourier = self.eixo_y_fourier[self.inicio_janela:self.fim_janela]
            print(f"self.janela_fourier = {self.janela_fourier}")


        else:
            
            self.intervalo_janela = [0,self.fim_janela]
            print(f"self.intervalo_janela = {self.intervalo_janela}")

            self.janela_freq = self.eixo_freq[0:self.fim_janela]
            print(f"self.janela_freq = {self.janela_freq}")

            self.janela_fourier = self.eixo_y_fourier[0:self.fim_janela]
            print(f"self.janela_fourier = {self.janela_fourier}")

        return self.janela_fourier

    def plot_banda(self,freq_referencia,tamanho_janela_hz = 4):

        """
        plot_banda() é um método da Classe IndicadoresFrequencia() 
        que tem por objetivo criar um gráfico da banda centrada na frequência de referência

        Parameters
        ----------

        freq_referencia : float -> frequência a qual a janela / banda será centrada
        tamanho_janela_hz : float -> largura da banda
        
        Returns
        -------
        None
        """

        self.banda_de_frequencia(freq_referencia,tamanho_janela_hz)

        plt.plot(self.janela_freq,self.janela_fourier)
        plt.vlines(freq_referencia/self.rotacao_hz,self.ymin,self.ymax,'red','dashed')
        plt.ylim((self.ymin,self.ymax))
        plt.show()

    def pegar_indicadores(self,freq_referencia,tamanho_janela_hz = 4,no_ordens = 1):
        """
        pegar_indicadores() é um método da Classe IndicadoresFrequencia() 
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
            dados = self.banda_de_frequencia(freq_referencia*(i+1),tamanho_janela_hz)
            # metricas_frequencia = time_features_extraction.TimeFeatures(dados)
            dicionario = {"Soma":np.sum(self.eixo_y_fourier[self.inicio_janela:self.fim_janela])}
            dicionario['ordem'] = i+1
            metricas.append(dicionario)

        self.metricas = pd.json_normalize(metricas)
        self.media = self.metricas.mean()

        for i in range(len(self.indicadores)):
            data_jason[f'{self.indicadores[i]}_{self.label}'] = self.media[i]

        return data_jason
 
