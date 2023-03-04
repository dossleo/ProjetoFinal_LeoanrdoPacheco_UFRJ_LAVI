import models
import pandas as pd
import sklearn.ensemble
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report
from numpy import round
class MethodPrepare:

    def __init__(self, data:pd.DataFrame,colunas:list, test_size = models.test_size) -> None:
        self.data = data
        self.colunas = colunas
        self.x_data = self.get_x_data()
        self.y_data = self.get_y_data()
        self.x_columns = self.colunas[0:-1]

        self.test_size = test_size
        self.seed = models.seed

    def get_x_data(self):
        df = self.data[self.colunas]
        df = df[df.columns[0:-1]]

        return df

    def get_y_data(self):
        return self.data[self.data.columns[-1]]

    def prepare_data(self):
        self.x_train, self.x_test, self.y_train, self.y_test = train_test_split(
            self.x_data,
            self.y_data,
            test_size=self.test_size,
            random_state = self.seed,
            stratify=self.y_data
        )

class Classifier(MethodPrepare):

    def __init__(self, data: pd.DataFrame, colunas: list,harmonico: int,classifier:sklearn.ensemble, rede_oculta = '', test_size=models.test_size,**kwargs) -> None:
        self.harmonico = harmonico
        self.classifier = classifier(**kwargs)
        self.test_size = test_size
        self.rede = rede_oculta
        self.colunas = colunas
        super().__init__(data,self.colunas,test_size=self.test_size)


    def exportar_relatorio(self):
        metodo = f'{self.classifier.__class__.__name__}{self.rede}'

        relatorio_classificador = f'Classificador: {metodo} - {self.harmonico}º harmonico'
        self.relatorio_acuracia = f'A precisão do classificador é:{round(100*accuracy_score(self.y_test, self.prediction),1)}%'
        relatorio_report = f'Relatório de classificação:\n{classification_report(self.y_test, self.prediction)}'
        relatorio = f'{relatorio_classificador}\n{self.relatorio_acuracia}\n{relatorio_report}'

        with open(f"database/dados_tratados/harmonicos_{self.harmonico}/relatorio_{metodo}_harmonico{self.harmonico}.txt", "w") as text_file:
            text_file.write(relatorio)

        print(f'Método {metodo} exportado com sucesso!')

    def run(self):
        self.prepare_data()
        self.fit_classifier = self.classifier.fit(self.x_train,self.y_train)
        self.prediction = self.classifier.predict(self.x_test)
        self.score = self.classifier.score(self.x_test, self.y_test)
        self.exportar_relatorio()

