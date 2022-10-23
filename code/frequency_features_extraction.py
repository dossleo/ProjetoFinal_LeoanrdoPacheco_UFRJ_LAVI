from msilib.schema import SelfReg
import matplotlib.pyplot as plt
import scipy.io
import numpy as np
import pandas as pd
import os
import glob
from math import sqrt
import scipy.fftpack

class Frequency_Features_Extraction():
    def __init__(self,path):
        self.path = path
        self.filename = '2004.02.12.10.32.39'
        self.dataset=pd.read_csv(os.path.join(path, self.filename), sep='\t',header=None)

        self.bearing_no = 1
        self.bearing_data = np.array(self.dataset.iloc[:,self.bearing_no-1])

        self.feature_matrix=np.zeros((1,9))

        self.length = len(self.bearing_data)

        self.freq_sample = 20480
        self.rpm = 2000

        self.time_vector = np.linspace(0,1,self.freq_sample)

        self.raw_data = np.array((self.bearing_data,self.time_vector))

        # Dados encontrados em https://www.rexnord.com/products/za2115
        self.Frequency_Fundamental_Train = 0.0072
        self.Frequency_Inner_Ring_Defect = 0.1617
        self.Frequency_Outer_Ring_Defect = 0.1217
        self.Frequency_Roller_Spin = 0.0559

        
        # Aplicando a transformada de Fourier
        self.fourier = scipy.fftpack.fft(self.raw_data)

        self.xf = self.time_vector
        self.yf = self.fourier
        self.N = self.length

        self.yf = self.yf[0,:]

        # Verificar se esta discretização da frequência está correta
        self.xf = np.linspace(0,self.freq_sample//2,self.freq_sample//2)

        # Janela de pico
        self.window = 10


        # Retirado do código em matlab

        self.k = np.linspace(0,self.N-1,self.N)                          # k é um vetor que vai de zero até N menos 1
        self.T = self.N/self.freq_sample                           # Vetor de tempo N dividido pela frequência de amostragem
    
        self.X = np.fft.fftn(self.raw_data)/self.N                      # X recebe a FFT normalizada do vetor x sobre N
        self.cutOff = (self.N//2)                 # cutOff ajusta o eixo X
        self.X = self.X[1:self.cutOff]
        self.freq = np.linspace(1,self.cutOff,self.cutOff+1)
        # figure()
        # plot(freq(1:cutOff),abs(X))        # Plota a transformada de Fourier e o valor de X em módulo

    

    def plot_fourier(self):
        self.yf = self.rms()
        self.fig, self.ax = plt.subplots()
        self.ax.plot(self.xf, np.abs(self.yf[:self.N//2]))
        plt.title('Legenda')
        plt.xlabel('Frequency (Hz)')
        plt.ylabel('Amplitude')
        plt.show()

    def PicosRPM(self):
        pass
    
    def PicosPistaExterna(self):
        pass

    def PicosPistaInterna(self):
        pass

    def PicosGaiola(self):
        pass

    def PicosRolo(self):
        pass

    def rms(self):
        self.rms_value = sqrt(sum(n*n for n in self.bearing_data[0:len(self.bearing_data)*0.01])/self.length)        
        return self.rms_value 

Teste = Frequency_Features_Extraction('C:/Users/leona/Documents/ProjetoFinal_LeonardoPacheco_UFRJ_LAVI/database/brutos/2nd_test')

Teste.plot_fourier()