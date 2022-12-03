from models import _data_normalization, _frequency_features_extraction, _get_data, _low_pass_filter, _time_features_extraction, generate_rpm, get_rpm
import models
import pandas as pd
import matplotlib.pyplot as plt

if __name__ == "__main__":
    # Definição de frequência de aquisição
    fs = models.freq_sample
    
    # Gerar RPM
    gerar_rpm = generate_rpm.GenerateRPM(2000,20480)
    df_rpm = gerar_rpm.generate_array()
    # gerar_rpm.plot_array()

    pegar_rpm = get_rpm.GetRPM(df_rpm,models.freq_sample)
    rpm_pontos = pegar_rpm.get_rpm_ponto_a_ponto()
    rpm_medio = pegar_rpm.get_rpm_medio()
    # pegar_rpm.plot_picos()
    # pegar_rpm.plot_rpm()

    # breakpoint()

for fault in range(len(models.fault_frequency)):
# Passo 1: Descobrir maior frequência de defeito do rolamento
    maior_freq_defeito = max(models.fault_frequency)*rpm_medio
    dataframe = []
    for file in models.filenames:

    # Passo 2: Passar filtro passa baixa um pouco acima dessa frequência
        
        # Extraindo dados brutos
        raw_data = _get_data.GetData(models.path,file).Get()
        
        # Definindo ordem do filtro
        order = 7

        # Definindo frequência de aplicação do filtro
        cutoff = rpm_medio*2

        dados_filtrados = _low_pass_filter.LowPassFilter(raw_data,cutoff,order)
        dados_filtrados.plot_time_domain(plot_raw_data = False)

        # Dados brutos após aplicação do filtro
        dados_filtrados = dados_filtrados.lowpass_filter()

        # breakpoint()

    # Passo 3: Normalizar os dados

        # Dados filtrados após aplicação da normalização da frequência
        dados_normalizados = _data_normalization.DataNormalized(dados_filtrados)
        dados_normalizados.plot_normal_data()

        # breakpoint()

    # Passo 4: Aplicar métricas no domínio do tempo

        dominio_tempo = _time_features_extraction.TimeFeatures(dados_normalizados.get())

    # Passo 5: Aplicar métricas no domínio da frequência

        dominio_frequencia = _frequency_features_extraction.FrequencyFeaturesExtraction(dados_normalizados.get(),rpm_medio)
        frequencia_referencia = 2000 #models.fault_frequency[fault]*rpm_medio
        ordens = 1
        janela = 50
        dominio_frequencia.plot_frequency_domain(frequencia_referencia,ordens)
        dominio_frequencia.plot_window(frequencia_referencia,janela)
        # breakpoint()
        dominio_frequencia.window_around_frequency(frequencia_referencia,janela)

    # Passo 6: Aplicar métricas do domínio do tempo nas janelas de frequência
        media = dominio_frequencia.get_features(frequencia_referencia,janela,ordens)
        metricas = dominio_frequencia.metricas

        dataframe.append(media)

        # print('-------------')
        # print('METRICAS')
        # print(metricas)
        # print('-------------')
        # print(media)
        # print('-------------')


    # Get RPM
    dataframe = pd.json_normalize(dataframe)
    print(dataframe)
    for feature in models.features:
        plt.plot(range(len(models.filenames)),dataframe[feature])
        plt.title(feature + "-" + str(models.fault_frequency[fault]))
        plt.show()

# breakpoint()