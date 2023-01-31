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
microfone = 8

colunas = {'rotacao':rotacao,'rolamento_interno':rolamento_interno,'rolamento_externo':rolamento_externo,'microfone':microfone}

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

frequencias_rolamento = [frequencia_esfera,
                        frequencia_gaiola,
                        frequencia_pista_externa
                        ,frequencia_pista_interna]



# -----------------------------------------------
# --------- Defeitos Impostos -------------------
# -----------------------------------------------


testes = ['horizontal-misalignment','imbalance','normal','overhang','underhang','vertical-misalignment']
defeitos_desbalanceamento = ['6g','10g','15g','20g','25g','30g','35g'] # g gramas de desbalancemanto
defeitos_desalinhamento_horizontal = ['0.5mm','1.0mm','1.5mm','2.0mm'] # mm de desalinhamento horizontal
defeitos_desalinhamento_vertical = ['0.51mm','0.63mm','1.27mm','1.40mm','1.78mm','1.90mm'] # mm de desalinhamento vertical

defeito_rolamento = ['ball_fault','cage_fault','outer_race','inner_race']
desbalanceamento_rolamento = ['0g','6g','20g','35g']


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
            indicadores.append(f'potencia_{defeito}')
            indicadores.append(f'soma_{defeito}')