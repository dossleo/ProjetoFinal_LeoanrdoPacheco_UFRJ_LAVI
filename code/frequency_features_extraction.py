from msilib.schema import SelfReg
import matplotlib.pyplot as plt
import scipy.io
import numpy as np
import pandas as pd
import os
import glob
from math import sqrt
from .general_decorators import logger

class Frequency_Features_Extraction():
    def __init__(self,path,rolamento):
        self.filename = '2004.02.12.10.32.39'
        self.dataset=pd.read_csv(os.path.join(path, self.filename), sep='\t',header=None)

        self.bearing_no = 1
        self.bearing_data = np.array(self.dataset.iloc[:,self.bearing_no-1])

        #self.feature_matrix=np.zeros((1,9))

        self.length = len(self.bearing_data)
    
    @logger
    def FFT(self):
        self.fourier = np.fft.fftfreq(self.bearing_data)
        return self.fourier

    @logger
    def PicosRPM(self):
        pass
    
    @logger
    def PicosPistaExterna(self):
        pass

    @logger
    def PicosPistaInterna(self):
        pass

    @logger
    def PicosGaiola(self):
        pass

    @logger
   def PicosRolo(self):
        pass

