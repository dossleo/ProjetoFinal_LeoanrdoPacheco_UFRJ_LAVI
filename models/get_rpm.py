import os

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import models
from models import indicadores_frequencia, get_raw_data, criar_pastas
import numpy as np
import math


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

    def __init__(self,sinal_rpm, sinal_sensor, path_to_save = f'{models.path_dados_tratados}/dados_rotacao'):

        self.path_to_save = path_to_save

        self.sinal_sensor = sinal_sensor
        self.data = np.array(sinal_rpm)
        self.sinal_rpm = self.data

        self.data = np.abs(self.data-np.mean(self.data))
        self.freq_aquisicao = models.freq_aquisicao

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

        janela = 90
        janela = int(janela)

        for i in range(len(self.data)):
            if self.data[i] > self.cutoff and i-janela > 0:
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
            
        for i in range(len(self.data)-1):
            if self.data[i] > self.cutoff and self.data[i+1] < self.cutoff and self.data[i-1] > self.cutoff:
                self.picos.append(i)

        for j in range(0,len(self.picos)-1):
            self.rpms.append(self.picos[j+1]-self.picos[j])
        
        self.rpm = np.zeros(len(self.data))

        if self.picos[0] > 0 and self.picos[0] < len(self.rpm):
            self.rpm[0:self.picos[0]] = self.rpms[0]
        
        if self.picos[-1] < len(self.rpm):
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

        porcentagem_janela = 0.35
        janela_inferior = int(porcentagem_janela*len(self.rpm))
        janela_superior = int((1-porcentagem_janela)*len(self.rpm))

        self.rpm_medio = np.mean(self.rpm[janela_inferior:janela_superior])

        sinal = self.sinal_sensor
        self.Objeto_Frequencia = indicadores_frequencia.DominioFrequencia(sinal,self.freq_aquisicao)

        self.fourier_banda, self.frequencia_banda = self.Objeto_Frequencia.banda_frequencia(self.rpm_medio,self.rpm_medio)
        indice_rpm_correto = list(self.fourier_banda[0]).index(np.max(self.fourier_banda[0]),0,-1)

        self.rpm_medio = np.abs(self.frequencia_banda[0][indice_rpm_correto])

        return self.rpm_medio

    def plot_rpm_bruto(self, salvar=True, plotar=True,title='Dados Brutos - Sensor de Rotação'):

        fig, ax = plt.subplots()
        fig.set_size_inches(14, 5)
        ax.plot(self.vetor_tempo,self.sinal_rpm)
        plt.ylim((0,np.max(self.data)*1.5))
        plt.xlabel('Tempo [s]')
        plt.ylabel('Amplitude [Volt]')
        plt.title(title)

        if salvar:
            fig.savefig(f'{criar_pastas.create_dir(self.path_to_save)}/rotacao_bruta_{title}.png',dpi=600)

        if plotar:
            plt.show()

        plt.close()
    
    
    def plot_picos(self, salvar=True, plotar=True,title='Dados de Rotação tratados'):
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
        fig, ax = plt.subplots()
        fig.set_size_inches(14, 5)
        ax.plot(self.vetor_tempo,self.data)
        plt.ylim((0,np.max(self.data)*1.5))
        plt.xlabel('Tempo [s]')
        plt.ylabel('Amplitude [Volt]')
        plt.title(title)

        if salvar:
            fig.savefig(f'{criar_pastas.create_dir(self.path_to_save)}/rotacao_bruta_{title}.png',dpi=600)

        if plotar:
            plt.show()

        plt.close()

    def plot_rpm(self,unidade = 'hz', salvar=True, plotar=True):
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
        title = f'Rotação ao longo do tempo - Rotação Média = {np.round(self.get_rpm_medio(),1)} Hz'

        fig, ax = plt.subplots()
        fig.set_size_inches(14, 5)
        ax.plot(self.vetor_tempo,rpm_ponto)
        plt.grid(True)
        plt.ylim((0,np.max(rpm_ponto)*1.5))
        plt.xlabel('Tempo [s]')
        plt.ylabel('Rotação [Hz]')
        plt.title(title)

        if salvar:
            fig.savefig(f'{criar_pastas.create_dir(self.path_to_save)}/rotacao_bruta_{title}.png',dpi=600)

        if plotar:
            plt.show()

        plt.close()

class PlotRPMPASTAS:
    def __init__(self,pasta,path_to_save = f'{models.path_dados_tratados}/graficos_rpm') -> None:
        self.path_to_save = path_to_save
        
        self.pasta = pasta
        self.arquivos = os.listdir(pasta)

    def extrai_sinal_rpm(self,index):
        sinal_rpm = get_raw_data.GetData(self.pasta,self.arquivos[index],0).Get()
        return sinal_rpm

    def extrai_sinal_sensor(self,index):
        sinal_rpm = get_raw_data.GetData(self.pasta,self.arquivos[index],1).Get()
        return sinal_rpm

    def Cria_Objeto(self,sinal_rpm,sinal_sensor):
        Objeto_RPM = GetRPM(sinal_rpm,sinal_sensor)
        return Objeto_RPM

    def extrai_medio(self,Objeto_RPM):
        rpm_medio = Objeto_RPM.get_rpm_medio('hz')
        return rpm_medio

    def plot_rpm_pasta_inteira(self, unidade = 'hz', salvar=True, plotar=True):
        

        sinal_rpm_inicial = self.extrai_sinal_rpm(0)
        sinal_sensor_inicial = self.extrai_sinal_sensor(0)

        Objeto_rpm_inicial = self.Cria_Objeto(sinal_rpm_inicial,sinal_sensor_inicial)

        rpm_medio_inicial = Objeto_rpm_inicial.get_rpm_medio('hz')
        rpms = [rpm_medio_inicial]

        for i in range(len(self.arquivos)):
            sinal_rpm = 0
            sinal_sensor = 0

            sinal_rpm = self.extrai_sinal_rpm(i)
            sinal_sensor = self.extrai_sinal_sensor(i)

            Objeto_rpm = self.Cria_Objeto(sinal_rpm,sinal_sensor)
            rpm_medio = Objeto_rpm.get_rpm_medio('hz')

            if np.abs(rpm_medio) > np.abs(rpms[-1])+3:
                rpm_medio = rpms[-1]+1

            rpms.append(rpm_medio)

        rpms.pop(0)

        title = f'Rotações dos sinais ao longo dos testes - Rotação Mínima = {np.round(np.min(rpms),1)} Hz - Rotação Máxima = {np.round(np.max(rpms),1)} Hz'
        
        fig, ax = plt.subplots()
        fig.set_size_inches(14, 5)
        ax.plot(range(len(rpms)),rpms)
        plt.grid(True)
        plt.ylim((0,np.max(rpms)*1.5))
        plt.xlabel('Número do Experimento')
        plt.ylabel('Rotação [Hz]')
        plt.title(title)
        
        if salvar:
            fig.savefig(f'{criar_pastas.create_dir(self.path_to_save)}/rotacao_bruta_{title}.png',dpi=600)

        if plotar:
            plt.show()

        plt.close()


    

