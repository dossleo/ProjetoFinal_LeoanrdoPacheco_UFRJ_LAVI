import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

class GetRPM():
    def __init__(self,data,freq_aquisicao):
        self.data = np.array(data)
        self.freq_aquisicao = freq_aquisicao

    def generate_impulse(self):
        self.data = np.power(self.data,4)
        self.max = np.max(self.data)

    def cut_off(self):
        self.generate_impulse()
        self.cutoff = self.max/2
        for i in range(len(self.data)):
            if self.data[i] < self.cutoff:
                self.data[i] = 0
     
        return self.data

    def square_wave(self):
        self.data = self.cut_off()
        self.max = np.max(self.data)

        janela = 6
        janela = int(janela)

        for i in range(len(self.data)):
            if self.data[i] > self.cutoff:
                self.data[i-janela:i] = self.max

        return self.data


    def get_rpm_medio(self):
        self.data = self.square_wave()
        self.picos = []
        self.rpms = []

        for i in range(len(self.data)):
            if self.data[i] > self.cutoff and self.data[i+1] == 0:
                self.picos.append(i)

        for j in range(0,len(self.picos)-1):
            self.rpms.append(self.picos[j+1]-self.picos[j])

        return np.mean(self.rpms)

    def get_rpm_ponto_a_ponto(self):
        self.data = self.square_wave()
        self.rpm_meio = self.get_rpm_medio()
        
        self.rpm = np.zeros(len(self.data))

        for i in range(0,len(self.rpms)):
            self.rpm[self.picos[i]:self.picos[i+1]] = self.rpms[i]

        return self.rpm


    def plot_picos(self):
        self.data = self.square_wave()

        plt.plot(range(len(self.data)),self.data)
        plt.show()

    def plot_rpm(self):
        self.data = self.get_rpm_ponto_a_ponto()
        plt.plot(range(len(self.data)),self.data)
        plt.show()


    

