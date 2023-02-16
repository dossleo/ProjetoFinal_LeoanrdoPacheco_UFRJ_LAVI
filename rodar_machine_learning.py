from sklearn.model_selection import train_test_split
from sklearn import svm
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

import models
from models import ml_functions

from sklearn.ensemble import RandomForestClassifier
from sklearn.neural_network import MLPClassifier
from sklearn.linear_model import SGDClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC, NuSVC
from sklearn.tree import DecisionTreeClassifier

import os
import datetime
import time
from rich import pretty, print

from models import visualizar_dados

os.system("cls")

pretty.install()

def iniciar_contagem():
        start = time.time()
        now = datetime.datetime.now()
        now = now.strftime("%d/%m/%Y - %H:%M:%S")

        print(f'___________________________\nInício: {now}\n')
        return start

def tempo_decorrido(start, ciclo_atual, ciclos_totais,harmonico):
        elapsed_time = time.time() - start

        # Evita divisão por zero
        if ciclo_atual > 0:
                tempo_estimado = elapsed_time*((ciclos_totais/ciclo_atual)-1)
        else:
                tempo_estimado = 0
                
        print(f'Harmônico: {harmonico}\nAndamento Total: {np.round(100*ciclo_atual/ciclos_totais,2)}%')
        print("Tempo decorrido: {:02}:{:02}:{:02}".format(int(elapsed_time // 3600), int(elapsed_time % 3600 // 60), int(elapsed_time % 60)))
        print("Tempo Estimado até o Fim: {:02}:{:02}:{:02}\n\n".format(int(tempo_estimado // 3600), int(tempo_estimado % 3600 // 60), int(tempo_estimado % 60)))


harmonico_inicial = 1
harmonico_final = 10

# Nome dos dados normalizados
dados_normalizados = 'Dados_Normalizados.csv'

# Criação de dicionários para comparação de acurácias entre as harmonicos
score_RandomForest = {}
score_KNN = {}
score_DecisionTree = {}
score_rede = {}

redes = [
        (128,),
        (128,128),
        (64,128,64),
        # (64,128,128,64),
        # (256,128,64),
        # (64,128,256),
        (128,128,128),
        # (128,256,128),
        # (256,512,256)
        ]

ciclos_totais = (len(redes)+3)*harmonico_final
ciclo_atual = 0


start = iniciar_contagem()


# Loop percorrendo 10 harmonicos
for harmonico in range(harmonico_final+1)[harmonico_inicial:harmonico_final+1]:
        local_arquivo = f'{models.path_dados_tratados}/harmonicos_{harmonico}/{dados_normalizados}'
        df = pd.read_csv(local_arquivo, header=0)

        # Dicionário para comparar acurácia entre os métodos
        score = {}


        # Loop para percorrer e executar o aprendizado das redes neurais artificiais
        for rede in redes:
                legenda_rede =  f'Camadas Ocultas da rede {rede}'
        # Instanciando o classificador
                classifier = ml_functions.Classifier(data = df, classifier=MLPClassifier,harmonico=harmonico,test_size=0.2,
                        rede_oculta=f' - {rede}',
                        hidden_layer_sizes=rede, 
                        activation='relu', 
                        solver='adam', 
                        alpha=0.0001, 
                        batch_size='auto', 
                        learning_rate='constant', 
                        learning_rate_init=0.01, 
                        power_t=0.5, 
                        max_iter=500, 
                        shuffle=True, 
                        random_state=models.seed, 
                        tol=0.0001, 
                        verbose=False, 
                        warm_start=False, 
                        momentum=0.9, 
                        nesterovs_momentum=True, 
                        early_stopping=False, 
                        validation_fraction=0.1, 
                        beta_1=0.9, 
                        beta_2=0.999, 
                        epsilon=1e-08, 
                        n_iter_no_change=10, 
                        max_fun=15000)
        
                # Realizando a classificação
                classifier.run()

                # Guardando o valor da acurácia no dicionário score
                score[f'{classifier.classifier.__class__.__name__} - {rede}'] = round(classifier.score * 100,2)
                # Guardando o valor da acurácia no dicionário referente ao classificador
                score_rede[f'{harmonico} harmonicos - {rede}'] = round(classifier.score * 100,2)
                # Salvando a matriz de confusão    
                visualizar_dados.MatrizConfusao(classifier, 
                                                method_name = f'{classifier.classifier.__class__.__name__} - {harmonico} harmonicos', 
                                                harmonico=harmonico,
                                                legenda_rede=legenda_rede).plot_confusion_matrix(plotar=False, salvar=True)


                ciclo_atual+=1
                tempo_decorrido(start,ciclo_atual,ciclos_totais,harmonico)
                

        # Início do aprendizado de máquina de outros classificadores
        
        # Instanciando o classificador
        classifier = ml_functions.Classifier(data = df, classifier=RandomForestClassifier, random_state = models.seed,harmonico=harmonico)
        # Realizando a classificação
        classifier.run()

        # Guardando o valor da acurácia no dicionário score
        score[f'{classifier.classifier.__class__.__name__}'] = round(classifier.score * 100,2)
        # Guardando o valor da acurácia no dicionário referente ao classificador
        score_RandomForest[f'{harmonico} harmonicos'] = round(classifier.score * 100,2)
        # Salvando a matriz de confusão    
        visualizar_dados.MatrizConfusao(classifier, method_name = f'{classifier.classifier.__class__.__name__} - {harmonico} harmonicos', harmonico=harmonico).plot_confusion_matrix(plotar=False, salvar=True)

        ciclo_atual+=1
        tempo_decorrido(start,ciclo_atual,ciclos_totais,harmonico)



        # Instanciando o classificador
        classifier = ml_functions.Classifier(data = df, classifier=KNeighborsClassifier,harmonico=harmonico)
        # Realizando a classificação
        classifier.run()

        # Guardando o valor da acurácia no dicionário score
        score[f'{classifier.classifier.__class__.__name__}'] = round(classifier.score * 100,2)
        # Guardando o valor da acurácia no dicionário referente ao classificador
        score_KNN[f'{harmonico} harmonicos'] = round(classifier.score * 100,2)
        # Salvando a matriz de confusão        
        visualizar_dados.MatrizConfusao(classifier, method_name = f'{classifier.classifier.__class__.__name__} - {harmonico} harmonicos', harmonico=harmonico).plot_confusion_matrix(plotar=False, salvar=True)

        ciclo_atual+=1
        tempo_decorrido(start,ciclo_atual,ciclos_totais,harmonico)



        # Instanciando o classificador
        classifier = ml_functions.Classifier(data = df, classifier=DecisionTreeClassifier, criterion = 'entropy',harmonico=harmonico)
        # Realizando a classificação
        classifier.run()

        # Guardando o valor da acurácia no dicionário score
        score[f'{classifier.classifier.__class__.__name__}'] = round(classifier.score * 100,2)
        # Guardando o valor da acurácia no dicionário referente ao classificador
        score_DecisionTree[f'{harmonico} harmonicos'] = round(classifier.score * 100,2)
        # Salvando a matriz de confusão    
        visualizar_dados.MatrizConfusao(classifier, method_name = f'{classifier.classifier.__class__.__name__} - {harmonico} harmonicos', harmonico=harmonico).plot_confusion_matrix(plotar=False, salvar=True)

        ciclo_atual+=1
        tempo_decorrido(start,ciclo_atual,ciclos_totais,harmonico)


        # Plotando o gráfico de barras comparando a acurácia
        visualizar_dados.ComparacaoDeAcuracias().plot_score(harmonico,score)

        # Zerando o score para limpar a memória
        score = 0
        score = {}
        print(f'Harmônico {harmonico} finalizado!\n\n')

# Salvando o gráfico de barras comparando a acurácia de diferentes harmonicos
visualizar_dados.ComparacaoDeAcuracias().plot_harmonicos('Comparação de Acurácia - Random Forest Classifier',score_RandomForest, 
        plotar=False, 
        salvar=True)
visualizar_dados.ComparacaoDeAcuracias().plot_harmonicos('Comparação de Acurácia - KNeighbours Classfier',score_KNN, 
        plotar=False, 
        salvar=True)
visualizar_dados.ComparacaoDeAcuracias().plot_harmonicos('Comparação de Acurácia - Decision Tree Classifier',score_DecisionTree, 
        plotar=False, 
        salvar=True)

for rede in redes:
        dicionario_filtrado = {chave: valor for chave, valor in score_rede.items() if f'{rede}' in chave}
        visualizar_dados.ComparacaoDeAcuracias().plot_harmonicos(f'Comparação de Acurácia - Rede Neural {rede}',dicionario_filtrado, 
                plotar=False, 
                salvar=True)

breakpoint()