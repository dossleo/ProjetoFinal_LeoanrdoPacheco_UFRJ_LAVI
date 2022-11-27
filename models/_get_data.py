from msilib.schema import SelfReg
import matplotlib.pyplot as plt
import scipy.io
import numpy as np
import pandas as pd
import os
import glob
from math import sqrt
import models

path=r'database/brutos/2nd_test'
filename = '2004.02.12.10.32.39'

class GetData():

    def __init__(self,path,filename,column):
        

        self.path = path
        self.filename = filename
        self.dataset=pd.read_csv(os.path.join(path, self.filename), sep='\t',header=None)

        self.bearing_no = column
        self.bearing_data = np.array(self.dataset.iloc[:,self.bearing_no-1])

        self.length = len(self.bearing_data)
    
    def Get(self):
        return self.bearing_data

if __name__ == "__main__":
    teste = GetData(path,filename,1)
    data = teste.Get()
    print(data)
