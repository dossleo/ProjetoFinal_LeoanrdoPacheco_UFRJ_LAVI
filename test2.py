import models
from models import indicadores_referencia
import pandas as pd

percentual_primeiras_medidas = 0.01
freq_referencia = 10
no_ordens_frequencia = 1
largura_banda = 2
freq_passa_baixa = 1000
orden_filtro = 5


Teste = indicadores_referencia.IndicadoresReferencia(percentual_primeiras_medidas,
                                                    no_ordens_frequencia,
                                                    largura_banda,
                                                    freq_passa_baixa,
                                                    orden_filtro=5)

dados = Teste.extrair()
print(len(dados))
print(dados)
breakpoint()