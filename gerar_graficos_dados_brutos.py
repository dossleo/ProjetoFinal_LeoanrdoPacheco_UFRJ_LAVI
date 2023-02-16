import models
from models import visualizar_dados, get_rpm, criar_pastas, get_raw_data

import os

# pasta ='database/dados_brutos/normal'

# pasta ='database/dados_brutos/horizontal-misalignment/0.5mm'
# pasta ='database/dados_brutos/horizontal-misalignment/1.0mm'
# pasta ='database/dados_brutos/horizontal-misalignment/1.5mm'
# pasta ='database/dados_brutos/horizontal-misalignment/2.0mm'

# pasta ='database/dados_brutos/imbalance/6g'
# pasta ='database/dados_brutos/imbalance/10g'
# pasta ='database/dados_brutos/imbalance/15g'
# pasta ='database/dados_brutos/imbalance/20g'
# pasta ='database/dados_brutos/imbalance/25g'
# pasta ='database/dados_brutos/imbalance/30g'
# pasta ='database/dados_brutos/imbalance/35g'

# pasta ='database/dados_brutos/overhang/ball_fault/0g'
# pasta ='database/dados_brutos/overhang/ball_fault/6g'
# pasta ='database/dados_brutos/overhang/ball_fault/20g'
# pasta ='database/dados_brutos/overhang/ball_fault/35g'

# pasta ='database/dados_brutos/overhang/cage_fault/0g'
# pasta ='database/dados_brutos/overhang/cage_fault/6g'
# pasta ='database/dados_brutos/overhang/cage_fault/20g'
pasta ='database/dados_brutos/overhang/cage_fault/35g'

# pasta ='database/dados_brutos/overhang/outer_race/0g'
# pasta ='database/dados_brutos/overhang/outer_race/6g'
# pasta ='database/dados_brutos/overhang/outer_race/20g'
# pasta ='database/dados_brutos/overhang/outer_race/35g'
 
# pasta ='database/dados_brutos/underhang/ball_fault/0g'
# pasta ='database/dados_brutos/underhang/ball_fault/6g'
# pasta ='database/dados_brutos/underhang/ball_fault/20g'
# pasta ='database/dados_brutos/underhang/ball_fault/35g'

# pasta ='database/dados_brutos/underhang/cage_fault/0g'
# pasta ='database/dados_brutos/underhang/cage_fault/6g'
# pasta ='database/dados_brutos/underhang/cage_fault/20g'
# pasta ='database/dados_brutos/underhang/cage_fault/35g'

# pasta ='database/dados_brutos/underhang/outer_race/0g'
# pasta ='database/dados_brutos/underhang/outer_race/6g'
# pasta ='database/dados_brutos/underhang/outer_race/20g'
# pasta ='database/dados_brutos/underhang/outer_race/35g'

posicao_sensor = 'externo'
numero_sensor = 2
numero_frequencia_referencia = 1

arquivo = os.listdir(pasta)[-1]

executar_grafico_rpm = False
executar_grafico_tempo = True
executar_grafico_frequencia = False

numero_de_harmonicos = 2

sinal_rpm = get_raw_data.GetData(pasta,arquivo,0).Get()
sinal_sensor = get_raw_data.GetData(pasta,arquivo,1).Get()

if executar_grafico_rpm:
    Objeto_RPM_Pasta = get_rpm.PlotRPMPASTAS(pasta).plot_rpm_pasta_inteira(salvar=True,plotar=True)
    Objeto_RPM = get_rpm.GetRPM(sinal_rpm=sinal_rpm,sinal_sensor=sinal_sensor)
    Objeto_RPM.plot_rpm_bruto(plotar=True)
    Objeto_RPM.plot_picos(plotar=True)
    Objeto_RPM.plot_rpm(plotar=True)


if executar_grafico_tempo:
    Objeto_Visualizar_Tempo = visualizar_dados.VisualizarTempo( pasta=pasta,
                                                                arquivo=arquivo,
                                                                numero_sensor=numero_sensor,
                                                                posicao=posicao_sensor,
                                                                title=f' - Rolamento {posicao_sensor} - Sensor número {numero_sensor}'
                                                                )   
    Objeto_Visualizar_Tempo.plt_sinal(  salvar=True,
                                        plotar=True)
    Objeto_Visualizar_Tempo = 0


if executar_grafico_frequencia:
    Objeto_visualizar_Freq = visualizar_dados.VisualizarFrequencia(  pasta=pasta,
                                                                    arquivo=arquivo,
                                                                    numero_sensor=numero_sensor,
                                                                    posicao=posicao_sensor,
                                                                    num_frequencia_referencia=numero_frequencia_referencia)
    Objeto_visualizar_Freq.plotar_fft(  salvar=True,
                                        plotar=True
                                        )

    Objeto_visualizar_Freq.plotar_fft_com_frequencia_de_referencia( salvar=True,
                                                                    plotar=True
                                                                )
    Objeto_visualizar_Freq.plotar_bandas(numero_de_harmonicos,plotar=True)

    Objeto_visualizar_Freq = 0
