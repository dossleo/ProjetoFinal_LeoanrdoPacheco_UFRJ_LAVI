from numpy import array
import pandas as pd
import os
import models

class GetData():

    def __init__(self,path,filename,column):
        
        self.path = path
        self.filename = filename
        self.dataset=pd.read_csv(os.path.join(path, self.filename), sep='\t',header=None)

        self.bearing_no = column
        self.bearing_data = array(self.dataset.iloc[:,self.bearing_no-1])
    
    def Get(self):
        return self.bearing_data