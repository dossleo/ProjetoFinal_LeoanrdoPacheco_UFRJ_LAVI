import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os

# path_save_csv = os.path.join(os.getcwd(), "models")

class GenerateRPM():
    def __init__(self,rpm,freq_aquisic):
        self.rpm = rpm
        self.freq_aquisic = freq_aquisic


    def generate_array(self):
        self.array = np.random.rand(self.freq_aquisic)

        for i in range(0,self.freq_aquisic,self.rpm):
            random = np.random.rand(20)
            for j in range(len(random)):
                self.array[i+j] = 2+random[j]

        
        return pd.DataFrame(self.array)

    def save_as_csv(self,path):
        self.array = pd.DataFrame(self.generate_array())
        pd.DataFrame.to_csv(self.array,path)

    def plot_array(self):
        self.df = self.generate_array()
        plt.plot(range(len(self.array)),self.array)
        plt.show()



if __name__ == "__main__":
    teste = GenerateRPM(2000,20480)
    print(teste.generate_array())
    teste.save_as_csv('2000rpm_artificial_data.csv')
    teste.plot_array()
