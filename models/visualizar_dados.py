import os

# import graphviz
import numpy as np
import seaborn as sns
from matplotlib import pyplot as plt
from numpy import arange
from pandas import DataFrame
from sklearn.metrics import ConfusionMatrixDisplay
from sklearn.tree import export_graphviz

import models
from models import get_raw_data,get_rpm, indicadores_frequencia

# Função para cirar um diretório para as imagens
def create_images_dir(harmonico):
    dir_path = os.path.join(f'{models.path_dados_tratados}/harmonicos_{harmonico}')
    if not os.path.exists(dir_path):
        os.mkdir(dir_path)
    return dir_path


# Classe para visualização dos dados brutos
class RawVisualization():
    def __init__(self,sinal,fault,harmonico,title):

        self.sinal = sinal
        self.fault = fault
        self.title = title

        # Frequência de aquisição
        freq_aquisicao = models.freq_aquisicao

        # Número de pontos do sinal
        self.N = len(self.sinal)
        self.tempo_total = self.N/freq_aquisicao
        self.harmonico = harmonico

    def plt_sinal(self):
        self.vetor_tempo = np.linspace(0,self.tempo_total,self.N)
        plt.plot(self.vetor_tempo,self.sinal)
        plt.title(f"Dados Brutos - {self.title}")
        plt.ylabel("Amplitude [gs]")
        plt.savefig(F"{models.path_dados_tratados}/sinal_bruto_{self.title}.png")
        plt.show()

class VisualizarFrequencia:
    def __init__(self, pasta:str,arquivo:str,numero_sensor=1,posicao='interno',num_frequencia_referencia:int=0) -> None:
        self.pasta = pasta
        self.arquivo = arquivo   
        self.posicao = posicao
        self.numero_sensor = numero_sensor
        self.sensor = f'rolamento_{self.posicao}_radial{self.numero_sensor}'
        self.coluna = models.sensores[self.sensor]
        self.frequencias_rolamento = models.frequencias_rolamento
        self.num_frequencia_referencia = num_frequencia_referencia
        self.pegar_rpm()


    def pegar_sinal(self):
        self.sinal = get_raw_data.GetData(self.pasta,self.arquivo,self.coluna).Get()
        self.sinal_rpm = get_raw_data.GetData(self.pasta,self.arquivo,0).Get()

    def pegar_rpm(self):
        self.pegar_sinal()
        self.rpm = get_rpm.GetRPM(sinal_rpm=self.sinal_rpm,sinal_sensor=self.sinal).get_rpm_medio()
        self.largura_banda = self.rpm

    def pegar_frequencia_de_referencia(self):
        frequencia_de_referencia=[]
        for rolamento in self.frequencias_rolamento:
            if self.sensor.__contains__(rolamento):
                frequencia_de_referencia = self.frequencias_rolamento[rolamento]
                break

        for i in range(len(frequencia_de_referencia)):
            frequencia_de_referencia[i] = frequencia_de_referencia[i]*self.rpm

        return frequencia_de_referencia[self.num_frequencia_referencia]
    
    def definir_objeto(self):
        self.Objeto_Frequencia = indicadores_frequencia.DominioFrequencia(self.sinal,self.rpm)

    def plotar_fft(self,salvar=True,plotar=True):
        self.definir_objeto()
        self.Objeto_Frequencia.plot_fft(title=f'Sinal do sensor {self.posicao} número {self.numero_sensor} no domínio da frequência',
                                        salvar=salvar,
                                        plotar=plotar)

    def plotar_fft_com_frequencia_de_referencia(self,salvar=True,plotar=True):
        self.definir_objeto()
        freq = self.pegar_frequencia_de_referencia()
        self.Objeto_Frequencia.plot_fft(freq_referencia=freq,
                                        title=f'Frequência = {np.round(freq,1)}Hz',
                                        salvar=salvar,plotar=plotar)

    def plotar_bandas(self,num_harmonicos=10,salvar=True,plotar=True):
        self.definir_objeto()
        self.Objeto_Frequencia.plot_banda(self.rpm,self.rpm,title=f'- Rotação da Máquina = {np.round(self.rpm,1)}Hz')

        freq = self.pegar_frequencia_de_referencia()

        for harmonico in range(1,num_harmonicos+1):
            self.Objeto_Frequencia.plot_banda(  freq*(harmonico),
                                                self.rpm,
                                                title=f'Frequência = {np.round(freq,1)}Hz - {harmonico}º Harmônico a rotação de {np.round(self.rpm,1)}Hz',
                                                salvar=salvar,
                                                plotar=plotar)


# Classe para gerar a matriz de confusão e relatório de scores de um método
class MatrizConfusao():

    def __init__(self, classifier, method_name,harmonico) -> None:
        self.classifier = classifier
        self.title = method_name
        self.harmonico = harmonico

    def plot_confusion_matrix(self,plotar:bool=False,salvar=True):
        # Criando matriz de confusão
        disp = ConfusionMatrixDisplay.from_estimator(
            self.classifier.fit_classifier,
            self.classifier.x_test,
            self.classifier.y_test,

            # Label dos eixos como números de 1 a 16
            display_labels=range(1,len(models.defeitos)+1),

            # Cor da matriz
            cmap=plt.cm.Blues,
            normalize='true',

            # Orientação dos valores do eixo x
            xticks_rotation='horizontal',

            # Formato da porcentagem da matriz
            values_format='.1%',

            # Tamanho da fonte da porcentagem da matriz
            text_kw={'size':6}
        )

        # Configurando tamanho da imagem
        fig = disp.ax_.get_figure()
        fig.set_figwidth(7)
        fig.set_figheight(7)
        
        
        # Configurando título de labels
        disp.ax_.set_title(f"Matriz de Confusão - {self.title}")
        disp.ax_.set_xlabel('Categoria Prevista', fontsize=13)
        disp.ax_.set_ylabel('Categoria Real', fontsize=13)
        disp.ax_.tick_params(labelsize=5)
        
        # Condicional para salvar
        if salvar:
            plt.savefig(F"{create_images_dir(self.harmonico)}/{self.title}.png",dpi=600)

        # Condicional para plotar
        if plotar:
            plt.show()
        
        # Fechar figura para liberar memória
        plt.close()

# Classe para criar gráfico de barra
class ComparacaoDeAcuracias:
    # Método para criar gráfico de barras para comparar diferentes classificadores
    def plot_score(self, harmonico, score,plotar:bool=False,salvar=True):
        
        # Criando o gráfico de barras
        ax = sns.barplot(x=arange(len(score)), y=list(score.values()), hue=list(score.keys()), dodge=False)
        for i in ax.containers:
            ax.bar_label(i,)

        # Configurando o tamanho da imagem
        fig = ax.get_figure()
        fig.set_figwidth(7)
        fig.set_figheight(7)

        # Configurando título e legenda da imagem
        plt.title("Comapração entre a acurácia dos algoritmos")
        plt.legend(loc='lower right', fontsize='x-small')
        plt.ylabel('Acurácia [%]')

        # Condicional para salvar 
        if salvar:
            plt.savefig(f"{create_images_dir(harmonico)}/Comparacao_Scores_harmonico_{harmonico}.png",dpi=600)
        
        # Condicional para plotar
        if plotar:
            plt.show()
        
        # Fechar imagem para liberar memória
        plt.close()

    # Método para criar gráfico de barras para comparar um mesmo método em várias harmonicos
    def plot_harmonicos(self, title:str, score,plotar:bool=False,salvar=True):
        
        # Criando gráfico de barras
        ax = sns.barplot(x=arange(len(score)), y=list(score.values()), hue=list(score.keys()), dodge=False)
        for i in ax.containers:
            ax.bar_label(i,)

        # Setando o tamanho da figura
        fig = ax.get_figure()
        fig.set_figwidth(7)
        fig.set_figheight(7)

        # Setando título e legenda
        plt.title(title)
        plt.legend(loc='lower right', fontsize='x-small')
        plt.ylabel('Acurácia [%]')

        # Condicional para salvar
        if salvar:
            plt.savefig(F"{models.path_dados_tratados}/Comparacao_Scores_{title}.png",dpi=600)
        
        # Condicional para plotar
        if plotar:
            plt.show()

        # Fechar imagem para limpar a memória
        plt.close()

