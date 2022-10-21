from statistics import *
import pandas as pd
import glob
import numpy as from msilib.schema import SelfReg
from typing_extensions import Self
import matplotlib.pyplot as plt
import scipy.io
import numpy as np
import pandas as pd
import os
import glob
from math import sqrt


class Frequency_Features_Extraction():
    def __init__(self,path):
        self.all_files = glob.glob(path + "\*")

    def fourier(self):
        self.fft = np.fft.fft()





