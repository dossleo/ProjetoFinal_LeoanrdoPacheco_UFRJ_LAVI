import numpy as np
from math import sqrt
import os
from scipy.io import loadmat
import models
import pandas as pd
import models
from models import _time_features_extraction


class DataGenerator:

    BASE_DIR = os.path.join(os.getcwd(), "database", "brutos")

    def __init__(self) -> None:
        self.files_list = self.get_file_list()
        self.data = None
        self.data_list = []
        self.data_json = []

    def make_file_path(self, file_name:str, folder_name:str):
        return os.path.join(self.BASE_DIR, folder_name, file_name)

    def get_file_list(self) -> list:
        folders = models.mapped_databases.keys()
        files_path_list = []
        for folder in folders:
            files = os.listdir(os.path.join(self.BASE_DIR, folder))
            files_path_list.extend([self.make_file_path(file, folder) for file in files if ".mat" in file])
        return files_path_list

    def read(self, file_path) -> np.array:
        mat_data = loadmat(file_path)
        data = mat_data["bearing"][0]
        index_gs = data.dtype.names.index('gs')
        self.data = data[0][index_gs][:,0]

    def split(self, fault:str):
        index = 0
        self.data_list = []
        data = self.data
        overlap = models.overlap/100
        incrementer = int((models.time_window-models.time_window*overlap)*models.frequency_rate_dict.get(fault))

        while index < len(data):
            self.data_list.append(data[index:index+incrementer])
            index += incrementer
        index -= incrementer
        self.data_list.append(data[index:len(data)])

    def increment_data_json(self, fault: str) -> pd.DataFrame:
        for data in self.data_list:
            time_features = _time_features_extraction.TimeFeatures(data)
            self.data_json.append({
                'maximum':time_features.maximum(),
                'minimum':time_features.minimum(),
                'mean':time_features.mean(),
                'standard_deviation':time_features.standard_deviation(),
                'rms':time_features.rms(),
                'skewness':time_features.skewness(),
                'kurtosis':time_features.kurtosis(),
                'form_factor':time_features.form_factor(),
                'crest_factor':time_features.crest_factor(),
                'fault': fault
            })

    def run(self):
        for file in self.files_list:
            fault = models.mapped_databases.get(file.split("\\")[-2])
            self.read(file)
            self.split(fault)
            self.increment_data_json(fault)
        return pd.json_normalize(self.data_json)