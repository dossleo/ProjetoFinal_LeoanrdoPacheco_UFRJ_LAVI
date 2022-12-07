import os

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


class GetRPM():
    def __init__(self,data,freq_aquisicao):
        self.data = np.array(data)
        self.data = np.abs(self.data-np.mean(self.data))
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

        self.data = np.power(self.data,0.25)
        self.cutoff = self.cutoff**(0.25)
     
        return self.data

    def square_wave(self):
        self.data = self.cut_off()
        self.max = np.max(self.data)

        janela = 8
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

        self.picos = self.picos
        return np.mean(self.rpms)

    def get_rpm_ponto_a_ponto(self):
        self.data = self.square_wave()

        self.picos = []
        self.rpms = []
            
        for i in range(len(self.data)):
            if self.data[i] > self.cutoff and self.data[i+1] == 0:
                self.picos.append(i)

        for j in range(0,len(self.picos)-1):
            self.rpms.append(self.picos[j+1]-self.picos[j])
        
        self.rpm = np.zeros(len(self.data))

        self.rpm[0:self.picos[0]] = self.rpms[0]
        self.rpm[self.picos[-1]:len(self.rpm)] = self.rpms[-1]

        for k in range(0,len(self.rpms)):
            self.rpm[self.picos[k]:self.picos[k+1]] = self.rpms[k]

        return self.rpm


    def plot_picos(self):
        self.data = self.square_wave()

        plt.plot(range(len(self.data)),self.data)
        plt.ylim((0,np.max(self.data)*1.5))
        plt.show()

    def plot_rpm(self):
        self.data = self.get_rpm_ponto_a_ponto()
        plt.plot(range(len(self.data)),self.data)
        plt.ylim((0,np.max(self.data)*1.5))
        plt.show()


    

