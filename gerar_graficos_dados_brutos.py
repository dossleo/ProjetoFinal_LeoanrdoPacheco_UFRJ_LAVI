import models
from models import visualizar_dados

import os

# pasta =f'{models.path_dados_brutos}/normal'

# pasta =f'{models.path_dados_brutos}/horizontal-misalignment/0.5mm'
# pasta =f'{models.path_dados_brutos}/horizontal-misalignment/1.0mm'
# pasta =f'{models.path_dados_brutos}/horizontal-misalignment/1.5mm'
# pasta =f'{models.path_dados_brutos}/horizontal-misalignment/2.0mm'

# pasta =f'{models.path_dados_brutos}/imbalance/6g'
# pasta =f'{models.path_dados_brutos}/imbalance/10g'
# pasta =f'{models.path_dados_brutos}/imbalance/15g'
# pasta =f'{models.path_dados_brutos}/imbalance/20g'
# pasta =f'{models.path_dados_brutos}/imbalance/25g'
# pasta =f'{models.path_dados_brutos}/imbalance/30g'
# pasta =f'{models.path_dados_brutos}/imbalance/35g'

# pasta =f'{models.path_dados_brutos}/overhang/ball_fault/0g'
# pasta =f'{models.path_dados_brutos}/overhang/ball_fault/6g'
# pasta =f'{models.path_dados_brutos}/overhang/ball_fault/20g'
pasta =f'{models.path_dados_brutos}/overhang/ball_fault/35g'

# pasta =f'{models.path_dados_brutos}/overhang/cage_fault/0g'
# pasta =f'{models.path_dados_brutos}/overhang/cage_fault/6g'
# pasta =f'{models.path_dados_brutos}/overhang/cage_fault/20g'
# pasta =f'{models.path_dados_brutos}/overhang/cage_fault/35g'

# pasta =f'{models.path_dados_brutos}/overhang/outer_race/0g'
# pasta =f'{models.path_dados_brutos}/overhang/outer_race/6g'
# pasta =f'{models.path_dados_brutos}/overhang/outer_race/20g'
# pasta =f'{models.path_dados_brutos}/overhang/outer_race/35g'
 
# pasta =f'{models.path_dados_brutos}/underhang/ball_fault/0g'
# pasta =f'{models.path_dados_brutos}/underhang/ball_fault/6g'
# pasta =f'{models.path_dados_brutos}/underhang/ball_fault/20g'
# pasta =f'{models.path_dados_brutos}/underhang/ball_fault/35g'

# pasta =f'{models.path_dados_brutos}/underhang/cage_fault/0g'
# pasta =f'{models.path_dados_brutos}/underhang/cage_fault/6g'
# pasta =f'{models.path_dados_brutos}/underhang/cage_fault/20g'
# pasta =f'{models.path_dados_brutos}/underhang/cage_fault/35g'

# pasta =f'{models.path_dados_brutos}/underhang/outer_race/0g'
# pasta =f'{models.path_dados_brutos}/underhang/outer_race/6g'
# pasta =f'{models.path_dados_brutos}/underhang/outer_race/20g'
# pasta =f'{models.path_dados_brutos}/underhang/outer_race/35g'

arquivo = os.listdir(pasta)[-1]

numero_sensor = 2
posicao_sensor = 'externo'
numero_frequencia_referencia = 1

plotar_tempo = True
plotar_frequencia = True


if plotar_tempo:
    Objeto_Visualizar_Tempo = visualizar_dados.VisualizarTempo( pasta=pasta,
                                                                arquivo=arquivo,
                                                                numero_sensor=numero_sensor,
                                                                posicao=posicao_sensor,
                                                                title=f' - Rolamento número {numero_sensor} {posicao_sensor}')

    Objeto_Visualizar_Tempo.plt_sinal(  salvar=True,
                                        plotar=True)


if plotar_frequencia:
    Objeto_visualizar_Freq = visualizar_dados.VisualizarFrequencia(  pasta=pasta,
                                                                    arquivo=arquivo,
                                                                    numero_sensor=numero_sensor,
                                                                    posicao=posicao_sensor,
                                                                    num_frequencia_referencia=numero_frequencia_referencia)
    # Objeto_visualizar.plotar_fft()
    Objeto_visualizar_Freq.plotar_fft(  salvar=True,
                                        plotar=True)

    Objeto_visualizar_Freq.plotar_fft_com_frequencia_de_referencia( salvar=True,
                                                                    plotar=True)

    Objeto_visualizar_Freq.plotar_bandas(10)
