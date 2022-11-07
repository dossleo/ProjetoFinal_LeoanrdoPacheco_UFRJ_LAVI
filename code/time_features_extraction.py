from msilib.schema import SelfReg
import matplotlib.pyplot as plt
import scipy.io
import numpy as np
import pandas as pd
import os
import glob
from math import sqrt
from .general_decorators import logger


class TimeFeatureExtraction():

    def __init__(self,path,filename,column):
        
        #path=r'database/brutos/2nd_test'

        self.path = path
        # self.filename = '2004.02.12.10.32.39'
        self.filename = filename
        self.dataset=pd.read_csv(os.path.join(path, self.filename), sep='\t',header=None)

        self.bearing_no = column
        self.bearing_data = np.array(self.dataset.iloc[:,self.bearing_no-1])

        self.length = len(self.bearing_data)

    @logger
    def maximum(self):
        self.max = np.max(self.bearing_data)        
        return self.max

    @logger
    def minimum(self):
        self.min = np.min(self.bearing_data)        
        return self.min

    @logger
    def mean(self):
        self.media = np.mean(self.bearing_data)        
        return self.media

    @logger
    def standard_deviation(self):
        self.std = np.std(self.bearing_data, ddof = 1)        
        return self.std

    @logger
    def rms(self):
        self.rms_value = sqrt(sum(n*n for n in self.bearing_data)/self.length)        
        return self.rms_value 

    @logger
    def skewness(self):
        self.n = len(self.bearing_data)
        self.third_moment = np.sum((self.bearing_data - np.mean(self.bearing_data))**3) / self.length
        self.s_3 = np.std(self.bearing_data, ddof = 1) ** 3
        self.skew = self.third_moment/self.s_3

        return self.skew

    @logger
    def kurtosis(self):
        self.n = len(self.bearing_data)
        self.fourth_moment = np.sum((self.bearing_data - np.mean(self.bearing_data))**4) / self.n
        self.s_4 = np.std(self.bearing_data, ddof = 1) ** 4
        self.kurt = self.fourth_moment / self.s_4 - 3

        return self.kurt

    @logger
    def crest_factor(self):
        self.cf = self.max/self.rms_value

        return self.cf

    @logger
    def form_factor(self):
        self.ff = self.rms_value/self.media

        return self.ff

    @logger
    def data_visualization(self):
        df1 = pd.read_csv("C:/Users/leona/Documents/ProjetoFinal_LeonardoPacheco_UFRJ_LAVI/database/Tratados/Time_feature_matrix_Bearing_1_Test_2.csv")
        df1 = pd.read_csv("C:/Users/leona/Documents/ProjetoFinal_LeonardoPacheco_UFRJ_LAVI/database/Tratados/Time_feature_matrix_Bearing_1_Test_2.csv",index_col='Unnamed: 0')
        df1.index = pd.to_datetime(df1.index)
        
        df1 = pd.read_csv("C:/Users/leona/Documents/ProjetoFinal_LeonardoPacheco_UFRJ_LAVI/database/Tratados/Time_feature_matrix_Bearing_1_Test_2.csv",index_col='Unnamed: 0')
        df2 = pd.read_csv("C:/Users/leona/Documents/ProjetoFinal_LeonardoPacheco_UFRJ_LAVI/database/Tratados/Time_feature_matrix_Bearing_2_Test_2.csv",index_col='Unnamed: 0')
        df3 = pd.read_csv("C:/Users/leona/Documents/ProjetoFinal_LeonardoPacheco_UFRJ_LAVI/database/Tratados/Time_feature_matrix_Bearing_3_Test_2.csv",index_col='Unnamed: 0')
        df4 = pd.read_csv("C:/Users/leona/Documents/ProjetoFinal_LeonardoPacheco_UFRJ_LAVI/database/Tratados/Time_feature_matrix_Bearing_4_Test_2.csv",index_col='Unnamed: 0')

        df1.index = pd.to_datetime(df1.index)

        for col in (df1.columns):  
    
            plt.figure(figsize=(10, 5))
            plt.plot(df1.index,df1[col])
            plt.plot(df1.index,df2[col])
            plt.plot(df1.index,df3[col])
            plt.plot(df1.index,df4[col])

            plt.legend(['bearing-1','bearing-2','bearing-3','bearing-4'])

            plt.xlabel("Date-Time")
            plt.ylabel(col)
            plt.title(col)
            plt.show()
        
    @logger
    def execute_time_features(self):
        path = self.path
        self.Time_feature_matrix=pd.DataFrame()

        self.test_set=2
        for bearing_no in range(4):
            self.bearing_no= bearing_no # Provide the Bearing number [1,2,3,4] of the Test set '   

            for filename in os.listdir(path):
                
                self.dataset=pd.read_csv(os.path.join(path, filename), sep='\t',header=None)

                self.bearing_data = np.array(self.dataset.iloc[:,self.bearing_no])

                self.feature_matrix=np.zeros((1,9))

                self.feature_matrix[0,0] = self.maximum()
                self.feature_matrix[0,1] = self.minimum()
                self.feature_matrix[0,2] = self.mean()
                self.feature_matrix[0,3] = self.standard_deviation()
                self.feature_matrix[0,4] = self.rms()
                self.feature_matrix[0,5] = self.skewness()
                self.feature_matrix[0,6] = self.kurtosis()
                self.feature_matrix[0,7] = self.crest_factor()
                self.feature_matrix[0,8] = self.form_factor()
                
                self.df = pd.DataFrame(self.feature_matrix)
                self.df.index=[filename[:-3]]
                
                self.frames = [self.Time_feature_matrix,self.df]
                self.Time_feature_matrix = pd.concat(self.frames)


            self.Time_feature_matrix.columns = ['Max','Min','Mean','Std','RMS','Skewness','Kurtosis','Crest Factor','Form Factor']
            self.Time_feature_matrix.index = pd.to_datetime(self.Time_feature_matrix.index, format='%Y.%m.%d.%H.%M')

            self.Time_feature_matrix = self.Time_feature_matrix.sort_index()

            self.Time_feature_matrix.to_csv('Time_feature_matrix_Bearing_{}_Test_{}.csv'.format(self.bearing_no,self.test_set))