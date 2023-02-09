import numpy as np
from math import sqrt
import os
from scipy.io import loadmat
import models
import pandas as pd

class DataGenerator:

    BASE_DIR = os.path.join(os.getcwd(), "data", "MFPT Fault Data Sets")

    def __init__(self) -> None:
        self.files_list = self.get_file_list()
        self.data = None
        self.fault = None
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
        data = data[0][index_gs][:,0]
        return data
        
    def run(self):
        lista_arquivos = []
        for file in self.files_list:
            fault = models.mapped_databases.get(file.split("\\")[-2])
            self.fault = fault
            data = self.read(file)
            lista_arquivos.append(data)

        return lista_arquivos
