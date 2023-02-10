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

# Função para cirar um diretório para as imagens
def create_images_dir(ordem):
    dir_path = os.path.join(f'{models.path_dados_tratados}/ordens_{ordem}')
    if not os.path.exists(dir_path):
        os.mkdir(dir_path)
    return dir_path


# Classe para visualização dos dados brutos
class RawVisualization():
    def __init__(self,sinal,fault,ordem,title):

        self.sinal = sinal
        self.fault = fault
        self.title = title

        # Frequência de aquisição
        freq_aquisicao = models.freq_aquisicao

        # Número de pontos do sinal
        self.N = len(self.sinal)
        self.tempo_total = self.N/freq_aquisicao
        self.ordem = ordem

    def plt_sinal(self):
        self.vetor_tempo = np.linspace(0,self.tempo_total,self.N)
        plt.plot(self.vetor_tempo,self.sinal)
        plt.title(f"Dados Brutos - {self.title}")
        plt.ylabel("Amplitude [gs]")
        plt.savefig(F"{models.path_dados_tratados}/sinal_bruto_{self.title}.png")
        plt.show()


# Classe para gerar a matriz de confusão e relatório de scores de um método
class MatrizConfusao():

    def __init__(self, classifier, method_name,ordem) -> None:
        self.classifier = classifier
        self.title = method_name
        self.ordem = ordem

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
            plt.savefig(F"{create_images_dir(self.ordem)}/{self.title}.png",dpi=600)

        # Condicional para plotar
        if plotar:
            plt.show()
        
        # Fechar figura para liberar memória
        plt.close()

# Classe para criar gráfico de barra
class ComparacaoDeAcuracias:
    # Método para criar gráfico de barras para comparar diferentes classificadores
    def plot_score(self, ordem, score,plotar:bool=False,salvar=True):
        
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

        # Condicional para salvar 
        if salvar:
            plt.savefig(F"{create_images_dir(ordem)}/Comparacao_Scores_Ordem_{ordem}.png",dpi=600)
        
        # Condicional para plotar
        if plotar:
            plt.show()
        
        # Fechar imagem para liberar memória
        plt.close()

    # Método para criar gráfico de barras para comparar um mesmo método em várias ordens
    def plot_ordens(self, title:str, score,plotar:bool=False,salvar=True):
        
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

        # Condicional para salvar
        if salvar:
            plt.savefig(F"{models.path_dados_tratados}/Comparacao_Scores_{title}.png",dpi=600)
        
        # Condicional para plotar
        if plotar:
            plt.show()

        # Fechar imagem para limpar a memória
        plt.close()

