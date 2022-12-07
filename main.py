import models
from models import (run)

teste = "Test2"
rolamento = "bearing1"
path =  models.PATH_TEST[teste]
column = models.test2[rolamento]
filter_order = 5
order_frequency=4
window_frequency=40

modelo = run.GenerateCSV(path =path,
                        column=column,
                        filter_order=filter_order,
                        order_frequency=order_frequency,
                        window_frequency = window_frequency)

modelo.save_as_csv(name = f'features_{teste}_{rolamento}_filter{filter_order}_order_{order_frequency}_window_{window_frequency}')