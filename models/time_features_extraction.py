import os
from math import sqrt

import numpy as np
import pandas as pd
from scipy.io import loadmat

import models


class TimeFeatures():

    def __init__(self,data):
        self.data = np.array(data)
        self.length = len(self.data)

    def maximum(self):
        self.max = np.max(self.data)        
        return self.max

    def minimum(self):
        self.min = np.min(self.data)        
        return self.min

    def mean(self):
        self.media = np.mean(self.data)        
        return self.media

    def standard_deviation(self):
        self.std = np.std(self.data, ddof = 1)        
        return self.std

    def rms(self):
        self.rms_value = sqrt(sum(n*n for n in self.data)/self.length)        
        return self.rms_value 

    def skewness(self):
        self.n = len(self.data)
        self.third_moment = np.sum((self.data - np.mean(self.data))**3) / self.length
        self.s_3 = np.std(self.data, ddof = 1) ** 3
        self.skew = self.third_moment/self.s_3

        return self.skew

    def kurtosis(self):
        self.n = len(self.data)
        self.fourth_moment = np.sum((self.data - np.mean(self.data))**4) / self.n
        self.s_4 = np.std(self.data, ddof = 1) ** 4
        self.kurt = self.fourth_moment / self.s_4 - 3
        return self.kurt

    def crest_factor(self):
        self.cf = self.max/self.rms_value
        return self.cf

    def form_factor(self):
        self.ff = self.rms_value/self.media
        return self.ff

    def run(self):

        self.freatures = models.features

        self.data_json = {
            'maximum':np.abs(self.maximum()),
            # 'minimum':np.abs(self.minimum()),
            # 'mean':np.abs(self.mean()),
            # 'standard_deviation':np.abs(self.standard_deviation()),
            'rms':np.abs(self.rms()),
            'skewness':np.abs(self.skewness()),
            'kurtosis':np.abs(self.kurtosis())
            # ,'form_factor':np.abs(self.form_factor()),
            # 'crest_factor':np.abs(self.crest_factor())
        }

        return self.data_json
        # return pd.json_normalize(self.data_json)