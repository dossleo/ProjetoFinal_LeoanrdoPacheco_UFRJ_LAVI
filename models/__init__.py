import os

freq_sample = 20480
rpm = 2000

frequency_fundamental_train = 0.0072*rpm
frequency_inner_ring_defect = 0.1617*rpm
frequency_outer_ring_defect = 0.1217*rpm
frequency_roller_spin = 0.0559*rpm

raw_data_path = os.path.join(os.getcwd(), "database", "brutos")

# set number = {Bearing number : channel number}
test1 = {"bearing1x":1,"bearint1y":2,
        "bearing2x":3,"bearint2y":4,
        "bearing3x":5,"bearint3y":6,
        "bearing4x":7,"bearint4y":8}

test2 = {"bearing1":1,
        "bearint2":2,
        "bearint3":3,
        "bearint4":4}

test3 = {"bearing1":1,
        "bearint2":2,
        "bearint3":3,
        "bearint4":4}