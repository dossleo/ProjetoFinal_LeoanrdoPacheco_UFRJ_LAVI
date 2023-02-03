import models
from models import gerar_csv
from os import listdir


numero_de_ordens = 10

gerar = gerar_csv.RunCSV(numero_de_ordens)
gerar.Run()

