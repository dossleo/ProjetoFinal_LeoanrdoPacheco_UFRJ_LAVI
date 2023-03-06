import models
import pandas as pd
import numpy as np

import sklearn.ensemble
from sklearn.neural_network import MLPRegressor
from sklearn.svm import SVR
from sklearn.neighbors import KNeighborsRegressor
from sklearn.linear_model import Ridge
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor

from sklearn.preprocessing import MinMaxScaler
from sklearn.linear_model import LinearRegression

from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score

import os

class MethodPrepare:

    def __init__(self, data:pd.DataFrame, test_size = models.test_size) -> None:
        self.data = data
        self.x_data = self.get_x_data()
        self.y_normalizado, self.y_original = self.get_y_data()
        self.x_columns = self.data[models.colunas_x]

        self.test_size = test_size
        self.seed = models.seed

    def get_x_data(self):
        df = self.data[models.colunas_x]
        return df

    def get_y_data(self):
        defeitos = models.defeitos_gerais
        df = self.data

        y_original = df[defeitos]
        # Criando um objeto scaler para normalizar os dados
        self.scaler = MinMaxScaler()

        # Normalizando os dados de y
        y_norm = self.scaler.fit_transform(y_original)

        return y_norm, y_original

    def prepare_data(self):
        self.x_train, self.x_test, self.y_train, self.y_test = train_test_split(
            self.x_data,
            self.y_normalizado,
            test_size=self.test_size,
            random_state = self.seed,
            stratify=self.y_normalizado
        )

class Regressor(MethodPrepare):

    def __init__(self, data: pd.DataFrame, colunas: list,harmonico: int,regressor:sklearn.ensemble, rede_oculta = '', test_size=models.test_size,**kwargs) -> None:
        self.harmonico = harmonico
        self.regressor = regressor(**kwargs)
        self.test_size = test_size
        self.rede = rede_oculta
        self.colunas = colunas
        super().__init__(data,test_size=self.test_size)


    def exportar_relatorio(self):
        self.metodo = f'{self.regressor.__class__.__name__}{self.rede}'

        # Cria o arquivo txt e escreve as informações
        with open(f"database/dados_tratados/harmonicos_{self.harmonico}/relatorio_{self.metodo}_harmonico{self.harmonico}.txt", 'w') as f:
            f.write(f"Regressor {self.metodo} - {self.harmonico} Harmônicos\n\n")
            f.write("Erro Médio Quadrático (MSE): {:.3f}\n".format(self.mse))
            f.write("RMS Erro (RMSE): {:.3f}\n".format(np.sqrt(self.mse)))
            f.write(f'Erro Médio Absoluto (MAE): {self.mae:.3f}\n')
            f.write("Coeficiente de Determinação (R²): {:.3f}\n".format(self.r2))

        print(f'Método {self.metodo} exportado com sucesso!')

    def run(self):
        self.prepare_data()
        self.fit_regressor = self.regressor.fit(self.x_train,self.y_train)

        # Faz a predição dos dados de teste
        self.y_pred = self.fit_regressor.predict(self.x_test)

        self.y_pred = self.scaler.inverse_transform(self.y_pred)
        self.y_test = self.scaler.inverse_transform(self.y_test)
        
        # Avalia o desempenho do modelo
        self.mse = mean_squared_error(self.y_test, self.y_pred)
        self.mae = mean_absolute_error(self.y_test, self.y_pred)
        self.r2 = r2_score(self.y_test, self.y_pred)

        self.exportar_relatorio()

