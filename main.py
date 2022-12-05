import models
from models import (run)

modelo = run.GenerateCSV(path = models.PATH_2ND_DATABASE,
                        column=models.test2["bearing1"],
                        filter_order=5,
                        order_frequency=9,
                        window_frequency=50)

modelo.print_dataframe()