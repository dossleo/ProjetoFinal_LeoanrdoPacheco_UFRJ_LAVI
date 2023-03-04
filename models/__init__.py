# -----------------------------------------------
# -----------------------------------------------
# --------- Base de dados MAFAULDA --------------
# -----------------------------------------------
# -----------------------------------------------

import os
import models

# -----------------------------------------------
# --------- Pasta dos Arquivos   ----------------
# -----------------------------------------------

path_dados_brutos = 'database/dados_brutos'
path_dados_tratados = 'database/dados_tratados'

nome_padrao_de_arquivo = 'dados_extraidos'

PATH = {
        # "Nome da pasta" : "classe do defeito"
        f'{path_dados_brutos}/normal':'normal',

        f'{path_dados_brutos}/horizontal-misalignment/0.5mm':'desalinhamento_horizontal_baixo',
        f'{path_dados_brutos}/horizontal-misalignment/1.0mm':'desalinhamento_horizontal_médio',
        f'{path_dados_brutos}/horizontal-misalignment/1.5mm':'desalinhamento_horizontal_médio',
        f'{path_dados_brutos}/horizontal-misalignment/2.0mm':'desalinhamento_horizontal_alto',

        f'{path_dados_brutos}/vertical-misalignment/0.51mm':'desalinhamento_vertical_baixo',
        f'{path_dados_brutos}/vertical-misalignment/0.63mm':'desalinhamento_vertical_baixo',
        f'{path_dados_brutos}/vertical-misalignment/1.27mm':'desalinhamento_vertical_médio',
        f'{path_dados_brutos}/vertical-misalignment/1.40mm':'desalinhamento_vertical_médio',
        f'{path_dados_brutos}/vertical-misalignment/1.78mm':'desalinhamento_vertical_alto',
        f'{path_dados_brutos}/vertical-misalignment/1.90mm':'desalinhamento_vertical_alto',
           
        f'{path_dados_brutos}/imbalance/6g':'desbalanceamento_baixo',
        f'{path_dados_brutos}/imbalance/10g':'desbalanceamento_baixo',
        f'{path_dados_brutos}/imbalance/15g':'desbalanceamento_medio',
        f'{path_dados_brutos}/imbalance/20g':'desbalanceamento_medio',
        f'{path_dados_brutos}/imbalance/25g':'desbalanceamento_alto',
        f'{path_dados_brutos}/imbalance/30g':'desbalanceamento_alto',
        f'{path_dados_brutos}/imbalance/35g':'desbalanceamento_alto',
        
        # f'{path_dados_brutos}/overhang/ball_fault/0g':'ball_fault_baixo',
        f'{path_dados_brutos}/overhang/ball_fault/6g':'ball_fault_baixo',
        f'{path_dados_brutos}/overhang/ball_fault/20g':'ball_fault_medio',
        f'{path_dados_brutos}/overhang/ball_fault/35g':'ball_fault_alto',

        # f'{path_dados_brutos}/overhang/cage_fault/0g':'cage_fault_baixo',
        # f'{path_dados_brutos}/overhang/cage_fault/6g':'cage_fault_baixo',
        # f'{path_dados_brutos}/overhang/cage_fault/20g':'cage_fault_medio',
        # f'{path_dados_brutos}/overhang/cage_fault/35g':'cage_fault_alto',

        # f'{path_dados_brutos}/overhang/outer_race/0g':'outer_race_baixo',
        f'{path_dados_brutos}/overhang/outer_race/6g':'outer_race_baixo',
        f'{path_dados_brutos}/overhang/outer_race/20g':'outer_race_medio',
        f'{path_dados_brutos}/overhang/outer_race/35g':'outer_race_alto',
           
        # f'{path_dados_brutos}/underhang/ball_fault/0g':'ball_fault_baixo',
        f'{path_dados_brutos}/underhang/ball_fault/6g':'ball_fault_baixo',
        f'{path_dados_brutos}/underhang/ball_fault/20g':'ball_fault_medio',
        f'{path_dados_brutos}/underhang/ball_fault/35g':'ball_fault_alto',

        # f'{path_dados_brutos}/underhang/cage_fault/0g':'cage_fault_baixo',
        # f'{path_dados_brutos}/underhang/cage_fault/6g':'cage_fault_baixo',
        # f'{path_dados_brutos}/underhang/cage_fault/20g':'cage_fault_medio',
        # f'{path_dados_brutos}/underhang/cage_fault/35g':'cage_fault_alto',

        # f'{path_dados_brutos}/underhang/outer_race/0g':'outer_race_baixo',
        f'{path_dados_brutos}/underhang/outer_race/6g':'outer_race_baixo',
        f'{path_dados_brutos}/underhang/outer_race/20g':'outer_race_medio',
        f'{path_dados_brutos}/underhang/outer_race/35g':'outer_race_alto',
           }

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

        #     'rolamento_interno_axial':1,
            'rolamento_interno_radial1':2,
            'rolamento_interno_radial2':3,
            
        #     'rolamento_externo_axial':4,
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

# ball_fault = 1.8710 # Original
ball_fault_overhang = 1.9860 # Adequado para pasta ='database/dados_brutos/overhang/ball_fault/35g'
ball_fault_underhang = 1.9678 # Adequado para pasta ='database/dados_brutos/underhang/ball_fault/35g'


# cage_fault = 0.3750 # Original
# cage_fault_overhang = 0.3750
# cage_fault_underhang = 0.3750

# outer_race = 2.9980 # Original
outer_race_overhang = 2.9780
outer_race_underhang = 3.0000

# inner_race = 5.0020 # Original
# inner_race_overhang = 5.0020
# inner_race_underhang = 5.0020

frequencias_rolamento_overhang = [ball_fault_overhang,
                                #     cage_fault_overhang,
                                    outer_race_overhang,
                                #     inner_race_overhang
                                    ]

frequencias_rolamento_underhang = [ball_fault_underhang,
                                #     cage_fault_underhang,
                                    outer_race_underhang,
                                #     inner_race_underhang
                                    ]

frequencias_rolamento = {'externo':frequencias_rolamento_overhang,
                        'interno':frequencias_rolamento_underhang}

harmonico = 10

# -----------------------------------------------
# --------- Defeitos Impostos -------------------
# -----------------------------------------------

testes = ['horizontal-misalignment','imbalance','normal','overhang','underhang','vertical-misalignment']
defeitos_desbalanceamento = ['6g','10g','15g','20g','25g','30g','35g'] # g gramas de desbalancemanto
defeitos_desalinhamento_horizontal = ['0.5mm','1.0mm','1.5mm','2.0mm'] # mm de desalinhamento horizontal
defeitos_desalinhamento_vertical = ['0.51mm','0.63mm','1.27mm','1.40mm','1.78mm','1.90mm'] # mm de desalinhamento vertical

defeito_rolamento = ['ball_fault',
                    # 'cage_fault',
                    'outer_race',
                    # 'inner_race',
                    'rotacao_hz']

desbalanceamento_rolamento = ['0g','6g','20g','35g']

defeitos = ['normal',
            'desalinhamento_horizontal_baixo','desalinhamento_horizontal_médio','desalinhamento_horizontal_alto',
            'desalinhamento_vertical_baixo','desalinhamento_vertical_médio','desalinhamento_vertical_alto',
            'desbalanceamento_baixo','desbalanceamento_médio','desbalanceamento_alto',
            'ball_fault_baixo','ball_fault_médio','ball_fault_alto',
            # 'cage_fault_baixo','cage_fault_médio','cage_fault_alto',
            'outer_race_baixo','outer_race_médio','outer_race_alto'
            # ,'inner_race_baixo','inner_race_médio','inner_race_alto'
            ]



# -----------------------------------------------
# --------- Colunas do DataFrame ----------------
# -----------------------------------------------

colunas_tempo = ['rotacao_hz',
                 'maximo','rms',
                 'assimetria',
                 'curtose',
                 'fator_crista',
                 'defeito']

colunas_freq_pot_relativa = [
                'pot_relativa_ball_fault',
                # 'pot_relativa_cage_fault',
                'pot_relativa_outer_race',
                # 'pot_relativa_inner_race',
                'pot_relativa_rotacao_hz',
                'defeito']

colunas_freq_pot = [
                'pot_ball_fault',
                # 'pot_cage_fault',
                'pot_outer_race',
                # 'pot_inner_race',
                'pot_rotacao_hz',
                'defeito']

coluna_sensor = ['sensor']

colunas = [
            'rotacao_hz',
            'maximo','rms',
            'assimetria',
            'curtose',
            'fator_crista',

            'pot_ball_fault',
            'pot_outer_race',
            'pot_rotacao_hz',

            'pot_relativa_ball_fault',
            'pot_relativa_outer_race',
            'pot_relativa_rotacao_hz',

            'sensor',
            'defeito']


colunas_pot = [
                'rotacao_hz',
                'maximo','rms',
                'assimetria',
                'curtose',
                'fator_crista',

                'pot_ball_fault',
                'pot_outer_race',
                'pot_rotacao_hz',

                'sensor',
                'defeito']

colunas_pot_relativa = [
                'rotacao_hz',
                'maximo','rms',
                'assimetria',
                'curtose',
                'fator_crista',

                'pot_relativa_ball_fault',
                'pot_relativa_outer_race',
                'pot_relativa_rotacao_hz',

                'sensor',
                'defeito']


# -----------------------------------------------
# --------- Machine Learning Sets ---------------
# -----------------------------------------------

seed = 10
test_size = 0.51


time_window = 1
overlap = 0.51