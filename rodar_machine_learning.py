from sklearn.model_selection import train_test_split
from sklearn import svm
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

import models
from models import ml_functions

from sklearn.ensemble import RandomForestClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC, NuSVC
from sklearn.tree import DecisionTreeClassifier

import os
from rich import pretty, print

from models import visualizar_dados

os.system("cls")

pretty.install()

# Nome dos dados normalizados
dados_normalizados = 'Dados_Normalizados.csv'

# Random State
seed = 15

# Criação de dicionários para comparação de acurácias entre as harmonicos
score_RandomForest = {}
score_KNN = {}
score_DecisionTree = {}

# Loop percorrendo 10 harmonicos
for harmonico in range(11)[1:11]:
    pasta = f'{models.path_dados_tratados}/harmonicos_{harmonico}/{dados_normalizados}'
    df = pd.read_csv(pasta, header=0)

    # Dicionário para comparar acurácia entre os métodos
    score = {}

    # Instanciando o classificador
    classifier = ml_functions.Classifier(data = df, classifier=RandomForestClassifier, random_state = seed,harmonico=harmonico)
    # Realizando a classificação
    classifier.run()

    # Guardando o valor da acurácia no dicionário score
    score[f'{classifier.classifier.__class__.__name__}'] = round(classifier.score * 100,2)
    # Guardando o valor da acurácia no dicionário referente ao classificador
    score_RandomForest[f'{harmonico} harmonicos'] = round(classifier.score * 100,2)
    # Salvando a matriz de confusão    
    visualizar_dados.MatrizConfusao(classifier, method_name = f'{classifier.classifier.__class__.__name__} - {harmonico} harmonicos', harmonico=harmonico).plot_confusion_matrix(plotar=False, salvar=True)


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


    # Plotando o gráfico de barras comparando a acurácia
    visualizar_dados.ComparacaoDeAcuracias().plot_score(harmonico,score)

    # Zerando o score para limpar a memória
    score = 0
    score = {}
    print(f'harmonico {harmonico} finalizada!\n\n')

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

breakpoint()