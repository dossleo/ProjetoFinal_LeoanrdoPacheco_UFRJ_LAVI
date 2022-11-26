from models import get_data,low_pass_filter,data_normalization, time_features_extraction, frequency_features_extraction
import models

if __name__ == "__main__":
    
    # Definição de frequência de aquisição
    fs = models.freq_sample
    
# Passo 1: Descobrir maior frequência de defeito do rolamento
    maior_freq_defeito = max(models.fault_frequency)

# Passo 2: Passar filtro passa baixa um pouco acima dessa frequência
    
    # Extraindo dados brutos
    raw_data = get_data.GetData(models.path,models.filename,1).Get()
    
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

# Passo 4: Aplicar FFT

    dominio_frequencia = frequency_features_extraction.FrequencyFeaturesExtraction(dados_normalizados.Get())
    dominio_frequencia.PlotFrequencyDomain()
    for defeito in models.fault_frequency:
        dominio_frequencia.JanelaFrequencia(defeito,40)

