import models
from models import visualizar_dados, get_rpm

import os

pasta =f'{models.path_dados_brutos}/normal'

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

def ploter_graficos(numero_sensor,posicao_sensor,numero_frequencia_referencia,pasta,path_to_save):
    numero_sensor = 2
    posicao_sensor = 'externo'
    numero_frequencia_referencia = 1

    executar_grafico_tempo = True
    executar_grafico_frequencia = True
    executar_grafico_rpm = True

    if executar_grafico_rpm:
        Objeto_RPM = get_rpm.PlotRPMPASTAS(pasta).plot_rpm_pasta_inteira()


    if executar_grafico_tempo:
        Objeto_Visualizar_Tempo = visualizar_dados.VisualizarTempo( pasta=pasta,
                                                                    arquivo=arquivo,
                                                                    numero_sensor=numero_sensor,
                                                                    posicao=posicao_sensor,
                                                                    title=f' - Rolamento número {numero_sensor} {posicao_sensor}')
        Objeto_Visualizar_Tempo.plt_sinal(  salvar=True,
                                            plotar=False)


    if executar_grafico_frequencia:
        Objeto_visualizar_Freq = visualizar_dados.VisualizarFrequencia(  pasta=pasta,
                                                                        arquivo=arquivo,
                                                                        numero_sensor=numero_sensor,
                                                                        posicao=posicao_sensor,
                                                                        num_frequencia_referencia=numero_frequencia_referencia)
        Objeto_visualizar_Freq.plotar_fft(  salvar=True,
                                            plotar=False)
        Objeto_visualizar_Freq.plotar_fft_com_frequencia_de_referencia( salvar=True,
                                                                        plotar=False)
        Objeto_visualizar_Freq.plotar_bandas(10)

