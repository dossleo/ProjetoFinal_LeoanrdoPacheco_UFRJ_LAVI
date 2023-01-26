import os
import models

PATH_1ST_DATABASE = 'database/brutos/1st_test'
PATH_2ND_DATABASE = 'database/brutos/2nd_test'
PATH_3RD_DATABASE = 'database/brutos/3rd_test'

PATH_TEST = [PATH_1ST_DATABASE,PATH_2ND_DATABASE,PATH_3RD_DATABASE]

RPM_ARTIFICIAL_FILE = 'database/2000rpm_artificial_data.csv'

# General configs
DEBUG = True


freq_sample = 20480 #Hz
rpm = 2000 #rpm
rotacao_hz = rpm/60

# Dados encontrados em https://www.rexnord.com/products/za2115
frequency_fundamental_train = 0.0072
frequency_inner_ring_defect = 0.1617
frequency_outer_ring_defect = 0.1217
frequency_roller_spin = 0.0559

fault_frequency = [frequency_fundamental_train
                ,frequency_inner_ring_defect
                ,frequency_outer_ring_defect
                ,frequency_roller_spin]

fault_names = ['freq_train'
                ,'freq_inner_race'
                ,'freq_outer_race'
                ,'freq_roller']

# set number = {Bearing number : channel number}
test1 = {"bearing1x":0,"bearing1y":1,
        "bearing2x":2,"bearing2y":3,
        "bearing3x":4,"bearing3y":5,
        "bearing4x":6,"bearing4y":7}

test2 = {"bearing1":0,
        "bearing2":1,
        "bearing3":2,
        "bearing4":3}

test3 = {"bearing1":0,
        "bearing2":1,
        "bearing3":2,
        "bearing4":3}

bearings = [test1,test2,test3]

features = ['maximum',
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
            features.append(f'potencia_{defeito}')
            features.append(f'soma_{defeito}')