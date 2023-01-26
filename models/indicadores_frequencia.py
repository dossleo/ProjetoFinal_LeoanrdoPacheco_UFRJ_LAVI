import models
import numpy as np
import matplotlib.pyplot as plt
from models import filtro_passa_baixa

class DominioFrequencia():
    """
    Classe DominioFrequencia() tem o objetivo de fazer a análise dos dados no domínio da frequência.

    Parameters
    ----------

    data : (N,) array_like
    rpm : integer
    
    Returns
    -------
    None
    """

    def __init__(self,data,rpm,freq_sample = models.freq_sample):
        
        self.sinal = data # dados brutos
        self.n_points_dado_bruto = len(self.sinal) # npoints
        self.rpm = rpm #rpm
        self.rotacao_hz = self.rpm/60
        self.freq_sample = freq_sample

        duracao_seg = self.n_points_dado_bruto/self.freq_sample # duração em segundos

        self.dt = duracao_seg/self.freq_sample # dt

    def run_fft(self):
        """
        run_fft() é um método da Classe DominioFrequencia() 
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
        self.fft_transform = np.fft.fft(self.sinal)
        self.fft_transform_conjugado = np.conj(self.fft_transform)

        self.fft_transform = np.sqrt(self.fft_transform*self.fft_transform_conjugado)



        self.fft_frequencia = np.fft.fftfreq(len(self.sinal),d=1/self.freq_sample)

        primeiros_pontos = 1

        self.fft_transform[0:primeiros_pontos] = np.zeros(primeiros_pontos)


        self.fft_frequencia = self.fft_frequencia[0:len(self.fft_frequencia)//2]
        self.fft_transform = self.fft_transform[0:len(self.fft_transform)//2]


    def banda_frequencia(self,freq_referencia,largura = 4):
        """
        banda_de_frequencia() é um método da Classe DominioFrequencia() 
        que tem por objetivo criar uma banda em torno de uma frequência.
        Esta banda tem uma largura definida.

        Parameters
        ----------

        freq_referencia : float -> frequência a qual a janela / banda será centrada
        largura : float -> largura da banda
        
        Returns
        -------
        self.fourier_banda : array_like -> seção da amplitude de fourier referente à banda
        self.frequencia_banda : array_like -: pontos referente à banda
        """
        self.run_fft()

        banda = np.logical_and(self.fft_frequencia >= int(freq_referencia) - largura/2, self.fft_frequencia <= int(freq_referencia) + largura/2)

        self.fourier_banda = self.fft_transform[banda]
        self.frequencia_banda = self.fft_frequencia[banda]

        return self.fourier_banda, self.frequencia_banda

    def plot_banda(self,freq_referencia,largura):

        fourier_banda, frequencia_banda = self.banda_frequencia(freq_referencia,largura)
        plt.figure()
        plt.plot(frequencia_banda, np.abs(fourier_banda))
        plt.ylim((0,1.1*np.max(self.fft_transform)))
        plt.xlabel("Frequência (Hz)")
        plt.ylabel("Amplitude")
        plt.title("Banda de Frequência")
        plt.show()

    def potencia_sinal(self,sinal_fourier):

        fourier_abs = np.abs(sinal_fourier)
        self.potencia = np.sum(fourier_abs**2) / len(fourier_abs)

        return self.potencia

    def plot_potencia_sinal(self,largura):
        self.run_fft()
        for sinal in range(0,len(self.fft_transform),largura):
            potencia = self.potencia_sinal(self.fft_transform[sinal:sinal+largura])
            plt.plot(self.fft_frequencia[sinal:sinal+largura],potencia*np.ones(len(self.fft_frequencia[sinal:sinal+largura])))
        
        plt.title(f'Largura : {largura}')
        plt.show()


    def soma_sinal(self,sinal):
        return np.sum(sinal)
        