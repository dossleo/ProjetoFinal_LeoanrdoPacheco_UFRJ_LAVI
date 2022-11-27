from models import _data_normalization, _frequency_features_extraction, _get_data, _low_pass_filter, _time_features_extraction
import models
import pandas as pd

if __name__ == "__main__":
    
    for file in models.filenames:
        # Definição de frequência de aquisição
        fs = models.freq_sample
        
    # Passo 1: Descobrir maior frequência de defeito do rolamento
        maior_freq_defeito = max(models.fault_frequency)

    # Passo 2: Passar filtro passa baixa um pouco acima dessa frequência
        
        # Extraindo dados brutos
        raw_data = _get_data.GetData(models.path,file).Get()
        
        # Definindo ordem do filtro
        order = 5

        # Definindo frequência de aplicação do filtro
        cutoff = maior_freq_defeito*4

        dados_filtrados = _low_pass_filter.LowPassFilter(raw_data,cutoff,order)
        # dados_filtrados.PlotTimeDomain(plot_raw_data = False)

        dados_filtrados = dados_filtrados.lowpass_filter()


    # Passo 3: Normalizar os dados

        dados_normalizados = _data_normalization.DataNormalized(dados_filtrados)

    # Passo 4: Aplicar métricas no domínio do tempo

        dominio_tempo = _time_features_extraction.TimeFeatures(dados_normalizados.Get())

    # Passo 5: Aplicar FFT

        dominio_frequencia = _frequency_features_extraction.FrequencyFeaturesExtraction(dados_normalizados.Get())
        frequencia_referencia = models.frequency_outer_ring_defect
        ordens = 9
        janela = 60
        # dominio_frequencia.PlotFrequencyDomain(frequencia_referencia,ordens)

    # Passo 6: Aplicar métricas do domínio do tempo nas janelas de frequência
        media = dominio_frequencia.MediaOrdens(frequencia_referencia,janela,ordens)
        metricas = dominio_frequencia.metricas

        print('-------------')
        print('METRICAS')
        print(metricas)
        print('-------------')
        print('Medias')
        print(media)
        print('-------------')
        print('-------------')
        print('-------------')
