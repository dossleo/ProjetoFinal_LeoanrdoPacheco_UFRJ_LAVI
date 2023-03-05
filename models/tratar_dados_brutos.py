import datetime
import os
import time

import numpy as np
import pandas as pd
from rich import pretty, print

import models
from models import extrair_indicadores, get_rpm, normalizar_sinal, get_raw_data

pretty.install()

# Função para cirar um diretório
def create_dir(harmonico):
    dir_path = os.path.join(f'{models.path_dados_tratados}/harmonicos_{harmonico}')
    if not os.path.exists(dir_path):
        os.mkdir(dir_path)
    return dir_path

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
    def tempo_decorrido(self, start, ciclo_atual, ciclos_totais,harmonico,cont):
            elapsed_time = time.time() - start

            # Evita divisão por zero
            if ciclo_atual > 0:
                tempo_estimado = elapsed_time*((ciclos_totais/ciclo_atual)-1)
            else:
                tempo_estimado = 0
            
            
            print(f'\nHarmônico: {harmonico}\nPastas Percorridas: {cont}/{len(models.PATH)}\nAndamento Total: {np.round(100*ciclo_atual/ciclos_totais,2)}%')
            print("Tempo decorrido: {:02}:{:02}:{:02}".format(int(elapsed_time // 3600), int(elapsed_time % 3600 // 60), int(elapsed_time % 60)))
            print("Tempo Estimado até o Fim: {:02}:{:02}:{:02}".format(int(tempo_estimado // 3600), int(tempo_estimado % 3600 // 60), int(tempo_estimado % 60)))
    

# Classe que gera os dados tratados e salva em csv
class GerarCSV(GeneralFuncions):
    
    PASTAS = models.intensidade_defeitos
    SENSORES = models.sensores
    FREQUENCIAS_REF = models.frequencias_rolamento
    COLUNA_RPM = 0
    COLUNA_CONFERE_RPM = 2

    def __init__(self, harmonico_inicial:int, harmonico_final:int) -> None:
        self.harmonico_inicial = harmonico_inicial
        self.harmonico_final = harmonico_final
        super().__init__()

    # Calcula o total de ciclos que o processamento de dados irá fazer
    def calcula_ciclos_totais(self,harmonico_inicial,harmonico_final):  # Ver como ta isso
        num_harmonicos = int(harmonico_final-harmonico_inicial+1)
        num_pastas = len(self.PASTAS)
        return num_harmonicos*num_pastas

    # gera uma lista contendo todas as harmonicos que deverão ser analisadas
    def gerar_lista_harmonico(self):
        return list(range(self.harmonico_inicial,self.harmonico_final+1))

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
    def salvar_dados(self, dados:dict, harmonico:int):
        local = create_dir(harmonico=harmonico)

        dataframe = pd.json_normalize(dados)
        # dataframe = dataframe[dataframe.columns[len(dataframe.columns)-len(models.colunas):len(dataframe.columns)]]
        dataframe.to_csv(f'{local}/{models.nome_padrao_de_arquivo}_concatenado_novo.csv')

    # método que executa toda a rotina de extração de dados
    def executar(self):
        ciclos_totais = self.calcula_ciclos_totais(self.harmonico_inicial,self.harmonico_final)
        ciclo_atual = 0
        start = self.iniciar_contagem()

        harmonicos = self.gerar_lista_harmonico()
        # percorre a lista de harmonicos
        for harmonico in harmonicos:
            lista_dados = []
            cont = 0
            # Percorre a lista de pastas
            for pasta in self.PASTAS:
                defeito = self.PASTAS.get(pasta)

                arquivos = self.listar_arquivos(pasta)
  
                local = f'{models.path_dados_tratados}/harmonicos_{harmonico}'
                local = f'{local}/{models.nome_padrao_de_arquivo}_{defeito[0]}_novo.csv'

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
                            ).Get(harmonico)

                            # Concatena os dados a cada loop para salvar em csv
                            lista_dados = lista_dados + dados
                
                # Calcula quanto uma aproximação de quanto tempo falta para finalizar todos os diclos baseado no tempo decorrido
                cont+=1
                ciclo_atual+=1
                self.tempo_decorrido(start=start, ciclo_atual=ciclo_atual, ciclos_totais = ciclos_totais,cont=cont, harmonico=harmonico)
            
            # Salva os dados concatenados em csv
            
            self.salvar_dados(dados=lista_dados, harmonico=harmonico)

            # Normalizar e Salvar Dados tratados
            pasta_completa = f'database/dados_tratados/harmonicos_{harmonico}'
            arquivo_completo = f'{models.nome_padrao_de_arquivo}_concatenado_novo.csv'
            df_completo = get_raw_data.GetData(pasta_completa,arquivo_completo).GetDataframe()
            normalizar_sinal.NormalizarSinal(df_completo,harmonico,metodo=2).save_as_csv()

            # Limpa a memória alocada em lista_dados
            lista_dados = []

