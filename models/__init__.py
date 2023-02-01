import os
import models

# -----------------------------------------------
# --------- Pasta dos Arquivos   ----------------
# -----------------------------------------------

HORIZONTAL_MISALIGNMENT = 'database/horizontal-misalignment'
IMBALANCE = 'database/imbalance'
NORMAL = 'database/normal'
OVERHANG = 'database/overhang'
UNERHANG = 'database/underhang'
VERTICAL_MISALIGNMENT = 'database/vertical-misalignment'

# General configs
DEBUG = True


# -----------------------------------------------
# --------- Informações do Experimento ----------
# -----------------------------------------------

# Aquisição de dados
freq_aquisicao = 50000 # Hz

rotacao = 0
rolamento_interno = [1,2,3]
rolamento_externo = [4,5,6]
microfone = 7

sensores = {
            # 'rotacao':0,

            'rolamento_interno_axial':1,
            'rolamento_interno_radial1':2,
            'rolamento_interno_radial2':3,
            
            'rolamento_externo_axial':4,
            'rolamento_externo_radial1':5,
            'rolamento_externo_radial2':6,
            
            # 'microfone':7
            }

# -----------------------------------------------
# --------- Frequencias Caracteristicas ---------
# -----------------------------------------------
# Rolamento
num_esferas = 8
diametro_esfera = 0.07145 # mm
diametro_gaiola = 2.8519 # mm

ball_fault = 1.8710
cage_fault = 0.3750
outer_race = 2.9980
inner_race = 5.0020

frequencias_rolamento = [ball_fault,
                        cage_fault,
                        outer_race
                        ,inner_race]



# -----------------------------------------------
# --------- Defeitos Impostos -------------------
# -----------------------------------------------


testes = ['horizontal-misalignment','imbalance','normal','overhang','underhang','vertical-misalignment']
defeitos_desbalanceamento = ['6g','10g','15g','20g','25g','30g','35g'] # g gramas de desbalancemanto
defeitos_desalinhamento_horizontal = ['0.5mm','1.0mm','1.5mm','2.0mm'] # mm de desalinhamento horizontal
defeitos_desalinhamento_vertical = ['0.51mm','0.63mm','1.27mm','1.40mm','1.78mm','1.90mm'] # mm de desalinhamento vertical

defeito_rolamento = ['ball_fault','cage_fault','outer_race','inner_race']
desbalanceamento_rolamento = ['0g','6g','20g','35g']


path_dados_tratados = 'database/dados_tratados'

PATH = {'database/dados_brutos/normal':'normal',

           'database/dados_brutos/horizontal-misalignment/0.5mm':'desalinhamento_horizontal_baixo',
           'database/dados_brutos/horizontal-misalignment/1.0mm':'desalinhamento_horizontal_médio',
           'database/dados_brutos/horizontal-misalignment/1.5mm':'desalinhamento_horizontal_alto',
           'database/dados_brutos/horizontal-misalignment/2.0mm':'desalinhamento_horizontal_alto',
           
           'database/dados_brutos/imbalance/6g':'desbalanceamento_baixo',
           'database/dados_brutos/imbalance/10g':'desbalanceamento_baixo',
           'database/dados_brutos/imbalance/15g':'desbalanceamento_medio',
           'database/dados_brutos/imbalance/20g':'desbalanceamento_medio',
           'database/dados_brutos/imbalance/25g':'desbalanceamento_alto',
           'database/dados_brutos/imbalance/30g':'desbalanceamento_alto',
           'database/dados_brutos/imbalance/35g':'desbalanceamento_alto',
           
           'database/dados_brutos/overhang/ball_fault/0g':'ball_fault_baixo',
           'database/dados_brutos/overhang/ball_fault/6g':'ball_fault_medio',
           'database/dados_brutos/overhang/ball_fault/20g':'ball_fault_alto',
           'database/dados_brutos/overhang/ball_fault/35g':'ball_fault_alto',

           'database/dados_brutos/overhang/cage_fault/0g':'cage_fault_baixo',
           'database/dados_brutos/overhang/cage_fault/6g':'cage_fault_medio',
           'database/dados_brutos/overhang/cage_fault/20g':'cage_fault_alto',
           'database/dados_brutos/overhang/cage_fault/35g':'cage_fault_alto',

           'database/dados_brutos/overhang/outer_race/0g':'outer_race_baixo',
           'database/dados_brutos/overhang/outer_race/6g':'outer_race_medio',
           'database/dados_brutos/overhang/outer_race/20g':'outer_race_alto',
           'database/dados_brutos/overhang/outer_race/35g':'outer_race_alto',
           
           'database/dados_brutos/underhang/ball_fault/0g':'ball_fault_baixo',
           'database/dados_brutos/underhang/ball_fault/6g':'ball_fault_medio',
           'database/dados_brutos/underhang/ball_fault/20g':'ball_fault_alto',
           'database/dados_brutos/underhang/ball_fault/35g':'ball_fault_alto',

           'database/dados_brutos/underhang/cage_fault/0g':'cage_fault_baixo',
           'database/dados_brutos/underhang/cage_fault/6g':'cage_fault_medio',
           'database/dados_brutos/underhang/cage_fault/20g':'cage_fault_alto',
           'database/dados_brutos/underhang/cage_fault/35g':'cage_fault_alto',

           'database/dados_brutos/underhang/outer_race/0g':'outer_race_baixo',
           'database/dados_brutos/underhang/outer_race/6g':'outer_race_medio',
           'database/dados_brutos/underhang/outer_race/20g':'outer_race_alto',
           'database/dados_brutos/underhang/outer_race/35g':'outer_race_alto',

           }

defeitos = ['normal',
            'desalinhamento_horizontal_baixo','desalinhamento_horizontal_médio','desalinhamento_horizontal_alto',
            'desbalanceamento_baixo','desbalanceamento_médio','desbalanceamento_alto',
            'ball_fault_baixo','ball_fault_médio','ball_fault_alto',
            'cage_fault_baixo','cage_fault_médio','cage_fault_alto',
            'ball_fault_baixo','ball_fault_médio','ball_fault_alto',
            'ball_fault_baixo','ball_fault_médio','ball_fault_alto',]


# -----------------------------------------------
# --------- Indicadores Analisados --------------
# -----------------------------------------------

indicadores = [
            'rotacao_hz',
            'maximo',
            'rms',
            'assimetria',
            'curtose'
            # ,'fator_forma',
            # 'fator_crista'
            ]

for defeito in defeito_rolamento:
            # indicadores.append(f'potencia_{defeito}')
            indicadores.append(f'soma_{defeito}')