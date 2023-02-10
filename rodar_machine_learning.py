from sklearn.model_selection import train_test_split
from sklearn import svm
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

import models
from models import data_vis, ml_functions

from sklearn.ensemble import RandomForestClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC, NuSVC
from sklearn.tree import DecisionTreeClassifier

import os
from rich import pretty, print

os.system("cls")

pretty.install()

# Carrega os dados, ignorando a primeira linha
dados_normalizados = 'Dados_Normalizados.csv'
dados_extraidos_geral = 'dados_extraidos_concatenado.csv'
dado_sensor = 'dados_extraidos_rolamento_interno_radial1.csv'

seed = 15
score_RandomForest = {}
score_KNN = {}
score_DecisionTree = {}

for ordem in range(11)[1:11]:
    pasta = f'{models.path_dados_tratados}/ordens_{ordem}/{dados_normalizados}'
    df = pd.read_csv(pasta, header=0)


    score = {}


    # Executa a predição
    classifier = ml_functions.Classifier(data = df, classifier=RandomForestClassifier, random_state = seed,ordem=ordem)
    classifier.run()
    score[f'{classifier.classifier.__class__.__name__}'] = round(classifier.score * 100,2)
    score_RandomForest[f'Ordem {ordem}'] = round(classifier.score * 100,2)

    data_vis.MatrizConfusao(classifier, method_name = f'{classifier.classifier.__class__.__name__} - {ordem}º Ordem', ordem=ordem).plot_confusion_matrix()



    classifier = ml_functions.Classifier(data = df, classifier=KNeighborsClassifier,ordem=ordem)
    classifier.run()
    score[f'{classifier.classifier.__class__.__name__}'] = round(classifier.score * 100,2)
    score_KNN[f'Ordem {ordem}'] = round(classifier.score * 100,2)
    
    data_vis.MatrizConfusao(classifier, method_name = f'{classifier.classifier.__class__.__name__} - {ordem}º Ordem', ordem=ordem).plot_confusion_matrix()



    classifier = ml_functions.Classifier(data = df, classifier=DecisionTreeClassifier, criterion = 'entropy',ordem=ordem)
    classifier.run()
    score[f'{classifier.classifier.__class__.__name__}'] = round(classifier.score * 100,2)
    score_DecisionTree[f'Ordem {ordem}'] = round(classifier.score * 100,2)

    data_vis.MatrizConfusao(classifier, method_name = f'{classifier.classifier.__class__.__name__} - {ordem}º Ordem', ordem=ordem).plot_confusion_matrix()



    data_vis.ComparacaoDeAcuracias().plot_score(ordem,score)
    score = 0
    score = {}
    print(f'Ordem {ordem} finalizada!\n\n')

data_vis.ComparacaoDeAcuracias().plot_ordens('Comparação de Acurácia - Random Forest Classifier',score_RandomForest)
data_vis.ComparacaoDeAcuracias().plot_ordens('Comparação de Acurácia - KNeighbours Classfier',score_KNN)
data_vis.ComparacaoDeAcuracias().plot_ordens('Comparação de Acurácia - Decision Tree Classifier',score_DecisionTree)

breakpoint()