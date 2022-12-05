import models
from models import (run)

modelo = run.GenerateCSV(path = models.PATH_TEST["Test2"],
                        column=models.test2["bearing1"],
                        filter_order=5,
                        order_frequency=4,
                        window_frequency=40)

modelo.save_as_csv(name = 'features_2nd_test_bearing1.csv')