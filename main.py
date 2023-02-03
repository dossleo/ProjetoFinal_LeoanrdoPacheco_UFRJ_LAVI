import models
from models import gerar_csv

Objeto_GerarCSV = gerar_csv.GerarCSV(
                                    sensor_inicial=2,
                                    no_ordens=10,
                                    ordem_inicial=2
                                    )

Objeto_GerarCSV.run()