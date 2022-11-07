# %%
from math import *

class NewBearing():

    def __init__(self,d_pista_externa:float,d_pista_interna:float,n_esferas:float,phi:float = 0) ->float:
        '''
        Unidades de medida linear em milímetro
        Phi deve ser fornecido em graus

        Output precisa ser multiplicado pela frequência de rotação em Hz
        '''
        
        self.d_pista_externa = d_pista_externa
        self.d_pista_interna = d_pista_interna
        self.n_esferas = n_esferas
        self.phi = phi*(pi/180)

        self.d_esfera = (self.d_pista_externa - self.d_pista_interna)/2
        self.d_medio = (self.d_pista_externa + self.d_pista_interna)/2

    def freq_outer_race(self):
        self.BPFO = (self.n_esferas/2)*(1-(self.d_esfera/self.d_medio)*cos(self.phi))
        return self.BPFO

    def freq_innter_race(self):
        self.BPFI = (self.n_esferas/2)*(1+(self.d_esfera/self.d_medio)*cos(self.phi))
        return self.BPFI
    
    def freq_gaiola(self):
        self.FTF = 0.5*(1-(self.d_esfera/self.d_medio)*cos(self.phi))
        return self.FTF
    
    def freq_esfera(self):
        self.BSF = (self.d_medio/(2*self.d_esfera))*(1-((self.d_esfera/self.d_medio)*cos(self.phi))**2)
        return self.BSF

rpm = 2000
hz = rpm/60
hz


rolamento = NewBearing(81.026,58.674,17,14)

# %%
rolamento.freq_gaiola()*hz

# %%
Frequency_Fundamental_Train = 0.0072*rpm
Frequency_Fundamental_Train

# %%
rolamento.freq_innter_race()*hz

# %%
Frequency_Inner_Ring_Defect = 0.1617*rpm
Frequency_Inner_Ring_Defect

# %%
rolamento.freq_outer_race()*hz

# %%
Frequency_Outer_Ring_Defect = 0.1217*rpm
Frequency_Outer_Ring_Defect

# %%
rolamento.freq_esfera()*hz

# %%
Frequency_Roller_Spin = 0.0559*rpm
Frequency_Roller_Spin

