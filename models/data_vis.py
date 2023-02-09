import os

# import graphviz
import numpy as np
import seaborn as sns
from matplotlib import pyplot as plt
from numpy import arange
from pandas import DataFrame
from sklearn.metrics import ConfusionMatrixDisplay
from sklearn.tree import export_graphviz

from models import defeitos, frequency_rate_dict, x_columns
import models

# font = {'family' : 'normal',
#     'weight' : 'bold',
#     'size'   : 5}
# plt.rc('font', **font)


def create_images_dir(ordem):
    dir_path = os.path.join(f'{models.path_dados_tratados}/ordens_{ordem}')
    if not os.path.exists(dir_path):
        os.mkdir(dir_path)
    return dir_path


class RawVisualization():
    def __init__(self,raw_data,fault,ordem):

        self.raw_data = raw_data
        self.fault = fault
        frequency_rate = frequency_rate_dict.get(fault)
        self.N = len(self.raw_data)
        self.tempo_total = self.N/frequency_rate
        self.ordem = ordem

    def plt_raw_data(self):
        self.vetor_tempo = np.linspace(0,self.tempo_total,self.N)
        plt.plot(self.vetor_tempo,self.raw_data)
        plt.title(f"Dados Brutos - {self.fault}")
        plt.ylabel("Amplitude [gs]")
        plt.savefig(F"{create_images_dir(self.ordem)}/raw_data.png")
        plt.show()

class MatrizConfusao():

    def __init__(self, classifier, method_name,ordem) -> None:
        self.classifier = classifier
        self.title = method_name
        self.ordem = ordem

    def plot_confusion_matrix(self,plotar:bool=False):

        disp = ConfusionMatrixDisplay.from_estimator(
            self.classifier.fit_classifier,
            self.classifier.x_test,
            self.classifier.y_test,
            display_labels=range(1,len(defeitos)+1),
            cmap=plt.cm.Blues,
            normalize='true',xticks_rotation='horizontal',
            values_format='.1%',
            text_kw={'size':5}
        )
        disp.ax_.set_title(f"Matriz de Confusão - {self.title}")
        disp.ax_.set_xlabel('Categoria Prevista', fontsize=14)
        disp.ax_.set_ylabel('Categoria Real', fontsize=14)
        # breakpoint()
        disp.ax_.tick_params(labelsize=5)
        
        plt.savefig(F"{create_images_dir(self.ordem)}/{self.title}.png",dpi=600)

        if plotar:
            plt.show()
        plt.close()

class ComparacaoDeAcuracias:
    def plot_score(self, ordem, score,plotar:bool=False):
        ax = sns.barplot(x=arange(len(score)), y=list(score.values()), hue=list(score.keys()), dodge=False)
        for i in ax.containers:
            ax.bar_label(i,)
        plt.title("Comapração entre a acurácia dos algoritmos")
        plt.legend(loc='lower right', fontsize='x-small')
        plt.savefig(F"{create_images_dir(ordem)}/Comparacao_Scores_Ordem_{ordem}.png",dpi=600)
        if plotar:
            plt.show()
        plt.close()
