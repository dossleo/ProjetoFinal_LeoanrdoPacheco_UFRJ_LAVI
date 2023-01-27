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


# -----------------------------------------------
# --------- Frequencias Caracteristicas ---------
# -----------------------------------------------
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



# -----------------------------------------------
# --------- Defeitos Impostos -------------------
# -----------------------------------------------

nomes_defeitos = ['normal','desalinhamento','desbalanceamento','freq_gaiola'
                ,'freq_pista_interna'
                ,'freq_pista_externa'
                ,'freq_esfera']

defeitos_desbalanceamento = [6,10,15,20,25,30,35] # gramas de desbalancemanto
defeitos_desalinhamento_horizontal = [0.5,1.0,1.5,2.0] # mm de desalinhamento horizontal
defeitos_desalinhamento_vertical = [0.51,0.63,1.27,1.40,1.78,1.90] # mm de desalinhamento vertical

defeito_rolamento = [0,6,20,35] # gramas de desbalanceamento




# -----------------------------------------------
# --------- Indicadores Analisados --------------
# -----------------------------------------------

indicadores = ['maximo',
            'rms',
            'assimetria',
            'curtose'
            # ,'fator_forma',
            # 'fator_crista'
            ]

for defeito in nomes_defeitos:
            indicadores.append(f'potencia_{defeito}')
            indicadores.append(f'soma_{defeito}')