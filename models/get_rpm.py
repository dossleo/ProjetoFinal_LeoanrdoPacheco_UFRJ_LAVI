import os

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


class GetRPM():
    """
    Classe GetRPM() é uma classe que tem por objetivo extrair 
    o valor de rpm a partir de dados de um sinal de um sensor de rotação

    Parameters
    ----------

    data : array like -> array coluna referente ao sinal do sensor de rotação
    freq_arquisicao : integer -> frequência de aquisição dos dados de rotação

    Returns
    -------
    None
    """

    def __init__(self,data,freq_aquisicao):
        self.data = np.array(data)
        self.data = np.abs(self.data-np.mean(self.data))
        self.freq_aquisicao = freq_aquisicao

    def generate_impulse(self):
        """
        generate_impulse() é um método da Classe GetRPM() 
        que tem por objetivo amplificar as diferenças entre um sinal 0 de um sinal 1
        Essa amplificação facilita a identificação da captação do sinal de rotação do eixo.

        Parameters
        ----------

        None

        Returns
        -------
        None
        """

        self.data = np.power(self.data,4)
        self.max = np.max(self.data)

    def cut_off(self):
        """
        cut_off() é um método da Classe GetRPM() 
        que tem por objetivo definir uma amplitude mínima para se considerar uma ativação válida do sensor.
        esta amplitude mínima servirá como filtro.

        Parameters
        ----------

        None

        Returns
        -------
        self.data : array like -> array com os dados brutos do sensor de rotação
        """

        self.generate_impulse()
        self.cutoff = self.max/2
        for i in range(len(self.data)):
            if self.data[i] < self.cutoff:
                self.data[i] = 0

        self.data = np.power(self.data,0.25)
        self.cutoff = self.cutoff**(0.25)
     
        return self.data

    def square_wave(self):
        """
        square_wave() é um método da Classe GetRPM() 
        que tem por objetivo filtrar os dados brutos do sensor, 
        visando deixar mais evidente os pontos de contagem de rotação.

        Parameters
        ----------

        None

        Returns
        -------
        self.data : arrau like -> array coluna contendo a amplitude filtrada do sensor de rotação
        """

        self.data = self.cut_off()
        self.max = np.max(self.data)

        janela = 8
        janela = int(janela)

        for i in range(len(self.data)):
            if self.data[i] > self.cutoff:
                self.data[i-janela:i] = self.max
            else:
                self.data[i] = 0

        return self.data


    def get_rpm_medio(self):
        """
        get_rpm_medio() é um método da Classe GetRPM() 
        que tem por objetivo extrair o rpm médio da máquina no intervalo medido

        Parameters
        ----------

        None

        Returns
        -------
        np.mean(self.rpms) : float -> valor float do rpm médio
        """

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
        """
        get_rpm_ponto_a_ponto() é um método da Classe GetRPM() 
        que tem por objetivo identificar o valor de rpm em cada ponto.
        Este valor contém aproximações entre os picos do sensor de rotação, 
        visto que o sinal de rotação não é contínuo.

        Parameters
        ----------

        None

        Returns
        -------
        self.rpm : array like -> array coluna contendo o valor de rpm em cada ponto de medição
        """

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
        """
        plot_picos() é um método da Classe GetRPM() 
        que tem por objetivo exibir graficamente o array extraído 
        no método get_rpm_ponto_a_ponto

        Parameters
        ----------

        None

        Returns
        -------
        None
        """

        self.data = self.square_wave()

        plt.plot(range(len(self.data)),self.data)
        plt.ylim((0,np.max(self.data)*1.5))
        plt.show()

    def plot_rpm(self):
        """
        plot_rpm() é um método da Classe GetRPM() 
        que tem por objetivo exibir graficamente o valor constante 
        do rpm médio utilizando o método get_rpm_medio

        Parameters
        ----------

        None

        Returns
        -------
        None
        """

        self.data = self.get_rpm_ponto_a_ponto()
        plt.plot(range(len(self.data)),self.data)
        plt.ylim((0,np.max(self.data)*1.5))
        plt.show()


    

