import models
from models import get_raw_data, get_rpm
import numpy as np
import pandas as pd
import os
import matplotlib.pyplot as plt

class ListaRPM():
    def __init__(self,pasta) -> None:
        self.pasta = pasta

        arquivos = os.listdir(self.pasta)

        sinal_rpm = get_raw_data.GetData(self.pasta,arquivos[0],0)
        sinal_rpm = sinal_rpm.Get()

        rpm = get_rpm.GetRPM(self.pasta,arquivos[0])
        rpm_medio = rpm.get_rpm_medio('hz')

        self.rpms = [rpm_medio]

        for i in range(len(arquivos)):
            sinal_rpm = get_raw_data.GetData(self.pasta,arquivos[i],0)
            sinal_rpm = sinal_rpm.Get()

            rpm = get_rpm.GetRPM(self.pasta,arquivos[i])
            rpm_medio = rpm.get_rpm_medio('hz')
            
            if np.abs(rpm_medio) > np.abs(self.rpms[-1])+3:
                rpm_medio = self.rpms[-1]+1

            self.rpms.append(rpm_medio)

        self.rpms.pop(0)

        
    def Get(self):
        return self.rpms
