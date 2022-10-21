from math import *

class Bearing():

    def __init__(self,rpm,d_pista_externa,d_pista_interna,n_rolos,phi = 0):

        self.d_rolo = (self.d_pista_externa - self.d_pista_interna)
        self.d_medio = (self.d_pista_externa - self.d_pista_interna)/2
        self.freq_rot = self.rpm*2*pi/60

    def freq_outer_race(self):
        #self.freq_rot = self.rpm*2*pi/60
        return self.freq_rot*self.n_rolos*0.5*(1-(self.d_rolo/self.d_medio)*cos(self.phi))

    def freq_innter_race(self):
        #self.freq_rot = self.rpm*2*pi/60
        return self.freq_rot*self.n_rolos*0.5*(1+(self.d_rolo/self.d_medio)*cos(self.phi))
    
    def freq_gaiola(self):
        #self.freq_rot = self.rpm*2*pi/60
        return self.freq_rot*0.5*(1-(self.d_rolo/self.d_medio)*cos(self.phi))
    
    def freq_rolo(self):
        #self.freq_rot = self.rpm*2*pi/60
        return (self.d_medio/(2*self.d_rolo))*(1-((self.d_rolo/self.d_medio)*cos(self.phi))**2)

