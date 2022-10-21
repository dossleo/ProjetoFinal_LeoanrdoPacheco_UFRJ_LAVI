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
    def __init__(self,path):
        #path=r'database/brutos/2nd_test'

        self.path = path
        self.filename = '2004.02.12.10.32.39'
        self.dataset=pd.read_csv(os.path.join(path, self.filename), sep='\t',header=None)

        self.bearing_no = 1
        self.bearing_data = np.array(self.dataset.iloc[:,self.bearing_no-1])

        #self.feature_matrix=np.zeros((1,9))

        self.length = len(self.bearing_data)

    @logger
    def maximum(self):
        self.max = np.max(self.bearing_data)
        
        #self.feature_matrix[0,0] = self.max
        return self.max

    @logger
    def minimum(self):
        self.min = np.min(self.bearing_data)
        
        #self.feature_matrix[0,1] = self.min
        return self.min

    @logger
    def mean(self):
        self.media = np.mean(self.bearing_data)
        
        #self.feature_matrix[0,2] = self.media
        return self.media

    @logger
    def standard_deviation(self):
        self.std = np.std(self.bearing_data, ddof = 1)
        
        #self.feature_matrix[0,3] = self.std
        return self.std

    @logger
    def rms(self):
        self.rms_value = sqrt(sum(n*n for n in self.bearing_data)/self.length)
        
        #self.feature_matrix[0,4] = self.rms_value
        return self.rms_value 

    @logger
    def skewness(self):
        self.n = len(self.bearing_data)
        self.third_moment = np.sum((self.bearing_data - np.mean(self.bearing_data))**3) / self.length
        self.s_3 = np.std(self.bearing_data, ddof = 1) ** 3
        self.skew = self.third_moment/self.s_3

        #self.feature_matrix[0,5] = self.skew
        return self.skew

    @logger
    def kurtosis(self):
        self.n = len(self.bearing_data)
        self.fourth_moment = np.sum((self.bearing_data - np.mean(self.bearing_data))**4) / self.n
        self.s_4 = np.std(self.bearing_data, ddof = 1) ** 4
        self.kurt = self.fourth_moment / self.s_4 - 3

        #self.feature_matrix[0,6] = self.kurt
        return self.kurt

    @logger
    def crest_factor(self):
        self.cf = self.max/self.rms_value

        #self.feature_matrix[0,7] = self.cf
        return self.cf

    @logger
    def form_factor(self):
        self.ff = self.rms_value/self.media

        #self.feature_matrix[0,8] = self.ff
        return self.ff
        
    @logger
    def execute_time_features(self):
        path = self.path
        self.Time_feature_matrix=pd.DataFrame()

        self.test_set=2

        self.bearing_no=1 # Provide the Bearing number [1,2,3,4] of the Test set

        for filename in os.listdir(path):
            
            self.dataset=pd.read_csv(os.path.join(path, filename), sep='\t',header=None)

            self.bearing_data = np.array(self.dataset.iloc[:,self.bearing_no-1])

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





class Frequency_Features_Extraction():
    def __init__(self,path,rolamento):
        self.filename = '2004.02.12.10.32.39'
        self.dataset=pd.read_csv(os.path.join(path, self.filename), sep='\t',header=None)

        self.bearing_no = 1
        self.bearing_data = np.array(self.dataset.iloc[:,self.bearing_no-1])

        #self.feature_matrix=np.zeros((1,9))

        self.length = len(self.bearing_data)
    
    def FFT(self):
        self.fourier = np.fft.fftfreq(self.bearing_data)
        return self.fourier

    def picos_rpm(self):
        pass
    
    def picos_pista_externa(self):
        pass

    def picos_pista_interna(self):
        pass

    def picos_gaiola(self):
        pass

    def picos_rolo(self):
        pass

