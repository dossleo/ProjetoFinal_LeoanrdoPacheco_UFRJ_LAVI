from models.tratar_dados_brutos import GerarCSV
import os

os.system("cls")

harmonico_inicial = 1
harmonico_final = 1

GerarCSV(harmonico_inicial,harmonico_final).executar()

