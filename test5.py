import os
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import models
from models import normalizar_sinal, get_raw_data
import os

ordem = 1
pasta = f'database/dados_tratados/ordens_{ordem}'
arquivos = os.listdir(pasta)
arquivo = arquivos[0]

sinal = get_raw_data.GetData(pasta,arquivo).GetDataframe()

sinal_normalizado = normalizar_sinal.NormalizarSinal(sinal,ordem).save_as_csv()


# sinal_normalizado[sinal_normalizado['defeito']=='normal']

print(sinal_normalizado)

