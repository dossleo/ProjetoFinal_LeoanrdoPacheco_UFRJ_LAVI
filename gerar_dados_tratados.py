from models.tratar_dados_brutos import GerarCSV
import os

os.system("cls")

harmonico_inicial = 2
harmonico_final = 10

GerarCSV(harmonico_inicial,harmonico_final).executar()

