import os
import models

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

raw_data_path = os.path.join(os.getcwd(), "database", "brutos")

path=r'database/brutos/2nd_test'
filenames = os.listdir(path)
# filenames = ['2004.02.19.05.52.39','2004.02.18.02.42.39']

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