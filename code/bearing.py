from math import *

class Bearing():

    def __init__(self,d_pista_externa,d_pista_interna,n_rolos,phi = 0):
        '''
        Unidades de medida linear em milímetro
        Unidades de medida angular em rad

        Output precisa ser multiplicado pela frequência de rotação em Hz
        '''
        
        self.d_pista_externa = d_pista_externa
        self.d_pista_interna = d_pista_interna
        self.n_rolos = n_rolos
        self.phi = phi

        self.d_rolo = (self.d_pista_externa - self.d_pista_interna)/2
        self.d_medio = (self.d_pista_externa + self.d_pista_interna)/2

    def freq_outer_race(self):
        self.BPFO = (self.n_rolos/2)*(1-(self.d_rolo/self.d_medio)*cos(self.phi))
        return self.BPFO

    def freq_innter_race(self):
        self.BPFI = (self.n_rolos/2)*(1+(self.d_rolo/self.d_medio)*cos(self.phi))
        return self.BPFI
    
    def freq_gaiola(self):
        self.FTF = 0.5*(1-(self.d_rolo/self.d_medio)*cos(self.phi))
        return self.FTF
    
    def freq_rolo(self):
        self.BSF = (self.d_medio/self.d_rolo)*(1-((self.d_rolo/self.d_medio)*cos(self.phi))**2)
        return self.BSF

