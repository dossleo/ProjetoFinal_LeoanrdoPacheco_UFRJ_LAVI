import datetime
import os
import time

import numpy as np
import pandas as pd
from rich import pretty, print

import models
from models import extrair_indicadores, get_rpm, normalizar_sinal, get_raw_data

pretty.install()

# Classe para instanciar métodos genéricos que serão utilizados em outras classes
class GeneralFuncions():

    PASTAS = models.PATH

    # retorna uma lista de arquivos contidos em uma pasta
    def listar_arquivos(self, pasta:str) -> list:
        arquivos = os.listdir(pasta)
        return arquivos

    # Lê um dataframe a partir de uma pasta
    def ler_dataframe(self, pasta, arquivo):
        caminho = os.path.join(pasta,arquivo)
        columns = [0,1,2,3,4,5,6,7]
        return pd.read_csv(caminho, sep=',', names=columns, header=None)

    # Extrai uma coluna de um dataframe
    def extrair_coluna(self, dataframe:pd.DataFrame, n_coluna:int):
        return np.array(dataframe[n_coluna])

    # Inicia a contagem de que horas iniciou o tratamento de dados
    def iniciar_contagem(self):
        start = time.time()
        now = datetime.datetime.now()
        now = now.strftime("%d/%m/%Y - %H:%M:%S")

        print(f'___________________________\nInício: {now}\n')
        return start
    
    # Pegar o tempo decorrido até o momento a partir do start
    def tempo_decorrido(self, start, ciclo_atual, ciclos_totais,ordem,cont):
            elapsed_time = time.time() - start

            # Evita divisão por zero
            if ciclo_atual > 0:
                tempo_estimado = elapsed_time*((ciclos_totais/ciclo_atual)-1)
            else:
                tempo_estimado = 0
            
            print(f'\nOrdem: {ordem}\nPastas Percorridas: {cont}/{len(models.PATH)}\nAndamento Total: {np.round(100*ciclo_atual/ciclos_totais,2)}%')
            print("Tempo decorrido: {:02}:{:02}:{:02}".format(int(elapsed_time // 3600), int(elapsed_time % 3600 // 60), int(elapsed_time % 60)))
            print("Tempo Estimado até o Fim: {:02}:{:02}:{:02}".format(int(tempo_estimado // 3600), int(tempo_estimado % 3600 // 60), int(tempo_estimado % 60)))
    

# Classe que gera os dados tratados e salva em csv
class GerarCSV(GeneralFuncions):
    
    PASTAS = models.PATH
    SENSORES = models.sensores
    FREQUENCIAS_REF = models.frequencias_rolamento
    COLUNA_RPM = 0
    COLUNA_CONFERE_RPM = 2

    def __init__(self, ordem_inicial:int, ordem_final:int) -> None:
        self.ordem_inicial = ordem_inicial
        self.ordem_final = ordem_final
        super().__init__()

    # Calcula o total de ciclos que o processamento de dados irá fazer
    def calcula_ciclos_totais(self,ordem_inicial,ordem_final):  # Ver como ta isso
        num_ordens = int(ordem_inicial-ordem_final+1)
        num_pastas = len(self.PASTAS)
        return num_ordens*num_pastas

    # gera uma lista contendo todas as ordens que deverão ser analisadas
    def gerar_lista_ordem(self):
        return list(range(self.ordem_inicial,self.ordem_final+1))

    # Define a frequência de referência que será utilizada de acordo com o rolamento (interno ou externo)
    # Cada rolamento possui pequenas variações em sua frequência de referência
    def calcular_freq_ref(self, acelerometro:str, rpm:float):
        if acelerometro.__contains__("externo"):
            freq = models.frequencias_rolamento.get("externo")
        else:
            freq = models.frequencias_rolamento.get("interno")

        freq = np.array(freq)
        return freq*rpm

    # A partir de um dataframe de dado bruto, calcula o rpm associado a este sinal
    def calcular_rpm(self, dataframe):
        sinal_rpm = self.extrair_coluna(dataframe, self.COLUNA_RPM)
        sinal_sensor = self.extrair_coluna(dataframe, self.COLUNA_CONFERE_RPM)
        rpm_medio = get_rpm.GetRPM(sinal_rpm, sinal_sensor).get_rpm_medio('hz')
        return rpm_medio

    # Salva os dados de um dicionário como um arquivo csv
    def salvar_dados(self, dados:dict, ordem:int,pasta:str=''):
        local = f'{models.path_dados_tratados}/ordens_{ordem}'
        dataframe = pd.json_normalize(dados)
        dataframe = dataframe[dataframe.columns[len(dataframe.columns)-len(models.colunas):len(dataframe.columns)]]
        dataframe.to_csv(f'{local}/{models.nome_padrao_de_arquivo}_concatenado.csv')

    # método que executa toda a rotina de extração de dados
    def executar(self):
        ciclos_totais = self.calcula_ciclos_totais(self.ordem_inicial,self.ordem_final)
        ciclo_atual = 0
        start = self.iniciar_contagem()

        ordens = self.gerar_lista_ordem()
        # percorre a lista de ordens
        for ordem in ordens:
            lista_dados = []
            cont = 0
            # Percorre a lista de pastas
            for pasta in self.PASTAS:
                defeito = self.PASTAS.get(pasta)
                arquivos = self.listar_arquivos(pasta)
  
                defeito = self.PASTAS[pasta]
                local = f'{models.path_dados_tratados}/ordens_{ordem}'
                local = f'{local}/{models.nome_padrao_de_arquivo}_{defeito}.csv'

                # Verifica se a pasta existe
                if os.path.exists(local):
                    print(f'O arquivo {local} existe.')

                else:
                    # Percorre todos os arquivos presentes na pasta atual
                    for arquivo in arquivos:
                        dataframe = self.ler_dataframe(pasta,arquivo)
                        rpm = self.calcular_rpm(dataframe)
                        # percorre as colunas associadas com cada acelerômetro dentro do dataframe atual
                        for acelerometro in self.SENSORES:
                            col_acelerometro = self.SENSORES.get(acelerometro)
                            array_sensor = self.extrair_coluna(dataframe, col_acelerometro)
                            freq_referencia = self.calcular_freq_ref(acelerometro, rpm)

                            # Extrai os indicadores da coluna de sinal atual
                            dados = extrair_indicadores.ExtrairIndicadores(
                                sinal=array_sensor,
                                rpm=rpm,
                                defeito=defeito,
                                freq_referencia=freq_referencia,
                                sensor = acelerometro
                            ).Get(ordem)

                            # Concatena os dados a cada loop para salvar em csv
                            lista_dados = lista_dados + dados
                
                # Calcula quanto uma aproximação de quanto tempo falta para finalizar todos os diclos baseado no tempo decorrido
                cont+=1
                ciclo_atual+=1
                self.tempo_decorrido(start=start, ciclo_atual=ciclo_atual, ciclos_totais = ciclos_totais,cont=cont, ordem=ordem)
            
            # Salva os dados concatenados em csv
            self.salvar_dados(lista_dados, ordem,pasta)

            # Normalizar e Salvar Dados tratados
            pasta_completa = f'database/dados_tratados/ordens_{ordem}'
            arquivo_completo = f'{models.nome_padrao_de_arquivo}_concatenado.csv'
            df_completo = get_raw_data.GetData(pasta_completa,arquivo_completo).GetDataframe()
            normalizar_sinal.NormalizarSinal(df_completo,ordem,metodo=2).save_as_csv()

            # Limpa a memória alocada em lista_dados
            lista_dados = []

