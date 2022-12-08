import os

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

import models
from models import (data_normalization, frequency_features_extraction,
                    get_data, get_rpm, low_pass_filter,
                    time_features_extraction)


class GenerateCSV:
    def __init__(self,path = models.PATH_1ST_DATABASE,column = 0, filter_order = 5,order_frequency = 9,window_frequency = 50):
        
        # Path and files
        self.path = path
        self.filenames = os.listdir(self.path)
        self.column = column

        # Dados de input do problema
        self.fs = models.freq_sample    
        self.order_frequency = order_frequency
        self.window_frequency = window_frequency
        self.filter_order = filter_order

        # Definindo dataframes
        self.df_completo = pd.DataFrame()

    def get_rpm(self):

        # get rpm file
        rpm_file = models.RPM_ARTIFICIAL_FILE
        rpm_raw_data = np.array(pd.read_csv(rpm_file))[:,1]

        # Tratando dados do rpm file
        self.pegar_rpm = get_rpm.GetRPM(rpm_raw_data,models.freq_sample)
        self.rpm_medio = self.pegar_rpm.get_rpm_medio()

        # Depende do RPM
        self.cutoff_filter = self.rpm_medio*2
        self.maior_freq_defeito = max(models.fault_frequency)*self.rpm_medio

    def plot_rpm(self):
        self.get_rpm()

        self.pegar_rpm.plot_picos()
        self.pegar_rpm.plot_rpm()

    def generate_data(self):
        self.get_rpm()

        for fault in range(len(models.fault_frequency)):
            self.df_loop = []
            for file in self.filenames:
                # Dados Brutos
                self.raw_data = get_data.GetData(self.path,file,column = self.column).Get()

                # Dados Filtrados
                self.filtered_data = low_pass_filter.LowPassFilter(self.raw_data,self.cutoff_filter,self.filter_order)
                self.filtered_data = self.filtered_data.lowpass_filter()

                # Dados Normalizados
                self.normalized_data = data_normalization.DataNormalized(self.filtered_data)

                # Fourier
                self.frequency_domain_data = frequency_features_extraction.FrequencyFeaturesExtraction(self.normalized_data.get(),self.rpm_medio,models.fault_names[fault])
                self.reference_frequency = models.fault_frequency[fault]*self.rpm_medio
                self.frequency_domain_data.window_around_frequency(self.reference_frequency,self.window_frequency)
                self.orders_mean = self.frequency_domain_data.get_features(self.reference_frequency,self.window_frequency,self.order_frequency)

                # Dataframe com os features extraídos na frequência
                self.df_loop.append(self.orders_mean)

            self.df_loop = pd.json_normalize(self.df_loop)

            # Concatenando dataframes
            for columns in self.df_loop.columns:
                self.df_completo[columns] = self.df_loop[columns]

    def save_as_csv(self,name = 'dataframe_completo',path_csv = 'database/tratados/frequency_domain'):
        self.generate_data()
        self.df_completo.to_csv(f'{path_csv}/{name}.csv')

    def print_dataframe(self):
        self.generate_data()
        print(self.df_completo)
            