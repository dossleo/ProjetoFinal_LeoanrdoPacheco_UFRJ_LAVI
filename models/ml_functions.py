import models
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

import sklearn.ensemble
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report

class MethodPrepare:


    def __init__(self, data:pd.DataFrame) -> None:
        self.data = data
        self.x_data = self.get_x_data()
        self.y_data = self.get_y_data()

        self.test_size = models.test_size
        self.seed = models.seed

    def get_x_data(self):
        return self.data[models.x_columns]

    def get_y_data(self):
        return self.data[models.y_column]

    def prepare_data(self):
        self.x_train, self.x_test, self.y_train, self.y_test = train_test_split(
            self.x_data,
            self.y_data,
            test_size=self.test_size,
            random_state = self.seed
        )

class Classifier(MethodPrepare):

    def __init__(self, data: pd.DataFrame, classifier:sklearn.ensemble, **kwargs) -> None:
        self.classifier = classifier(**kwargs)
        super().__init__(data)

    def run(self):
        self.prepare_data()
        self.fit_classifier = self.classifier.fit(self.x_train,self.y_train)
        self.prediction = self.classifier.predict(self.x_test)
        self.score = self.classifier.score(self.x_test, self.y_test)