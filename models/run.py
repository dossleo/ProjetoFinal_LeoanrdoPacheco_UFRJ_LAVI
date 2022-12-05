from models import _data_normalization, _frequency_features_extraction, _get_data, _low_pass_filter, _time_features_extraction, generate_rpm, get_rpm
import models
import pandas as pd
import matplotlib.pyplot as plt

class GenerateCSV:
    def __init__(self,filter_order = 5,order_frequency = 9,window_frequency = 50):
            
        # Dados de input do problema
        self.fs = models.freq_sample    
        self.maior_freq_defeito = max(models.fault_frequency)*self.rpm_medio
        self.order_frequency = order_frequency
        self.window_frequency = window_frequency
        self.filter_order = filter_order
        self.cutoff_filter = self.rpm_medio*2

        # Simulando input de dados de sensor de rotação
        self.gerar_rpm = generate_rpm.GenerateRPM(2000,self.fs)
        self.df_rpm = self.gerar_rpm.generate_array()
        self.pegar_rpm = get_rpm.GetRPM(self.df_rpm,models.freq_sample)
        self.rpm_pontos = self.pegar_rpm.get_rpm_ponto_a_ponto()
        self.rpm_medio = self.pegar_rpm.get_rpm_medio()

        # Definindo dataframes
        self.df_completo = pd.DataFrame()
        self.df_loop = []


    def plot_rpm(self):

        self.gerar_rpm.plot_array()
        self.pegar_rpm.plot_picos()
        self.pegar_rpm.plot_rpm()

    def generate(self):

        for fault in range(len(models.fault_frequency)):
            for file in models.filenames:
                # Dados Brutos
                self.raw_data = _get_data.GetData(models.path,file).Get()

                # Dados Filtrados
                self.filtered_data = _low_pass_filter.LowPassFilter(self.raw_data,self.cutoff_filter,self.filter_order)
                self.filtered_data = self.filtered_data.lowpass_filter()

                # Dados Normalizados
                self.normalized_data = _data_normalization.DataNormalized(self.filtered_data)

                # Fourier
                self.frequency_domain_data = _frequency_features_extraction.FrequencyFeaturesExtraction(self.normalized_data.get(),self.rpm_medio,models.fault_names[fault])
                self.reference_frequency = models.fault_frequency[fault]*self.rpm_medio
                self.frequency_domain_data.window_around_frequency(self.reference_frequency,self.window_frequency)
                self.orders_mean = self.frequency_domain_data.get_features(self.reference_frequency,self.window_frequency,self.order_frequency)

                # Dataframe com os features extraídos na frequência
                self.df_loop.append(self.orders_mean)

            self.df_loop = pd.json_normalize(self.df_loop)

            # Concatenando dataframes
            for column in self.df_loop.columns:
                self.df_completo[column] = self.df_loop[column]

    def save_as_csv(self,name = 'dataframe_completo'):
        self.df_completo.to_csv(f'{name}.csv')

    def print_dataframe(self):
        print(self.df_completo)
            