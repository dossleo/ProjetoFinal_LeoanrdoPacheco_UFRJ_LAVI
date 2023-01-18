import models
from models import (run)

for test_number in range(len(models.PATH_TEST)):
    for bearing in models.bearings[test_number]:
        nome_teste = f'test{test_number+1}'
        rolamento = bearing
        path =  models.PATH_TEST[test_number]
        column = models.bearings[test_number][bearing]
        filter_order = 5
        order_frequency=1
        for w in range(4):
            window_frequency=w

            modelo = run.GenerateCSV(path =path,
                                    column=column,
                                    filter_order=filter_order,
                                    order_frequency=order_frequency,
                                    window_frequency = window_frequency)

            modelo.print_dataframe()
            # modelo.save_as_csv(name = f'features_{nome_teste}_{rolamento}_filter{filter_order}_order{order_frequency}_window{window_frequency}')