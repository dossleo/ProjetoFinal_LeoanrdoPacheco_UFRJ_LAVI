import os
import models

# -----------------------------------------------
# --------- Pasta dos Arquivos   ----------------
# -----------------------------------------------

PATH_1ST_DATABASE = 'database/brutos/1st_test'
PATH_2ND_DATABASE = 'database/brutos/2nd_test'
PATH_3RD_DATABASE = 'database/brutos/3rd_test'

PATH_TEST = [PATH_1ST_DATABASE,PATH_2ND_DATABASE,PATH_3RD_DATABASE]

# General configs
DEBUG = True


# -----------------------------------------------
# --------- Informações do Experimento ----------
# -----------------------------------------------

# Aquisição de dados
freq_aquisicao = 50000 # Hz

# Rolamento
num_esferas = 8
diametro_esfera = 0.07145 # mm
diametro_gaiola = 2.8519 # mm

frequencia_gaiola = 0.3750
frequencia_pista_interna = 5.0020
frequencia_pista_externa = 2.9980
frequencia_esfera = 1.8710

frequencias_rolamento = [frequencia_gaiola
                ,frequencia_pista_interna
                ,frequencia_pista_externa
                ,frequencia_esfera]

fault_names = ['freq_gaiola'
                ,'freq_pista_interna'
                ,'freq_pista_externa'
                ,'freq_esfera']


# -----------------------------------------------
# --------- Indicadores Analisados --------------
# -----------------------------------------------

indicadores = ['maximum',
            # 'minimum',
            # 'mean',
            # 'standard_deviation',
            'rms',
            'skewness',
            'kurtosis'
            # ,'form_factor',
            # 'crest_factor'
            ]

for defeito in fault_names:
            indicadores.append(f'potencia_{defeito}')
            indicadores.append(f'soma_{defeito}')