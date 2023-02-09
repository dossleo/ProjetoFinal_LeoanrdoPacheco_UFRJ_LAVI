from models.tratar_dados_brutos import GerarCSV
import os

os.system("cls")

ordem_inicial = 2
ordem_final = 3

GerarCSV(ordem_inicial,ordem_final).run()

