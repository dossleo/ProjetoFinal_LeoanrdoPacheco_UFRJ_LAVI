import models
from models import indicadores_frequencia, indicadores_tempo, get_raw_data, extrair_indicadores, filtro_passa_baixa
import os
import pandas as pd

for frequencia_funcamental in models.fault_frequency:

    frequencia_de_referencia = frequencia_funcamental*models.rotacao_hz
    sinal = get_raw_data.GetData(models.PATH_1ST_DATABASE,os.listdir(models.PATH_1ST_DATABASE)[0],0).Get()

    Filtro = filtro_passa_baixa.LowPassFilter(sinal,cutoff=models.rpm*(20/60))

    Filtro.plot_time_domain(plot_raw_data=False)
    Filtro.plot_time_domain(plot_raw_data=True)

    sinal_filtrado = Filtro.lowpass_filter()

    Teste = indicadores_frequencia.DominioFrequencia(sinal_filtrado,models.rpm,models.freq_sample)

    Teste.plot_banda(frequencia_de_referencia,20000)

    # Teste.pegar_indicador(505,5,4)

    # sinal_fourier,sinal_frequencia = Teste.banda_frequencia(505,5)

    # print(Teste.potencia_sinal(sinal_fourier*2))

    for i in range(4):
        Teste.plot_potencia_sinal(10*(i+1))

    teste_extrair = extrair_indicadores.ExtrairIndicadores(sinal_filtrado,frequencia_de_referencia,20)

    print(pd.json_normalize(teste_extrair.Get(4)))