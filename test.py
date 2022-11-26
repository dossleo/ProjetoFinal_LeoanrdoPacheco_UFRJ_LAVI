from models import get_data,low_pass_filter,data_normalization, time_features_extraction, frequency_features_extraction
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
        raw_data = get_data.GetData(models.path,file,1).Get()
        
        # Definindo ordem do filtro
        order = 5

        # Definindo frequência de aplicação do filtro
        cutoff = maior_freq_defeito*4

        dados_filtrados = low_pass_filter.LowPassFilter(raw_data,cutoff,order)
        # dados_filtrados.PlotTimeDomain(plot_raw_data = False)

        dados_filtrados = dados_filtrados.lowpass_filter()


    # Passo 3: Normalizar os dados

        dados_normalizados = data_normalization.DataNormalized(dados_filtrados)

    # Passo 4: Aplicar métricas no domínio do tempo

        dominio_tempo = time_features_extraction.TimeFeatures(dados_normalizados.Get())

    # Passo 5: Aplicar FFT

        dominio_frequencia = frequency_features_extraction.FrequencyFeaturesExtraction(dados_normalizados.Get())
        dominio_frequencia.PlotFrequencyDomain()
        ordens = 9
        janela = 50

    # Passo 6: Aplicar métricas do domínio do tempo nas janelas de frequência
        metricas = []
        
        for i in range(ordens):
            dados = dominio_frequencia.JanelaFrequencia(models.frequency_outer_ring_defect*(i+1),janela)
            metricas_frequencia = time_features_extraction.TimeFeatures(dados)
            metricas.append(metricas_frequencia.run())

        print(pd.json_normalize(metricas))
