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

        self.duracao_seg = len(self.data)/self.freq_aquisicao
        self.vetor_tempo = np.linspace(0,self.duracao_seg,len(self.data))

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



    def get_rpm_ponto_a_ponto(self,unidade = 'hz'):
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

        for n in range(len(self.rpm)):
            self.rpm[n] = self.freq_aquisicao/self.rpm[n]
            # if self.rpm[n] > np.min(self.rpm)+2:
            #     self.rpm[n] = np.min(self.rpm)

        if unidade == 'rpm':
            self.rpm = self.rpm*60

        return self.rpm


    def get_rpm_medio(self,unidade = 'hz'):
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

        self.rpm = self.get_rpm_ponto_a_ponto(unidade)

        metade = len(self.rpm)//2
        janela = len(self.rpm)//10000

        self.rpm_medio = np.mean(self.rpm[metade-janela:metade+janela])

        return self.rpm_medio

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

        plt.plot(self.vetor_tempo,self.data)
        plt.ylim((0,np.max(self.data)*1.5))
        plt.show()

    def plot_rpm(self,unidade = 'hz'):
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

        rpm_ponto = self.get_rpm_ponto_a_ponto(unidade)
        plt.plot(self.vetor_tempo,rpm_ponto)
        plt.grid(True)
        plt.ylim((0,np.max(rpm_ponto)*1.5))
        plt.show()


    

