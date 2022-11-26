from scipy.signal import butter,filtfilt, hilbert, chirp
import plotly.graph_objects as go
import scipy.io
import numpy as np
import pandas as pd
import os
from msilib.schema import SelfReg
import matplotlib.pyplot as plt
import glob
from math import *
import scipy.fftpack
import models
from models import get_data,low_pass_filter,data_normalization, time_features_extraction


if __name__ == "__main__":
    data = get_data.GetData(models.path,models.filename,1).Get()


    fs = 20480
    cutoff = 400
    order = 5

    teste = low_pass_filter.LowPassFilter(data,cutoff,fs,order)
    # teste.plot_matplotlib(plot_raw_data = False)

    data_filtered = teste.lowpass_filter()

    data_normalized = data_normalization.DataNormalized(data_filtered)

    data_normalized = data_normalized.Get()["x"]

    

