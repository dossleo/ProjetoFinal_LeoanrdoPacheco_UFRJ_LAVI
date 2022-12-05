import os
import models

PATH_1ST_DATABASE = 'database/brutos/1st_test'
PATH_2ND_DATABASE = 'database/brutos/2nd_test'
PATH_3RD_DATABASE = 'database/brutos/3rd_test'

PATH_TEST = {"Test1": PATH_1ST_DATABASE,"Test2":PATH_2ND_DATABASE, "Test3":PATH_3RD_DATABASE}

RPM_ARTIFICIAL_FILE = 'database/2000rpm_artificial_data.csv'

# General configs
DEBUG = True


freq_sample = 20480
rpm = 2000

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
test1 = {"bearing1x":0,"bearint1y":1,
        "bearing2x":2,"bearint2y":3,
        "bearing3x":4,"bearint3y":5,
        "bearing4x":6,"bearint4y":7}

test2 = {"bearing1":0,
        "bearint2":1,
        "bearint3":2,
        "bearint4":3}

test3 = {"bearing1":0,
        "bearint2":1,
        "bearint3":2,
        "bearint4":3}

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