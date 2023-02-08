import models
import numpy as np
import matplotlib.pyplot as plt
from models import filtro_passa_baixa

class DominioFrequencia():


    def __init__(self,sinal,rpm,freq_aquisicao = models.freq_aquisicao):
        
        self.sinal = sinal # dados brutos
        self.n_points_dado_bruto = len(self.sinal) # npoints
        self.rpm = rpm #rpm
        self.rotacao_hz = self.rpm/60

        self.freq_aquisicao = freq_aquisicao

        self.frequencia_de_corte = 1000

        duracao_seg = self.n_points_dado_bruto/self.freq_aquisicao # duração em segundos

        self.dt = duracao_seg/self.freq_aquisicao # dt

    def run_fft(self,frequencia_de_corte = 0):

        # self.sinal = filtro_passa_baixa.Filtro(self.sinal,900,5).FiltroPassaBaixa()

        frequencia_de_corte = frequencia_de_corte*5
        # Todo: verificar unidades do dado de entrada e saída da FFT

        # Definindo o valor da amplitude de FFT
        self.fft_transform = np.fft.fft(self.sinal)
        self.fft_transform_conjugado = np.conj(self.fft_transform)

        self.fft_transform = np.sqrt(self.fft_transform*self.fft_transform_conjugado)



        self.fft_frequencia = np.fft.fftfreq(len(self.sinal),d=1/self.freq_aquisicao)

        primeiros_pontos = 1

        self.fft_transform[0:primeiros_pontos] = np.zeros(primeiros_pontos)

        if frequencia_de_corte == 0:
            self.fft_frequencia = self.fft_frequencia[0:len(self.fft_frequencia)//2]            
            self.fft_transform = self.fft_transform[0:len(self.fft_transform)//2]

        else:
            self.fft_frequencia = self.fft_frequencia[0:int(frequencia_de_corte)]
            self.fft_transform = self.fft_transform[0:int(frequencia_de_corte)]

        self.fft_frequencia = np.real(self.fft_frequencia)
        self.fft_transform = np.real(self.fft_transform)

    def plot_fft(self,freq_referencia = []):
        self.run_fft(2000)

        plt.plot(np.abs(self.fft_frequencia),np.abs(self.fft_transform))
        if len(freq_referencia)>0:
            # for index in freq_referencia:
            #     plt.vlines(index,0,np.max(self.fft_transform),'red','dashed')
        
            for i in range(10):
                plt.vlines(freq_referencia[0]*(i+1),0,np.max(self.fft_transform),'red','dashed')

        plt.vlines(self.rpm,0,1.1*np.max(self.fft_transform),'green','dashed')
        plt.xlabel("Frequência [Hz]")
        plt.ylabel("Amplitude")
        plt.title("Espectrograma")

        plt.show()

    def banda_frequencia(self,freq_referencia,largura = 14,no_ordens=2):

        self.run_fft() 

        erro = 0.1
        
        ordens_frequencia = list()
        ordens_fourier = list()

        for ordem in range(1,no_ordens+1):
            larg = largura*(1+erro*no_ordens)
            
            banda = np.logical_and(self.fft_frequencia >= (freq_referencia*(ordem) - larg/2), self.fft_frequencia <= (freq_referencia*(ordem) + larg/2))

            ordens_fourier.append(self.fft_transform[banda])
            ordens_frequencia.append(self.fft_frequencia[banda])

        return ordens_fourier, ordens_frequencia

    def plot_banda(self,freq_referencia,largura,title = ''):

        fourier_banda, frequencia_banda = self.banda_frequencia(freq_referencia,largura)

        plt.figure()
        plt.plot(frequencia_banda, np.abs(fourier_banda))
        plt.ylim((0,1.1*np.max(self.fft_transform)))
        plt.xlim(freq_referencia-largura,freq_referencia+largura)
        plt.xlabel("Frequência [Hz]")
        plt.ylabel("Amplitude")
        plt.title(f"Banda de Frequência {title}")
        plt.vlines(freq_referencia,0,1.1*np.max(self.fft_transform),'green','dashed')
        plt.show()

    def soma_relativa_sinal(self,lista_sinal_fourier_banda,sinal_fourier_completo):
        soma_relativa = 0
        for i in range(len(lista_sinal_fourier_banda)):
            fourier_abs = np.sum(lista_sinal_fourier_banda[i])
            soma_relativa += fourier_abs/np.sum(sinal_fourier_completo)
        return soma_relativa

    def soma_sinal(self,lista_sinal_fourier_banda):
        soma = 0
        for i in range(len(lista_sinal_fourier_banda)):
            soma += np.sum(lista_sinal_fourier_banda[i])
        return soma
        