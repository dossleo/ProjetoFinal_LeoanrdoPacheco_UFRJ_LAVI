import numpy as np
from math import sqrt
import os
from scipy.io import loadmat
import models
import pandas as pd

class TimeFeatures():

    def __init__(self,data):
        self.bearing_data = np.array(data)
        self.length = len(self.bearing_data)

    def maximum(self):
        self.max = np.max(self.bearing_data)        
        return self.max

    def minimum(self):
        self.min = np.min(self.bearing_data)        
        return self.min

    def mean(self):
        self.media = np.mean(self.bearing_data)        
        return self.media

    def standard_deviation(self):
        self.std = np.std(self.bearing_data, ddof = 1)        
        return self.std

    def rms(self):
        self.rms_value = sqrt(sum(n*n for n in self.bearing_data)/self.length)        
        return self.rms_value 

    def skewness(self):
        self.n = len(self.bearing_data)
        self.third_moment = np.sum((self.bearing_data - np.mean(self.bearing_data))**3) / self.length
        self.s_3 = np.std(self.bearing_data, ddof = 1) ** 3
        self.skew = self.third_moment/self.s_3

        return self.skew

    def kurtosis(self):
        self.n = len(self.bearing_data)
        self.fourth_moment = np.sum((self.bearing_data - np.mean(self.bearing_data))**4) / self.n
        self.s_4 = np.std(self.bearing_data, ddof = 1) ** 4
        self.kurt = self.fourth_moment / self.s_4 - 3
        return self.kurt

    def crest_factor(self):
        self.cf = self.max/self.rms_value
        return self.cf

    def form_factor(self):
        self.ff = self.rms_value/self.media
        return self.ff