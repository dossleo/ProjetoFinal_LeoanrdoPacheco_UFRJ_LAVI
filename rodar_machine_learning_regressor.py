from sklearn.model_selection import train_test_split

import pandas as pd
import numpy as np

import models
from models import ml_functions_regressor

from sklearn.neural_network import MLPRegressor
from sklearn.svm import SVR
from sklearn.neighbors import KNeighborsRegressor
from sklearn.linear_model import Ridge
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.tree import DecisionTreeRegressor

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
                
        print(f'\nHarmônico: {harmonico}\nAndamento Total: {np.round(100*ciclo_atual/ciclos_totais,2)}%')
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
        (256,),
        (128,128),
        (64,128,64),
        (256,128,64),
        (64,128,256),
        (64,128,128,64),
        (128,128,128),
        (128,256,128),
        (128,256,256,128),
        (256,512,256)
        # (512,1024,1024,512)
        ]

ciclos_totais = (len(redes)+3)*(harmonico_final-harmonico_inicial+1)
ciclo_atual = 0


colunas = models.colunas_pot


start = iniciar_contagem()


# Loop percorrendo 10 harmonicos
for harmonico in range(harmonico_final+1)[harmonico_inicial:harmonico_final+1]:
        arquivo = f'{models.path_dados_tratados}/harmonicos_{harmonico}/{dados_normalizados}'
        df = pd.read_csv(arquivo, header=0)
        
        df = df[colunas]


        # Dicionário para comparar acurácia entre os métodos
        score = {}


        # Loop para percorrer e executar o aprendizado das redes neurais artificiais
        for rede in redes:
                legenda_rede =  f'Camadas Ocultas da rede {rede}'
        # Instanciando o regressor
                regressor = ml_functions_regressor.Regressor(data = df,colunas=colunas ,regressor=MLPRegressor,harmonico=harmonico,test_size=0.2,
                        rede_oculta=f' - {rede}',
                        hidden_layer_sizes=rede, 
                        activation='relu',
                        solver='adam', 
                        alpha=0.0001, 
                        batch_size='auto', 
                        learning_rate='constant', 
                        learning_rate_init=0.001, 
                        power_t=0.5, 
                        max_iter=500, 
                        shuffle=True, 
                        random_state=None, 
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
        
                # Realizando a regressão
                regressor.run()


                ciclo_atual+=1
                tempo_decorrido(start,ciclo_atual,ciclos_totais,harmonico)
        # breakpoint()
                

        # Início do aprendizado de máquina de outros regressores
        
        # # Instanciando o regressor
        regressor = ml_functions_regressor.Regressor(data = df, colunas=colunas, regressor=RandomForestRegressor, random_state = models.seed,harmonico=harmonico)
        # Realizando a regressão
        regressor.run()


        ciclo_atual+=1
        tempo_decorrido(start,ciclo_atual,ciclos_totais,harmonico)



        # Instanciando o regressor
        regressor = ml_functions_regressor.Regressor(data = df, colunas=colunas, regressor=KNeighborsRegressor,harmonico=harmonico,n_neighbors=1)
        # Realizando a regressão
        regressor.run()

        ciclo_atual+=1
        tempo_decorrido(start,ciclo_atual,ciclos_totais,harmonico)



        # # Instanciando o regressor
        regressor = ml_functions_regressor.Regressor(data = df, colunas=colunas, regressor=DecisionTreeRegressor,harmonico=harmonico)
        # Realizando a regressão
        regressor.run()

        ciclo_atual+=1
        tempo_decorrido(start,ciclo_atual,ciclos_totais,harmonico)


        print(f'Harmônico {harmonico} finalizado!\n\n')


breakpoint()